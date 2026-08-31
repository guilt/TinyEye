"""Write / parse organism Eye pair: stem.eye.jpg + stem.eye.md.

Latent is optional extra (.pyc). JPEG + md is the memory (.py).
Watch has no camera — import files only. Do not invent a caption.
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MISS = ""  # empty belief. Never a guessed caption.


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    text = text.replace("\r\n", "\n")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, Any] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        val = v.strip()
        if val in ("true", "false"):
            meta[k.strip()] = val == "true"
        else:
            meta[k.strip()] = val
    return meta, body


def extract_belief(body: str) -> str:
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## belief":
            start = i + 1
            break
    if start is None:
        return ""
    chunk = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        chunk.append(line)
    return "\n".join(chunk).strip()


def write_eye_pair(
    src_jpg: Path,
    out_dir: Path,
    belief: str = "",
    source: str = "import",
    confidence: float = 0.4,
    latent_ok: bool = False,
    stats: dict | None = None,
) -> tuple[Path, Path]:
    src_jpg = Path(src_jpg)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src_jpg.stem
    dest_jpg = out_dir / f"{stem}.eye.jpg"
    if src_jpg.resolve() != dest_jpg.resolve():
        shutil.copy2(src_jpg, dest_jpg)
    belief_ok = bool(str(belief).strip())
    md = out_dir / f"{stem}.eye.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "---",
        "modality: eye",
        f"time: {now}",
        f"source: {source}",
        f"confidence: {confidence}",
        f"latent_ok: {'true' if latent_ok else 'false'}",
        f"belief_ok: {'true' if belief_ok else 'false'}",
    ]
    if stats:
        for k, v in stats.items():
            lines.append(f"{k}: {v}")
    lines += ["---", "", "## Belief", str(belief).strip(), ""]
    md.write_text("\n".join(lines), encoding="utf-8")
    print(f"  pair    -> {dest_jpg}")
    print(f"  belief  -> {md}")
    return dest_jpg, md


@dataclass
class EyeSidecar:
    path: Path
    meta: dict[str, Any] = field(default_factory=dict)
    belief: str = ""
    jpg_path: str | None = None

    @property
    def belief_ok(self) -> bool:
        return bool(self.meta.get("belief_ok")) and bool(self.belief.strip())


def parse_eye(path: Path) -> EyeSidecar:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    stem = path.name[: -len(".eye.md")] if path.name.endswith(".eye.md") else path.stem
    jpg = None
    for ext in (".jpg", ".jpeg", ".png"):
        cand = path.with_name(f"{stem}.eye{ext}")
        if cand.exists():
            jpg = str(cand)
            break
    return EyeSidecar(path=path, meta=meta, belief=extract_belief(body), jpg_path=jpg)
