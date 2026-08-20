"""YouTube Data API v3 upload with OAuth 2.0 and resumable transfer.

Two quota realities shape how this module behaves, and both are documented in the README.
A single ``videos.insert`` costs roughly 1600 units against a default daily allowance of
10,000, which permits about six uploads per day. And while the Google Cloud OAuth consent
screen is still in "Testing", refresh tokens expire after seven days and uploaded videos stay
locked to private no matter what privacy status is requested.

Retries are therefore deliberately narrow. A ``500`` is worth retrying; a ``quotaExceeded``
is not, and burning attempts on it only delays the error the user needs to see.
"""

from __future__ import annotations

import contextlib
import json
import os
import random
import stat
import sys
import time
from pathlib import Path
from typing import Any

from config.constants import (
    ATTRIBUTION_HEADER,
    ATTRIBUTION_LINE_TEMPLATE,
    SYNTHETIC_DISCLOSURE_TEXT,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    YOUTUBE_DESCRIPTION_MAX_CHARS,
    YOUTUBE_FATAL_REASONS,
    YOUTUBE_RETRIABLE_REASONS,
    YOUTUBE_RETRIABLE_STATUS_CODES,
    YOUTUBE_SCOPES,
    YOUTUBE_UPLOAD_CHUNK_SIZE,
    YOUTUBE_WATCH_URL_TEMPLATE,
)
from models.scenario import YouTubeSettings
from modules.interfaces import IUploader, MediaCredit, UploadResult
from utils.exceptions import UploadAuthError, UploadError, UploadQuotaError
from utils.logger import get_logger, log_info, log_warn

__all__ = ["YouTubeUploader", "build_description"]

logger = get_logger(__name__)

MAX_UPLOAD_ATTEMPTS = 5
INITIAL_BACKOFF_SECONDS = 2.0
MAX_BACKOFF_SECONDS = 60.0


def build_description(
    base: str,
    credits: list[MediaCredit],
    *,
    synthetic_disclosure: bool,
    max_chars: int = YOUTUBE_DESCRIPTION_MAX_CHARS,
) -> str:
    """Append the legally required attribution block to a description.

    The Pexels and Pixabay licences require crediting contributors, and YouTube requires
    disclosing synthetic or altered content. Both are appended here rather than left to the
    scenario author, so they cannot be forgotten.

    If the combined text would exceed ``max_chars``, the author's own description is trimmed
    and the attribution block is preserved intact, because the attribution is the part with a
    legal obligation attached.

    Args:
        base: The description from the scenario.
        credits: Attribution records, deduplicated by contributor.
        synthetic_disclosure: Whether to add the synthetic-audio disclosure line.
        max_chars: YouTube's description limit.

    Returns:
        The final description, never longer than ``max_chars``.
    """
    seen: set[tuple[str, str]] = set()
    lines: list[str] = []
    for credit in credits:
        key = credit.key()
        if key in seen:
            continue
        seen.add(key)
        lines.append(credit.as_line(ATTRIBUTION_LINE_TEMPLATE))

    block_parts: list[str] = []
    if lines:
        block_parts.append("\n".join(lines))
    if synthetic_disclosure:
        block_parts.append(SYNTHETIC_DISCLOSURE_TEXT)

    if not block_parts:
        return base[:max_chars]

    block = f"\n\n{ATTRIBUTION_HEADER}\n" + "\n\n".join(block_parts)

    if len(base) + len(block) <= max_chars:
        return base + block

    if len(block) >= max_chars:
        return block[:max_chars]

    ellipsis = "..."
    budget = max_chars - len(block) - len(ellipsis)
    trimmed = base[: max(0, budget)].rstrip()
    log_warn(
        f"Description trimmed to fit YouTube's {max_chars} character limit; "
        "the attribution block was preserved."
    )
    return trimmed + ellipsis + block


class YouTubeUploader(IUploader):
    """Uploads to YouTube with an installed-app OAuth flow and resumable transfer."""

    def __init__(
        self,
        client_secrets_file: Path,
        token_file: Path,
        *,
        credits: list[MediaCredit] | None = None,
        caption_file: Path | None = None,
        chunk_size: int = YOUTUBE_UPLOAD_CHUNK_SIZE,
    ) -> None:
        """Initialise the uploader.

        Args:
            client_secrets_file: Path to the OAuth client secrets JSON.
            token_file: Path where the access and refresh tokens are cached.
            credits: Attribution records appended to the description.
            caption_file: Optional SRT to attach as a caption track.
            chunk_size: Resumable upload chunk size in bytes.
        """
        self._client_secrets_file = client_secrets_file
        self._token_file = token_file
        self._credits = credits or []
        self._caption_file = caption_file
        self._chunk_size = chunk_size
        self._service: Any = None

    # ----------------------------------------------------------------------------------
    # Authentication
    # ----------------------------------------------------------------------------------

    def authenticate(self) -> None:
        """Load, refresh or interactively obtain OAuth credentials.

        Raises:
            UploadAuthError: If the client secrets file is missing or malformed, or if the
                consent flow cannot be completed.
        """
        from google.auth.exceptions import RefreshError
        from google.auth.transport.requests import Request

        credentials = self._load_cached_credentials()

        if credentials is not None and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                logger.debug("Refreshed the cached OAuth token")
            except RefreshError as exc:
                log_warn(
                    "The cached YouTube token could not be refreshed and will be replaced. "
                    "While the OAuth consent screen is in Testing, refresh tokens expire "
                    f"after 7 days. ({exc})"
                )
                credentials = None

        if credentials is None or not credentials.valid:
            credentials = self._run_consent_flow()

        self._persist_credentials(credentials)
        self._service = self._build_service(credentials)
        logger.info("YouTube authentication complete")

    def _load_cached_credentials(self) -> Any:
        """Read cached credentials from disk.

        Returns:
            The cached credentials, or ``None`` when absent or unreadable.
        """
        from google.oauth2.credentials import Credentials

        if not self._token_file.is_file():
            return None
        try:
            return Credentials.from_authorized_user_file(
                str(self._token_file), list(YOUTUBE_SCOPES)
            )
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            log_warn(f"Ignoring an unreadable token file at {self._token_file}: {exc}")
            return None

    def _run_consent_flow(self) -> Any:
        """Run the interactive installed-app OAuth flow.

        Returns:
            Freshly granted credentials.

        Raises:
            UploadAuthError: If the client secrets file is missing or the flow fails.
        """
        from google_auth_oauthlib.flow import InstalledAppFlow

        if not self._client_secrets_file.is_file():
            raise UploadAuthError(
                f"OAuth client secrets not found at {self._client_secrets_file}.",
                hint=(
                    "Create an OAuth 2.0 Desktop app client in the Google Cloud Console and "
                    "save the downloaded JSON there. The README has a step-by-step "
                    "walkthrough."
                ),
            )

        try:
            payload = json.loads(self._client_secrets_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise UploadAuthError(
                f"Could not read {self._client_secrets_file}: {exc}",
                hint="Re-download the client secrets JSON from the Google Cloud Console.",
            ) from exc

        if "installed" not in payload:
            raise UploadAuthError(
                f"{self._client_secrets_file.name} is not a Desktop app client "
                f"(top-level keys: {sorted(payload)}).",
                hint=(
                    "In the Google Cloud Console, create a new OAuth client with the "
                    "application type 'Desktop app' and download that file instead."
                ),
            )

        log_info("Opening your browser for YouTube authorization...")
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self._client_secrets_file), scopes=list(YOUTUBE_SCOPES)
            )
            return flow.run_local_server(port=0, prompt="consent")
        except Exception as exc:
            raise UploadAuthError(
                f"The OAuth consent flow failed: {exc}",
                hint=(
                    "Make sure your Google account is listed as a test user on the OAuth "
                    "consent screen, and that YouTube Data API v3 is enabled."
                ),
            ) from exc

    def _persist_credentials(self, credentials: Any) -> None:
        """Write credentials to disk with owner-only permissions.

        Args:
            credentials: The credentials to cache.

        Raises:
            UploadAuthError: If the token file cannot be written.
        """
        try:
            self._token_file.parent.mkdir(parents=True, exist_ok=True)
            self._token_file.write_text(credentials.to_json(), encoding="utf-8")
        except OSError as exc:
            raise UploadAuthError(f"Could not save the token to {self._token_file}: {exc}") from exc

        if sys.platform != "win32":
            with contextlib.suppress(OSError):
                os.chmod(self._token_file, stat.S_IRUSR | stat.S_IWUSR)

    @staticmethod
    def _build_service(credentials: Any) -> Any:
        """Construct the YouTube API client.

        Args:
            credentials: Valid OAuth credentials.

        Returns:
            The API service object.

        Raises:
            UploadAuthError: If the client cannot be constructed.
        """
        from googleapiclient.discovery import build

        try:
            return build(
                YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                credentials=credentials,
                cache_discovery=False,
            )
        except Exception as exc:
            raise UploadAuthError(f"Could not create the YouTube API client: {exc}") from exc

    def _require_service(self) -> Any:
        """Return the API client, authenticating first if needed.

        Returns:
            The API service object.
        """
        if self._service is None:
            self.authenticate()
        return self._service

    # ----------------------------------------------------------------------------------
    # Upload
    # ----------------------------------------------------------------------------------

    def upload(
        self,
        video_path: Path,
        meta: YouTubeSettings,
        thumbnail: Path | None,
    ) -> UploadResult:
        """Upload a video, then apply its thumbnail, playlist and captions.

        Args:
            video_path: The MP4 to publish.
            meta: Title, description, tags and privacy settings.
            thumbnail: Optional custom thumbnail.

        Returns:
            The new video's id, URL and applied privacy status.

        Raises:
            UploadError: If the upload fails.
            UploadQuotaError: If the daily API quota is exhausted.
        """
        if not video_path.is_file():
            raise UploadError(f"Cannot upload, video not found: {video_path}")

        service = self._require_service()
        body = self._build_body(meta)
        response = self._insert_video(service, video_path, body)

        video_id = str(response.get("id", "")).strip()
        if not video_id:
            raise UploadError(f"YouTube accepted the upload but returned no video id: {response}")

        applied_privacy = str(
            (response.get("status") or {}).get("privacyStatus", meta.privacy_status)
        )
        if applied_privacy != meta.privacy_status:
            log_warn(
                f"YouTube applied privacyStatus '{applied_privacy}' instead of the requested "
                f"'{meta.privacy_status}'. Unverified OAuth apps have their uploads locked to "
                "private until the app is verified."
            )

        result = UploadResult(
            video_id=video_id,
            url=YOUTUBE_WATCH_URL_TEMPLATE.format(video_id=video_id),
            privacy_status=applied_privacy,
        )

        thumbnail_set = self._maybe_set_thumbnail(service, video_id, meta, thumbnail)
        playlist_id = self._maybe_add_to_playlist(service, video_id, meta)
        caption_uploaded = self._maybe_upload_caption(service, video_id, meta)

        return UploadResult(
            video_id=result.video_id,
            url=result.url,
            privacy_status=result.privacy_status,
            thumbnail_set=thumbnail_set,
            playlist_id=playlist_id,
            caption_uploaded=caption_uploaded,
        )

    def _build_body(self, meta: YouTubeSettings) -> dict[str, Any]:
        """Build the ``videos.insert`` request body.

        Args:
            meta: The scenario's YouTube settings.

        Returns:
            The request body, with attribution already merged into the description.
        """
        description = build_description(
            meta.description,
            self._credits,
            synthetic_disclosure=meta.synthetic_content_disclosure,
        )

        status: dict[str, Any] = {
            "privacyStatus": meta.privacy_status,
            "selfDeclaredMadeForKids": meta.made_for_kids,
            "license": "youtube",
            "embeddable": True,
        }
        if meta.publish_at is not None:
            status["publishAt"] = meta.publish_at.isoformat()

        return {
            "snippet": {
                "title": meta.title,
                "description": description,
                "tags": meta.tags,
                "categoryId": meta.category_id,
                "defaultLanguage": meta.default_language,
                "defaultAudioLanguage": meta.default_language,
            },
            "status": status,
        }

    def _insert_video(self, service: Any, video_path: Path, body: dict[str, Any]) -> dict[str, Any]:
        """Perform the resumable upload, retrying only transient failures.

        Args:
            service: The API client.
            video_path: The MP4 to upload.
            body: The request body.

        Returns:
            The API response for the created video.

        Raises:
            UploadError: If the upload fails permanently.
            UploadQuotaError: If the daily quota is exhausted.
        """
        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload

        media = MediaFileUpload(
            str(video_path),
            chunksize=self._chunk_size,
            resumable=True,
            mimetype="video/mp4",
        )
        request = service.videos().insert(part="snippet,status", body=body, media_body=media)

        log_info(f"Uploading {video_path.name} ({video_path.stat().st_size / 1e6:.1f} MB)...")

        response: dict[str, Any] | None = None
        attempt = 0
        last_percent = -1

        while response is None:
            try:
                status, response = request.next_chunk()
                attempt = 0
                if status is not None:
                    percent = int(status.progress() * 100)
                    if percent >= last_percent + 5:
                        last_percent = percent
                        log_info(f"Upload progress: {percent}%")
            except HttpError as exc:
                attempt += 1
                self._handle_http_error(exc, attempt)
            except (OSError, ConnectionError) as exc:
                attempt += 1
                if attempt >= MAX_UPLOAD_ATTEMPTS:
                    raise UploadError(
                        f"The upload connection failed {attempt} times: {exc}",
                        hint="Check your internet connection and re-run.",
                    ) from exc
                self._sleep_backoff(attempt)

        log_info("Upload complete, finalizing...")
        return response

    def _handle_http_error(self, exc: Any, attempt: int) -> None:
        """Decide whether an ``HttpError`` is worth retrying, and back off if so.

        Args:
            exc: The raised ``HttpError``.
            attempt: The consecutive failure count.

        Raises:
            UploadQuotaError: On a quota exhaustion, which retrying cannot fix.
            UploadError: On any other non-retryable error, or once attempts run out.
        """
        status_code = int(getattr(getattr(exc, "resp", None), "status", 0) or 0)
        reason = self._extract_reason(exc)

        if reason in YOUTUBE_FATAL_REASONS or status_code in {400, 401, 404}:
            if reason == "quotaExceeded":
                raise UploadQuotaError(
                    "The YouTube API daily quota is exhausted.",
                    hint=(
                        "An upload costs about 1600 of the default 10,000 daily units, so "
                        "roughly six uploads per day. The quota resets at midnight Pacific "
                        "time, or you can request an increase in the Google Cloud Console."
                    ),
                )
            raise UploadError(
                f"YouTube rejected the upload (HTTP {status_code}, reason '{reason}').",
                hint=self._hint_for(status_code, reason),
            )

        retryable = status_code in YOUTUBE_RETRIABLE_STATUS_CODES or (
            status_code == 403 and reason in YOUTUBE_RETRIABLE_REASONS
        )
        if not retryable:
            raise UploadError(
                f"YouTube returned HTTP {status_code} (reason '{reason}'), which is not retryable.",
                hint=self._hint_for(status_code, reason),
            )

        if attempt >= MAX_UPLOAD_ATTEMPTS:
            raise UploadError(
                f"The upload failed {attempt} times with HTTP {status_code} (reason '{reason}').",
                hint="YouTube is having trouble on its side. Try again in a few minutes.",
            )

        logger.warning(
            "Upload chunk failed with HTTP %s (%s); retrying (attempt %d/%d)",
            status_code,
            reason,
            attempt,
            MAX_UPLOAD_ATTEMPTS,
        )
        self._sleep_backoff(attempt)

    @staticmethod
    def _extract_reason(exc: Any) -> str:
        """Pull the API's own machine-readable reason string out of an error.

        Args:
            exc: The raised ``HttpError``.

        Returns:
            The reason string, or ``"unknown"`` when the body cannot be parsed.
        """
        content = getattr(exc, "content", None)
        if not content:
            return "unknown"
        try:
            text = content.decode("utf-8") if isinstance(content, bytes) else str(content)
            payload = json.loads(text)
            errors = payload.get("error", {}).get("errors") or []
            if errors and isinstance(errors, list):
                return str(errors[0].get("reason", "unknown"))
            return str(payload.get("error", {}).get("status", "unknown"))
        except (ValueError, AttributeError, KeyError, TypeError):
            return "unknown"

    @staticmethod
    def _hint_for(status_code: int, reason: str) -> str:
        """Map an API failure to an actionable next step.

        Args:
            status_code: The HTTP status.
            reason: The API's reason string.

        Returns:
            A hint for the user.
        """
        if status_code == 401:
            return "The token is invalid. Delete secrets/token.json and run 'python main.py auth'."
        if reason == "forbidden":
            return (
                "The channel may not be verified for uploads of this length, or the account "
                "lacks permission. Check https://www.youtube.com/verify."
            )
        if reason == "uploadLimitExceeded":
            return "The channel hit its daily upload cap. Try again tomorrow."
        if status_code == 400:
            return (
                "The request body was rejected. Check the title, tags and categoryId in your "
                "scenario file."
            )
        return "See https://developers.google.com/youtube/v3/docs/errors for this reason code."

    @staticmethod
    def _sleep_backoff(attempt: int) -> None:
        """Sleep for an exponentially increasing, jittered interval.

        Args:
            attempt: The consecutive failure count, starting at 1.
        """
        delay = min(INITIAL_BACKOFF_SECONDS * (2 ** (attempt - 1)), MAX_BACKOFF_SECONDS)
        delay += random.uniform(0, 1.0)
        logger.debug("Backing off for %.1fs", delay)
        time.sleep(delay)

    # ----------------------------------------------------------------------------------
    # Post-upload steps
    # ----------------------------------------------------------------------------------

    def _maybe_set_thumbnail(
        self,
        service: Any,
        video_id: str,
        meta: YouTubeSettings,
        thumbnail: Path | None,
    ) -> bool:
        """Attach a custom thumbnail, if one was produced and enabled.

        A failure here is logged rather than raised: the video is already published, and
        losing the whole run over a thumbnail would be worse than an uploaded video with the
        auto-generated one.

        Args:
            service: The API client.
            video_id: The uploaded video's id.
            meta: The scenario's YouTube settings.
            thumbnail: The thumbnail file, if any.

        Returns:
            ``True`` when the thumbnail was accepted.
        """
        if not meta.thumbnail_enabled or thumbnail is None or not thumbnail.is_file():
            return False

        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload

        try:
            service.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail), mimetype="image/jpeg"),
            ).execute()
        except HttpError as exc:
            log_warn(
                f"Could not set the custom thumbnail: {self._extract_reason(exc)}. "
                "Custom thumbnails require a verified YouTube account."
            )
            return False
        log_info("Custom thumbnail applied")
        return True

    def _maybe_add_to_playlist(
        self, service: Any, video_id: str, meta: YouTubeSettings
    ) -> str | None:
        """Add the video to a playlist, if one was configured.

        Args:
            service: The API client.
            video_id: The uploaded video's id.
            meta: The scenario's YouTube settings.

        Returns:
            The playlist id on success, otherwise ``None``.
        """
        if not meta.playlist_id:
            return None

        from googleapiclient.errors import HttpError

        try:
            service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": meta.playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
        except HttpError as exc:
            log_warn(
                f"Could not add the video to playlist {meta.playlist_id}: "
                f"{self._extract_reason(exc)}"
            )
            return None
        log_info(f"Added to playlist {meta.playlist_id}")
        return meta.playlist_id

    def _maybe_upload_caption(self, service: Any, video_id: str, meta: YouTubeSettings) -> bool:
        """Attach an SRT caption track when subtitles are not burned into the frame.

        Burned-in captions are already visible, so uploading them again would double them up
        for viewers who enable closed captions.

        Args:
            service: The API client.
            video_id: The uploaded video's id.
            meta: The scenario's YouTube settings.

        Returns:
            ``True`` when a caption track was accepted.
        """
        if self._caption_file is None or not self._caption_file.is_file():
            return False

        from googleapiclient.errors import HttpError
        from googleapiclient.http import MediaFileUpload

        try:
            service.captions().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "language": meta.default_language,
                        "name": "Auto-generated",
                        "isDraft": False,
                    }
                },
                media_body=MediaFileUpload(
                    str(self._caption_file), mimetype="application/octet-stream"
                ),
            ).execute()
        except HttpError as exc:
            log_warn(f"Could not upload the caption track: {self._extract_reason(exc)}")
            return False
        log_info("Caption track uploaded")
        return True
