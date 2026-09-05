# HOW_TO_VERIFY — tinyeye

```bash
python -m pip install -e ".[dev]"
make tests
make examples
ls examples/out/*eye.jpg examples/out/*eye.md
```

Expect:

- `examples/out/mug.eye.md` has `belief_ok: true` and the supplied sentence
- `examples/out/swatches/sky.eye.md` has `belief_ok: false` and an empty Belief
- no sidecar contains an invented object name
- latent files are absent when `--no-latent` is used

Belief may be empty. Do not invent a caption. Latent is optional extra.
