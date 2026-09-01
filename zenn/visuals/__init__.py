"""Programmatic stick-figure frames and bundled SVG assets."""

from zenn.visuals.backgrounds import BACKGROUND_TAGS
from zenn.visuals.compose import compose_frame, save_frame
from zenn.visuals.poses import POSE_TAGS

__all__ = [
    "BACKGROUND_TAGS",
    "POSE_TAGS",
    "compose_frame",
    "save_frame",
]
