from pathlib import Path
from tinyeye.fixtures import write_mug

dest = Path(__file__).resolve().parent / "mug.jpg"
write_mug(dest)
print(dest)
