# TinyEye datasets

Watch has **no camera**. Files are imported.

| set | what | belief |
|-----|------|--------|
| `examples/mug.jpg` | 64×64 red square (PIL) or a 1×1 JPEG fallback | supplied by you |
| `examples/out/swatches/` | 4 colored squares | two labelled, two empty on purpose |
| TAESD latent | optional desktop extra, needs weights | never a substitute for md |

Empty belief stays empty. TinyEye will not write "a mug" because the pixels are red.
