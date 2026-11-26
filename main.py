#!/usr/bin/env python3
"""make.fun entry — "Sum up 25 November's world news in one image".

Winner-template design (cream broadsheet: big date masthead, red
subline, region chips, UTC timeline, "The Day in Numbers" box, 13
numbered illustrated cards, an ALSO column, a dotted world map with
pins, and a DATE CHECK footer). Writes the bundled front-page image
to /output/entry.png. No network, no randomness, no clock: every run
writes exactly the same bytes.
"""
import filecmp
import os
import shutil
import struct
from pathlib import Path

# Gate limits from the competition rules: PNG, at most 1 MiB, at most 1024x1024.
MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_png(path: Path) -> None:
    """Refuse anything the gate would reject: not a PNG, over 1 MiB, or over 1024x1024."""
    data = path.read_bytes()
    if data[:8] != PNG_MAGIC:
        raise SystemExit(f"not a PNG file: {path}")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"image over 1 MiB: {len(data)} bytes")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"image over 1024x1024: {width}x{height}")


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "image.png"
    if not src.is_file():
        pngs = sorted(here.glob("*.png"))
        if len(pngs) == 1:
            src = pngs[0]
    if not src.is_file():
        raise SystemExit(f"bundled image not found: {src}")
    check_png(src)
    dst = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if not filecmp.cmp(src, dst, shallow=False):
        raise SystemExit("written file does not match the bundled image")
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
