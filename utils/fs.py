"""Filesystem helpers: safe names, content hashing, atomic writes, disk space and fonts.

This module deliberately imports only :mod:`config.constants` and :mod:`utils.exceptions`.
It must not import :mod:`config.settings`, which itself depends on ``utils.exceptions`` and
would create an import cycle. Callers pass directories in explicitly.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from config.constants import (
    ANTON_FILENAME,
    ANTON_TTF_URL,
    FONT_EXTENSIONS,
    INTER_ZIP_MEMBER_CANDIDATES,
    INTER_ZIP_URL,
    MIN_FREE_DISK_BYTES,
    PROJECT_ROOT,
    SYSTEM_FONT_DIRECTORIES,
    SYSTEM_FONT_PREFERENCES,
)
from utils.exceptions import DiskSpaceError, FontNotFoundError

__all__ = [
    "atomic_write_bytes",
    "atomic_write_text",
    "available_fonts",
    "clear_directory",
    "default_fonts_dir",
    "describe_paths",
    "download_default_font",
    "ensure_parent",
    "file_sha256",
    "font_is_resolvable",
    "format_bytes",
    "free_disk_bytes",
    "hash_payload",
    "human_duration",
    "read_json",
    "require_free_disk",
    "resolve_font",
    "safe_filename",
    "temporary_path",
    "write_json",
]

_UNSAFE_FILENAME_CHARS = re.compile(r"[^A-Za-z0-9._-]+")
_REPEATED_SEPARATORS = re.compile(r"[-_]{2,}")


# --------------------------------------------------------------------------------------
# Names and hashing
# --------------------------------------------------------------------------------------


def safe_filename(value: str, *, max_length: int = 80, fallback: str = "untitled") -> str:
    """Convert arbitrary text into a portable filename component.

    Accents are folded to ASCII and every character outside ``[A-Za-z0-9._-]`` becomes a
    hyphen, which keeps names valid on Windows, macOS and Linux alike.

    Args:
        value: Arbitrary text, for example a video title.
        max_length: Maximum length of the returned string.
        fallback: Returned when ``value`` contains no usable characters.

    Returns:
        A filename-safe string, never empty and never longer than ``max_length``.
    """
    folded = unicodedata.normalize("NFKD", value)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    cleaned = _UNSAFE_FILENAME_CHARS.sub("-", ascii_only)
    cleaned = _REPEATED_SEPARATORS.sub("-", cleaned).strip("-_.")
    if not cleaned:
        return fallback
    return cleaned[:max_length].rstrip("-_.") or fallback


def hash_payload(*parts: Any) -> str:
    """Compute a stable SHA-256 over an arbitrary set of cache-key inputs.

    Values are serialised as sorted-key JSON so that dictionaries hash identically regardless
    of insertion order, which keeps cache keys stable across runs and Python versions.

    Args:
        *parts: Any JSON-serialisable values. Non-serialisable values fall back to ``repr``.

    Returns:
        A 64-character lowercase hex digest.
    """
    serialised = json.dumps(parts, sort_keys=True, ensure_ascii=False, default=repr)
    return hashlib.sha256(serialised.encode("utf-8")).hexdigest()


def file_sha256(path: Path, *, chunk_size: int = 1 << 20) -> str:
    """Hash a file's contents without loading it into memory.

    Args:
        path: File to hash.
        chunk_size: Read buffer size in bytes.

    Returns:
        A 64-character lowercase hex digest.

    Raises:
        OSError: If the file cannot be read.
    """
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


# --------------------------------------------------------------------------------------
# Writing
# --------------------------------------------------------------------------------------


def ensure_parent(path: Path) -> Path:
    """Create the parent directory of ``path`` if needed.

    Args:
        path: A file path whose directory should exist.

    Returns:
        The unchanged ``path``, so calls can be chained.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def atomic_write_bytes(path: Path, data: bytes) -> Path:
    """Write bytes to ``path`` atomically.

    The data lands in a sibling ``.part`` file that is renamed into place, so a crash mid-write
    can never leave a truncated artifact that a later run would treat as a valid cache hit.

    Args:
        path: Destination file.
        data: Payload to write.

    Returns:
        The destination path.

    Raises:
        OSError: If the write or rename fails.
    """
    ensure_parent(path)
    temp_path = path.with_suffix(path.suffix + ".part")
    try:
        temp_path.write_bytes(data)
        temp_path.replace(path)
    finally:
        temp_path.unlink(missing_ok=True)
    return path


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> Path:
    """Write text to ``path`` atomically, without a byte-order mark.

    Args:
        path: Destination file.
        text: Payload to write.
        encoding: Text encoding, UTF-8 by default.

    Returns:
        The destination path.
    """
    return atomic_write_bytes(path, text.encode(encoding))


def write_json(path: Path, payload: Any, *, indent: int = 2) -> Path:
    """Serialise ``payload`` to ``path`` as UTF-8 JSON.

    Args:
        path: Destination file.
        payload: Any JSON-serialisable object.
        indent: Indentation width.

    Returns:
        The destination path.
    """
    text = json.dumps(payload, indent=indent, ensure_ascii=False, default=str)
    return atomic_write_text(path, text + "\n")


def read_json(path: Path) -> Any:
    """Read UTF-8 JSON from ``path``.

    Args:
        path: File to read.

    Returns:
        The decoded object.

    Raises:
        OSError: If the file cannot be read.
        json.JSONDecodeError: If the contents are not valid JSON.
    """
    return json.loads(path.read_text(encoding="utf-8"))


@contextmanager
def temporary_path(suffix: str = "", directory: Path | None = None) -> Iterator[Path]:
    """Yield a path to a temporary file that is removed on exit.

    The file is closed immediately so the caller may reopen or replace it, which Windows
    requires before another handle can write to the same name.

    Args:
        suffix: Filename suffix, for example ``".mp4"``.
        directory: Parent directory. Defaults to the system temp directory.

    Yields:
        The temporary file path.
    """
    if directory is not None:
        directory.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(suffix=suffix, dir=str(directory) if directory else None)
    os.close(handle)
    path = Path(name)
    try:
        yield path
    finally:
        path.unlink(missing_ok=True)


def clear_directory(directory: Path, *, keep_directory: bool = True) -> int:
    """Delete everything inside ``directory``.

    Args:
        directory: Directory to empty. A missing directory is not an error.
        keep_directory: When true, the directory itself is preserved.

    Returns:
        The number of entries removed.
    """
    if not directory.is_dir():
        return 0
    removed = 0
    for entry in directory.iterdir():
        if entry.is_dir() and not entry.is_symlink():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            entry.unlink(missing_ok=True)
        removed += 1
    if not keep_directory:
        shutil.rmtree(directory, ignore_errors=True)
    return removed


# --------------------------------------------------------------------------------------
# Disk space and formatting
# --------------------------------------------------------------------------------------


def free_disk_bytes(path: Path) -> int:
    """Return the free space on the volume holding ``path``.

    Walks up to the nearest existing ancestor, so the check works before the output directory
    has been created.

    Args:
        path: Any path on the volume of interest.

    Returns:
        Free bytes available to the current user.
    """
    probe = path
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    return shutil.disk_usage(probe).free


def require_free_disk(path: Path, minimum: int = MIN_FREE_DISK_BYTES) -> int:
    """Assert that enough disk space is available.

    Args:
        path: Any path on the volume to check.
        minimum: Required free bytes.

    Returns:
        The actual number of free bytes.

    Raises:
        DiskSpaceError: If free space is below ``minimum``.
    """
    free = free_disk_bytes(path)
    if free < minimum:
        raise DiskSpaceError(
            f"Only {format_bytes(free)} free on the volume holding {path}, "
            f"{format_bytes(minimum)} required.",
            hint="Free up space or point OUTPUT_DIR at a roomier drive.",
        )
    return free


def format_bytes(count: float) -> str:
    """Render a byte count in human-readable units.

    Args:
        count: Number of bytes.

    Returns:
        A string such as ``"1.4 GB"``.
    """
    size = float(count)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(size) < 1024.0 or unit == "TB":
            precision = 0 if unit == "B" else 1
            return f"{size:.{precision}f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def human_duration(seconds: float) -> str:
    """Render a duration as ``M:SS`` or ``H:MM:SS``.

    Args:
        seconds: Duration in seconds.

    Returns:
        A compact human-readable duration.
    """
    total = int(round(max(0.0, seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


# --------------------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------------------


def default_fonts_dir() -> Path:
    """Return the bundled font directory.

    Returns:
        ``<project root>/assets/fonts``.
    """
    return PROJECT_ROOT / "assets" / "fonts"


def available_fonts(fonts_dir: Path | None = None) -> list[Path]:
    """List font files present in the project's font directory.

    Args:
        fonts_dir: Directory to scan. Defaults to :func:`default_fonts_dir`.

    Returns:
        Sorted font file paths, possibly empty.
    """
    directory = fonts_dir or default_fonts_dir()
    if not directory.is_dir():
        return []
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in FONT_EXTENSIONS
    )


def _iter_system_font_candidates() -> Iterator[Path]:
    """Yield plausible system font files, most preferred first.

    Yields:
        Existing font paths from the current platform's font directories.
    """
    platform_key = "linux"
    if sys.platform.startswith("win"):
        platform_key = "win32"
    elif sys.platform == "darwin":
        platform_key = "darwin"

    directories = [
        Path(entry).expanduser() for entry in SYSTEM_FONT_DIRECTORIES.get(platform_key, ())
    ]

    for preferred in SYSTEM_FONT_PREFERENCES:
        for directory in directories:
            candidate = directory / preferred
            if candidate.is_file():
                yield candidate

    for directory in directories:
        if not directory.is_dir():
            continue
        try:
            entries = sorted(directory.rglob("*"))
        except OSError:
            continue
        for entry in entries:
            if entry.is_file() and entry.suffix.lower() in FONT_EXTENSIONS:
                yield entry


def resolve_font(
    requested: Path | None,
    *,
    fonts_dir: Path | None = None,
    allow_system_fallback: bool = True,
) -> tuple[Path, str | None]:
    """Find a usable font file, degrading gracefully.

    Resolution order, with the reason for each fallback reported to the caller:

    1. ``requested`` exactly as given.
    2. A file of the same name inside ``fonts_dir``.
    3. Any other font already present in ``fonts_dir``.
    4. A platform font directory scan, when ``allow_system_fallback`` is set.

    Args:
        requested: The font path from the scenario or settings. May be ``None``.
        fonts_dir: Project font directory. Defaults to :func:`default_fonts_dir`.
        allow_system_fallback: Whether step 4 is permitted.

    Returns:
        A tuple of the resolved font path and a warning message. The warning is ``None`` when
        the requested font was used verbatim, and otherwise explains the substitution so the
        caller can log it.

    Raises:
        FontNotFoundError: If no usable font exists anywhere.
    """
    directory = fonts_dir or default_fonts_dir()

    if requested is not None:
        candidate = requested if requested.is_absolute() else (PROJECT_ROOT / requested)
        if candidate.is_file():
            return candidate, None

        same_name = directory / candidate.name
        if same_name.is_file():
            return same_name, (
                f"Font {requested} not found; using {same_name.name} from {directory}."
            )

    bundled = available_fonts(directory)
    if bundled:
        chosen = bundled[0]
        requested_label = str(requested) if requested else "<unset>"
        return chosen, (
            f"Font {requested_label} not found; falling back to bundled font {chosen.name}."
        )

    if allow_system_fallback:
        for system_font in _iter_system_font_candidates():
            requested_label = str(requested) if requested else "<unset>"
            return system_font, (
                f"Font {requested_label} not found and {directory} is empty; falling back to "
                f"the system font {system_font.name}. Run 'python main.py doctor --fix' to "
                "install a bundled font for reproducible output."
            )

    raise FontNotFoundError(
        f"No usable font found. Looked for {requested}, scanned {directory}"
        + (" and the system font directories." if allow_system_fallback else "."),
        hint=(
            "Run 'python main.py doctor --fix' to download one, or drop any .ttf into "
            f"{directory} and point subtitles.font at it."
        ),
    )


def font_is_resolvable(requested: Path | None, *, fonts_dir: Path | None = None) -> bool:
    """Report whether :func:`resolve_font` would succeed.

    Used by scenario validation, which should fail only when no font exists at all rather than
    when the exact configured file is missing.

    Args:
        requested: The font path from the scenario.
        fonts_dir: Project font directory. Defaults to :func:`default_fonts_dir`.

    Returns:
        ``True`` when some font can be resolved.
    """
    try:
        resolve_font(requested, fonts_dir=fonts_dir)
    except FontNotFoundError:
        return False
    return True


def _extract_font_from_zip(archive: bytes, destination: Path) -> Path | None:
    """Pull the first matching static font out of a downloaded archive.

    Args:
        archive: Raw bytes of a ZIP file.
        destination: Path the extracted font should be written to.

    Returns:
        The written path, or ``None`` when the archive holds none of the expected members.
    """
    import io

    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            names = bundle.namelist()
            for wanted in INTER_ZIP_MEMBER_CANDIDATES:
                for name in names:
                    if name.endswith(f"/{wanted}") or name == wanted:
                        atomic_write_bytes(destination, bundle.read(name))
                        return destination
    except (zipfile.BadZipFile, KeyError, OSError):
        return None
    return None


def download_default_font(
    fonts_dir: Path | None = None,
    *,
    timeout: float = 60.0,
) -> tuple[Path, str]:
    """Download an SIL Open Font License font into the project font directory.

    Tries the official Inter release archive first, extracting a static bold face, and falls
    back to Anton, a single-file display font that is always available as a direct download.

    Args:
        fonts_dir: Destination directory. Defaults to :func:`default_fonts_dir`.
        timeout: Per-request timeout in seconds.

    Returns:
        A tuple of the written font path and a short description of its source.

    Raises:
        FontNotFoundError: If every download attempt fails.
    """
    import requests

    directory = fonts_dir or default_fonts_dir()
    directory.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    inter_target = directory / "Inter-Bold.ttf"
    try:
        response = requests.get(INTER_ZIP_URL, timeout=timeout)
        response.raise_for_status()
        extracted = _extract_font_from_zip(response.content, inter_target)
        if extracted is not None:
            return extracted, "Inter (SIL OFL 1.1), from the official rsms/inter release"
        failures.append("Inter archive contained no static bold face")
    except requests.RequestException as exc:
        failures.append(f"Inter download failed: {exc}")

    anton_target = directory / ANTON_FILENAME
    try:
        response = requests.get(ANTON_TTF_URL, timeout=timeout)
        response.raise_for_status()
        if not response.content:
            failures.append("Anton download returned an empty body")
        else:
            atomic_write_bytes(anton_target, response.content)
            return anton_target, "Anton (SIL OFL 1.1), from the Google Fonts repository"
    except requests.RequestException as exc:
        failures.append(f"Anton download failed: {exc}")

    raise FontNotFoundError(
        "Could not download a default font. " + "; ".join(failures),
        hint=(
            "Check your internet connection, or download any .ttf manually into "
            f"{directory}. See assets/fonts/README.md for suggestions."
        ),
    )


def describe_paths(paths: Iterable[Path]) -> str:
    """Join paths into a compact, readable list for log messages.

    Args:
        paths: Paths to describe.

    Returns:
        A comma-separated list of file names, or ``"none"`` when empty.
    """
    names = [path.name for path in paths]
    return ", ".join(names) if names else "none"
