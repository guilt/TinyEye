# tinyeye

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Layer A — organism Eye.** JPEG → `stem.eye.jpg` + `stem.eye.md`. Belief may be empty. Do not hallucinate a caption. Watch has **no camera**.

**Layer B — desktop packer.** Optional TAESD latent. Latent is `.pyc`. JPEG + md is `.py`.

```bash
python -m pip install -e ".[dev]"
# or: pipenv install --dev
# family consumers, until PyPI:
#   pip install "tinyeye @ git+https://github.com/guilt/tinyeye.git@bananey"
make tests
make examples
python tinyeye_encode.py examples/mug.jpg --out memory/ --no-latent --belief "A mug on a desk."
```

Sidecars may include width/height/mean RGB. Those are measurements, not captions.
