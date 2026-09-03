# Architecture

```{mermaid}
flowchart LR
    JPEG[JPEG / PNG] --> Enc[tinyeye_encode]
    Enc --> Pair["stem.eye.jpg + stem.eye.md"]
    Enc -.->|optional| Lat[TAESD latent]
    Pair --> Tiny["/tiny/eye/"]
```
