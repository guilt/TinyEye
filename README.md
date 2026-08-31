# tinyeye

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Layer A — organism Eye.** Any JPEG from phone / USB / laptop → `stem.eye.jpg` + `stem.eye.md`. Belief may be human-written or empty (`belief_ok: false` → TinyToT miss on “what’s in the picture”). Do not hallucinate a caption. The watch has **no camera**. Import only.

**Layer B — desktop packer.** TAESD ~1.2M params, CPU. Optional `*.latent.png` + `*.latent.pt`. Latent is `.pyc`. JPEG + md is `.py`.

```bash
python tinyeye_encode.py pic.jpg --out memory/
ls memory/*eye.jpg memory/*eye.md
# optional latent png opens in an image viewer
# POST tinytot reload — "what do you see?" uses Belief or misses
```

Empty belief is honest. Watch Eye is import only.
