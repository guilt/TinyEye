"""Write organism Eye pair: stem.eye.jpg + stem.eye.md.

Latent is optional extra (.pyc). JPEG + md is the memory (.py).
Watch has no camera — import files only. Do not invent a caption.
"""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path


def write_eye_pair(
    src_jpg: Path,
    out_dir: Path,
    belief: str = "",
    source: str = "import",
    confidence: float = 0.4,
    latent_ok: bool = False,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src_jpg.stem
    dest_jpg = out_dir / f"{stem}.eye.jpg"
    if src_jpg.resolve() != dest_jpg.resolve():
        shutil.copy2(src_jpg, dest_jpg)
    belief_ok = bool(belief.strip())
    md = out_dir / f"{stem}.eye.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md.write_text(
        "\n".join(
            [
                "---",
                "modality: eye",
                f"time: {now}",
                f"source: {source}",
                f"confidence: {confidence}",
                f"latent_ok: {'true' if latent_ok else 'false'}",
                f"belief_ok: {'true' if belief_ok else 'false'}",
                "---",
                "",
                "## Belief",
                belief.strip(),
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"  pair    -> {dest_jpg}")
    print(f"  belief  -> {md}")
    return dest_jpg, md
