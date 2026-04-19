"""Save uploaded gallery images into the project `assets/` folder (served as static files)."""

from __future__ import annotations

import re
import uuid
from pathlib import Path

from django.conf import settings

_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def _sanitize_stem(stem: str) -> str:
    """Safe filename stem: word chars and hyphens only, collapsed to underscores."""
    s = (stem or "").strip()
    if not s:
        return ""
    s = re.sub(r"[^\w\-]+", "_", s, flags=re.UNICODE)
    s = re.sub(r"_+", "_", s).strip("_-")
    return s[:100] if s else ""


def save_uploaded_image(uploaded_file) -> str:
    """
    Write chunks to ASSETS_DIR. Uses the original file name (sanitized); if that
    file already exists, appends a short unique segment before the extension.
    Returns basename for `Artwork.image_path`.
    """
    assets_dir: Path = settings.ASSETS_DIR
    assets_dir.mkdir(parents=True, exist_ok=True)

    orig_name = Path(uploaded_file.name).name
    ext = Path(orig_name).suffix.lower()
    if ext not in _ALLOWED_EXT:
        ext = ".jpg"

    stem = _sanitize_stem(Path(orig_name).stem)
    if not stem:
        stem = "image"

    base = f"{stem}{ext}"
    candidate = base
    while (assets_dir / candidate).exists():
        candidate = f"{stem}_{uuid.uuid4().hex[:10]}{ext}"

    dest = assets_dir / candidate
    with dest.open("wb") as out:
        for chunk in uploaded_file.chunks():
            out.write(chunk)
    return candidate
