from pathlib import Path
dest = Path(__file__).resolve().parent / "mug.jpg"
try:
    from PIL import Image
    Image.new("RGB", (64, 64), (180, 40, 40)).save(dest, quality=85)
except Exception:
    dest.write_bytes(bytes.fromhex(
        "ffd8ffe000104a46494600010100000100010000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333432ffc0000b080001000101011100ffda0008000100013f00fb94a28a2803ffd9"
    ))
print(dest)
