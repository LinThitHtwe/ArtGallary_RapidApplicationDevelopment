"""Save uploaded gallery images into the project `assets/` folder (served as static files)."""

from __future__ import annotations

import uuid
from pathlib import Path

from django.conf import settings


def save_uploaded_image(uploaded_file) -> str:
    """
    Write chunks to ASSETS_DIR with a unique name. Returns basename for `Artwork.image_path`.
    """
    assets_dir: Path = settings.ASSETS_DIR
    assets_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        ext = ".jpg"
    name = f"upload_{uuid.uuid4().hex}{ext}"
    dest = assets_dir / name
    with dest.open("wb") as out:
        for chunk in uploaded_file.chunks():
            out.write(chunk)
    return name
