# TinyEye User Guide

## Where to start

| I want to... | Section |
|---|---|
| Import a JPEG | [Layer A](#layer-a--organism-eye) |
| Skip captions | [Belief](#belief) |
| Optionally pack a latent | [Layer B](#layer-b--desktop-packer) |

---

## Layer A — organism Eye

```bash
python tinyeye_encode.py pic.jpg --out memory/ --no-latent
python tinyeye_encode.py pic.jpg --out memory/ --no-latent --belief "A mug on a desk."
```

Watch has no camera — import files only.

---

## Belief

`MISS = ""`. Empty belief is correct when nobody supplied a sentence.
Do not write "a red cup" because the mean RGB looked red.

---

## Layer B — desktop packer

TAESD latent is optional extra. Memory is the JPEG + markdown.
