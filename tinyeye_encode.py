#!/usr/bin/env python3
"""
tinyeye - offline batch JPEG/PNG to latent encoder
CPU-first, no large VRAM required.

Uses TAESD (Tiny AutoEncoder for Stable Diffusion) as the starter encoder.
Produces:
  1. Quantized latent PNG  - human-visualizable "source" form (like .py)
  2. Full float .pt         - model-ready latent (like .pyc)

Usage:
  python tinyeye_encode.py image1.jpg image2.png ...
  python tinyeye_encode.py --dir ./photos --out ./latents
  python tinyeye_encode.py --help
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
import torchvision.transforms.functional as TF
from PIL import Image

from taesd import TAESD


def get_device(prefer_cpu: bool = True) -> torch.device:
    if prefer_cpu:
        return torch.device("cpu")
    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def load_taesd(device: torch.device) -> TAESD:
    here = Path(__file__).resolve().parent
    enc = here / "taesd_encoder.pth"
    dec = here / "taesd_decoder.pth"
    if not enc.exists() or not dec.exists():
        raise FileNotFoundError(
            f"Missing TAESD weights. Run ./download_weights.sh first.\n"
            f"Expected files in {here}"
        )
    model = TAESD(encoder_path=str(enc), decoder_path=str(dec))
    model.eval()
    model.to(device)
    return model


@torch.no_grad()
def encode_image(model: TAESD, img_path: Path, device: torch.device):
    """Return (raw_latent NCHW float, quantized_u8 CHW)"""
    img = Image.open(img_path).convert("RGB")
    x = TF.to_tensor(img).unsqueeze(0).to(device)
    latent = model.encoder(x)
    quant = model.scale_latents(latent).mul_(255).round_().byte()
    return latent.cpu(), quant[0].cpu()


def save_outputs(latent, quant, stem, out_dir, save_quant_png=True, save_pt=True):
    out_dir.mkdir(parents=True, exist_ok=True)
    if save_quant_png:
        quant_path = out_dir / f"{stem}.latent.png"
        TF.to_pil_image(quant).save(quant_path)
        print(f"  visual  -> {quant_path}")
    if save_pt:
        pt_path = out_dir / f"{stem}.latent.pt"
        torch.save(
            {
                "latent": latent.squeeze(0).contiguous(),
                "format": "tinyeye-taesd-v1",
                "note": "raw TAESD encoder output; decode with TAESD or compatible VAE",
            },
            pt_path,
        )
        print(f"  model   -> {pt_path}")


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


def main():
    parser = argparse.ArgumentParser(
        description="tinyeye - offline batch image to latent encoder (CPU-first, TAESD starter)"
    )
    parser.add_argument("images", nargs="*", help="Image files or directories")
    parser.add_argument("--dir", "-d", help="Directory to scan for images")
    parser.add_argument("--out", "-o", default="./latents", help="Output directory")
    parser.add_argument("--cpu", action="store_true", default=True, help="Force CPU (default)")
    parser.add_argument("--gpu", action="store_true", help="Prefer GPU/MPS if available")
    parser.add_argument("--no-png", action="store_true", help="Skip quantized PNG output")
    parser.add_argument("--no-pt", action="store_true", help="Skip .pt output")
    args = parser.parse_args()

    if not args.images and not args.dir:
        parser.print_help()
        print("\nExample: python tinyeye_encode.py photo.jpg --out ./memory")
        sys.exit(1)

    device = get_device(prefer_cpu=not args.gpu)
    print(f"Device: {device}")

    model = load_taesd(device)
    print("TAESD loaded (~1.2 M params encoder)")

    files = collect_images(args.images, args.dir)
    if not files:
        print("No images found.")
        sys.exit(1)

    out_dir = Path(args.out)
    print(f"Encoding {len(files)} image(s) -> {out_dir}\n")

    for i, img_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {img_path.name}")
        try:
            latent, quant = encode_image(model, img_path, device)
            save_outputs(
                latent, quant, stem=img_path.stem, out_dir=out_dir,
                save_quant_png=not args.no_png, save_pt=not args.no_pt,
            )
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nDone. The .latent.png files are human-inspectable; .latent.pt are model-ready.")
    print("This is the starter for tinyeye - better formats & on-the-fly encoders next.")


if __name__ == "__main__":
    main()
