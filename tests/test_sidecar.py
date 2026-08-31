from pathlib import Path
from tinyeye_sidecar import write_eye_pair

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
