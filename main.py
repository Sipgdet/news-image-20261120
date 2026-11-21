"""news-image-20261120 entry.

A newspaper front page summing up Friday 20 November 2026, drawn by
compose.py (PIL, DejaVu fonts) and stored in this repository as entry.png.
This program's only job is to hand that image to the grader: it copies
entry.png to the output directory, byte for byte.

Deterministic: the same input bytes always produce the same output bytes.
No network, no clock, no randomness, no model calls.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = OUTPUT_DIR / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not SOURCE.is_file():
        print(f"missing image: {SOURCE}", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("source is not a PNG image", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(TARGET)
    if source_hash != target_hash:
        print("copy mismatch: output differs from source", file=sys.stderr)
        return 1
    size = TARGET.stat().st_size
    if size > 1048576:
        print(f"entry over the 1 MiB cap: {size} bytes", file=sys.stderr)
        return 1
    print(f"wrote {TARGET} ({size} bytes, sha256 {target_hash[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
