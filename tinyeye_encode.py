#!/usr/bin/env python3
"""
tinyeye - offline batch JPEG/PNG to latent encoder + organism sidecar.
CPU-first, no large VRAM required.

Always writes:
  stem.eye.jpg + stem.eye.md     # memory (.py)
Optional extras:
  stem.latent.png + stem.latent.pt   # latent (.pyc)

Usage:
  python tinyeye_encode.py pic.jpg --out memory/
  python tinyeye_encode.py pic.jpg --out memory/ --belief "A mug on a desk."
  python tinyeye_encode.py pic.jpg --out memory/ --no-latent
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tinyeye_sidecar import write_eye_pair


def collect_images(paths, directory):
    exts = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    files = []
    if directory:
        d = Path(directory)
        for p in sorted(d.rglob("*")):
            if p.suffix.lower() in exts and p.is_file():
                files.append(p)
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() in exts:
            files.append(path)
        elif path.is_dir():
            for q in sorted(path.rglob("*")):
                if q.suffix.lower() in exts and q.is_file():
                    files.append(q)
    seen = set()
    unique = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def encode_latents(img_path: Path, out_dir: Path, stem: str, prefer_gpu: bool) -> bool:
    try:
        import torch
        import torchvision.transforms.functional as TF
        from PIL import Image

        from taesd import TAESD
    except ImportError as e:
        print(f"  skip latent (import): {e}")
        return False

    if prefer_gpu and torch.cuda.is_available():
        device = torch.device("cuda")
    elif prefer_gpu and getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    here = Path(__file__).resolve().parent
    enc = here / "taesd_encoder.pth"
    dec = here / "taesd_decoder.pth"
    if not enc.exists() or not dec.exists():
        print("  skip latent: missing TAESD weights (run ./download_weights.sh)")
        return False

    model = TAESD(encoder_path=str(enc), decoder_path=str(dec))
    model.eval()
    model.to(device)
    img = Image.open(img_path).convert("RGB")
    x = TF.to_tensor(img).unsqueeze(0).to(device)
    with torch.no_grad():
        latent = model.encoder(x)
        quant = model.scale_latents(latent).mul_(255).round_().byte()
    quant_path = out_dir / f"{stem}.latent.png"
    TF.to_pil_image(quant[0].cpu()).save(quant_path)
    print(f"  visual  -> {quant_path}")
    pt_path = out_dir / f"{stem}.latent.pt"
    torch.save(
        {
            "latent": latent.cpu().squeeze(0).contiguous(),
            "format": "tinyeye-taesd-v1",
            "note": "raw TAESD encoder output; decode with TAESD or compatible VAE",
        },
        pt_path,
    )
    print(f"  model   -> {pt_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="tinyeye - organism eye pair + optional TAESD latent"
    )
    parser.add_argument("images", nargs="*", help="Image files or directories")
    parser.add_argument("--dir", "-d", help="Directory to scan for images")
    parser.add_argument("--out", "-o", default="./memory", help="Output directory")
    parser.add_argument("--belief", default="", help="Human belief text (may be empty)")
    parser.add_argument("--source", default="import", help="source field in sidecar")
    parser.add_argument("--no-latent", action="store_true", help="Skip TAESD extras")
    parser.add_argument("--gpu", action="store_true", help="Prefer GPU/MPS if available")
    args = parser.parse_args()

    if not args.images and not args.dir:
        parser.print_help()
        print("\nExample: python tinyeye_encode.py pic.jpg --out memory/")
        sys.exit(1)

    files = collect_images(args.images, args.dir)
    if not files:
        print("No images found.")
        sys.exit(1)

    out_dir = Path(args.out)
    print(f"Eye pairs {len(files)} image(s) -> {out_dir}\n")

    for i, img_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {img_path.name}")
        try:
            latent_ok = False
            if not args.no_latent:
                latent_ok = encode_latents(img_path, out_dir, img_path.stem, args.gpu)
            write_eye_pair(
                img_path,
                out_dir,
                belief=args.belief,
                source=args.source,
                latent_ok=latent_ok,
            )
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nJPEG + md is memory. Latent is extra. TinyToT indexes md only.")


if __name__ == "__main__":
    main()
