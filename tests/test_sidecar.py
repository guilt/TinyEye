from pathlib import Path

from tinyeye.fixtures import write_mug, write_swatch
from tinyeye.images import collect_images, image_stats
from tinyeye.sidecar import parse_eye, write_eye_pair


def test_empty_belief(tmp_path: Path):
    jpg = tmp_path / "pic.jpg"
    jpg.write_bytes(b"not-really-jpeg")
    dest, md = write_eye_pair(jpg, tmp_path / "out", belief="")
    text = md.read_text(encoding="utf-8")
    assert dest.name.endswith(".eye.jpg")
    assert "belief_ok: false" in text


def test_human_belief(tmp_path: Path):
    jpg = tmp_path / "pic.jpg"
    jpg.write_bytes(b"x")
    _, md = write_eye_pair(jpg, tmp_path / "out", belief="A mug on a desk.", source="hand")
    text = md.read_text(encoding="utf-8")
    assert "belief_ok: true" in text and "A mug on a desk." in text
    sc = parse_eye(md)
    assert sc.belief_ok and sc.belief == "A mug on a desk."


def test_stats_not_caption(tmp_path: Path):
    jpg = write_swatch(tmp_path / "red.jpg", color=(200, 10, 10))
    stats = image_stats(jpg)
    assert stats.get("width") == 64
    assert "caption" not in stats
    _, md = write_eye_pair(jpg, tmp_path / "out", belief="", stats=stats)
    text = md.read_text(encoding="utf-8")
    assert "belief_ok: false" in text
    assert "width: 64" in text


def test_collect_images(tmp_path: Path):
    a = write_mug(tmp_path / "a.jpg")
    write_swatch(tmp_path / "nested" / "b.png", color=(10, 10, 180))
    found = collect_images([a], directory=tmp_path)
    assert len(found) >= 2


def test_compat_shim(tmp_path: Path):
    from tinyeye_sidecar import write_eye_pair as shim

    jpg = tmp_path / "x.jpg"
    jpg.write_bytes(b"x")
    dest, md = shim(jpg, tmp_path / "o", belief="ok")
    assert dest.exists() and md.exists()
