"""Offline visual dataset: 4 colored squares. No captions invented."""
from pathlib import Path
from tinyeye.fixtures import write_swatch
from tinyeye.sidecar import write_eye_pair
from tinyeye.images import image_stats

OUT = Path(__file__).resolve().parent / "out" / "swatches"
SWATCHES = {
    "red-mug-standin": ((180, 40, 40), "A red square standing in for a mug."),
    "desk-wood": ((140, 90, 40), "A brown square standing in for a desk."),
    "sky": ((70, 130, 200), ""),
    "leaf": ((40, 140, 60), ""),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (color, belief) in SWATCHES.items():
        jpg = write_swatch(OUT / f"{name}.jpg", color=color)
        write_eye_pair(jpg, OUT, belief=belief, source="fixture", stats=image_stats(jpg))
    print(OUT)


if __name__ == "__main__":
    main()
