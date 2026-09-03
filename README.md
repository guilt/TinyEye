# TinyEye — Borrowed Eyes for Tiny

[![GitHub](https://img.shields.io/badge/GitHub-guilt/TinyEye-181717?logo=github)](https://github.com/guilt/TinyEye)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![docs](https://img.shields.io/badge/docs-USER_GUIDE-0A66C2)](docs/USER_GUIDE.md)

Tiny is a markdown cache that can grow ears, a mouth, and borrowed eyes. If a sense is missing it says so. Port 11434. Files you can delete.

**Layer A — organism Eye.** JPEG → `stem.eye.jpg` + `stem.eye.md`.
Belief may be empty. Do not hallucinate a caption. Watch has **no camera**.

**Layer B — desktop packer.** Optional TAESD latent. Latent is `.pyc`.
JPEG + md is `.py`.

```bash
python -m pip install -e ".[dev]"
make tests && make examples
python tinyeye_encode.py examples/mug.jpg --out memory/ --no-latent --belief "A mug on a desk."
```

## The core idea

Width, height, and mean RGB are measurements. They are not a caption.
An empty `## Belief` is legal. An invented object name is not.

## Capabilities

| Feature | What it does |
|---|---|
| `write_eye_pair` | copy JPEG + write sidecar |
| Honest empty belief | `belief_ok: false`, blank `## Belief` |
| Measurements | optional width / height / mean RGB |
| `--no-latent` | skip TAESD; memory is still complete |
| Offline swatches | generated colors, no camera |

## Quick start

```bash
git clone https://github.com/guilt/TinyEye.git
cd TinyEye && git checkout bananey
python -m pip install -e ".[dev]"
make tests && make examples
```

Until PyPI: `pip install "tinyeye @ git+https://github.com/guilt/tinyeye.git@bananey"`

## Documentation

| I want to... | Page |
|---|---|
| Get running in 5 minutes | [Getting Started](docs/source/getting_started.md) |
| Understand the eye | [User Guide](docs/USER_GUIDE.md) |
| Write a sidecar | [How-To: Sidecar](docs/source/how_to/02_sidecar.md) |
| Keep belief empty | [How-To: Belief](docs/source/how_to/03_belief.md) |
| Look up a symbol | [API Reference](docs/source/api/README.md) |

## Development

```
make tests            pytest with coverage (gate ≥ 80%)
make fixtures         examples/mug.jpg
make dataset          4-swatch visual set
make examples         eye pairs without latent
make docs             regenerate API docs + Sphinx HTML
```

## Family

- [TinyToT](https://github.com/guilt/TinyToT) · [TinyHowl](https://github.com/guilt/TinyHowl) · [TinyEar](https://github.com/guilt/TinyEar) · [NanoToT](https://github.com/guilt/NanoToT)

## Links

- **GitHub**: [github.com/guilt/TinyEye](https://github.com/guilt/TinyEye)
- **Docs**: [USER_GUIDE](docs/USER_GUIDE.md) · [Getting started](docs/source/getting_started.md) · [API](docs/source/api/README.md)

## License

MIT — see [LICENSE.md](LICENSE.md).
