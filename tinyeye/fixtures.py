from __future__ import annotations

from pathlib import Path


_MINI_JPEG = bytes.fromhex(
    "ffd8ffe000104a46494600010100000100010000ffdb0043000806060706050807070709"
    "09080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c"
    "30313434341f27393d38323c2e333432ffc0000b080001000101011100ffda000800010001"
    "3f00fb94a28a2803ffd9"
)


def write_swatch(path: Path, color=(180, 40, 40), size=64) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        Image.new("RGB", (size, size), color).save(path, quality=85)
    except Exception:
        path.write_bytes(_MINI_JPEG)
    return path


def write_mug(path: Path) -> Path:
    return write_swatch(path, color=(180, 40, 40), size=64)
