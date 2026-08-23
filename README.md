# tinyeye

**Offline batch image → latent encoder**  
CPU-first • no large VRAM • human-visualizable memory

This is the starter implementation of the idea from the X thread by @_vkaku:

> “I need a way given an image, just offline write it to latents quickly and in a batch mode, without requiring to load large ish models into VRAM.  
> Plus, a memory should be easy to visualize by humans too (think of it as .py / .pyc).”

## What it does

1. Takes ordinary JPEG / PNG / WebP files.
2. Encodes them with **TAESD** (Tiny AutoEncoder for Stable Diffusion, ~1.2 M params).
3. Writes two artifacts per image:

| File | Purpose | Analogy |
|------|---------|---------|
| `*.latent.png` | 4-channel quantized latent any image viewer can open | `.py` (human inspectable) |
| `*.latent.pt`  | Full float latent ready for models | `.pyc` (machine ready) |

## Quick start

```bash
git clone https://github.com/guilt/tinyeye.git
cd tinyeye
pip install -r requirements.txt
./download_weights.sh          # ~9.4 MB total
python tinyeye_encode.py yourphoto.jpg --out ./memory
```

Or whole folders:

```bash
python tinyeye_encode.py --dir ~/Pictures --out ./latents
```

Force CPU (default) or prefer GPU:

```bash
python tinyeye_encode.py *.jpg --cpu
python tinyeye_encode.py *.jpg --gpu
```

## Why this exists

- Full SD / Flux VAEs are 80–300 MB+ and want VRAM.
- TAESD is tiny, runs happily on CPU, and is already good enough for many “memory store” and preview workflows.
- The dual output (PNG + .pt) makes the latent library both **human-checkable** and **model-usable**.

## Roadmap (the real tinyeye)

- Better LVQ / entropy-aware formats that keep sharpness where it matters
- Even smaller / faster on-the-fly encoders
- A proper filesystem / memory store that lives in latent space
- Live adapter (LoRA-style) on top of the store
- Skip-hop path: ultra-fast image → compact token when full latent isn’t needed

This is the minimal working seed.

## License

TAESD weights & architecture: [madebyollin/taesd](https://github.com/madebyollin/taesd)  
This wrapper: public domain / do whatever you want.
