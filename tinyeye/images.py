from __future__ import annotations

from pathlib import Path

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def collect_images(paths=None, directory=None):
    files = []
    if directory:
        d = Path(directory)
        if d.exists():
            for p in sorted(d.rglob("*")):
                if p.suffix.lower() in EXTS and p.is_file():
                    files.append(p)
    for p in paths or []:
        path = Path(p)
        if path.is_file() and path.suffix.lower() in EXTS:
            files.append(path)
        elif path.is_dir():
            for q in sorted(path.rglob("*")):
                if q.suffix.lower() in EXTS and q.is_file():
                    files.append(q)
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def image_stats(path: Path) -> dict:
    """Numbers only. Never a caption."""
    path = Path(path)
    info = {"bytes": path.stat().st_size if path.exists() else 0}
    try:
        from PIL import Image

        im = Image.open(path)
        info["width"] = im.size[0]
        info["height"] = im.size[1]
        info["mode"] = im.mode
        rgb = im.convert("RGB").resize((1, 1))
        r, g, b = rgb.getpixel((0, 0))
        info["mean_r"] = int(r)
        info["mean_g"] = int(g)
        info["mean_b"] = int(b)
    except Exception:
        pass
    return info
