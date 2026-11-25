#!/usr/bin/env python3
"""Wednesday 25 November 2026 front page — entry program (v3).

Standard library only. The finished page ships in this repository as
entry.png; this program checks it and places an exact copy at
MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when the variable
is unset). It never draws, never fetches, never writes a timestamp,
so running it twice yields the same bytes twice.
"""
import hashlib
import os
import struct
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
BUNDLED = os.path.join(BASE, "entry.png")
LIMIT = 1024 * 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def load_image():
    """Read and validate the bundled page; exit loudly if it is wrong."""
    try:
        with open(BUNDLED, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        sys.exit(f"cannot read bundled entry.png: {exc}")
    if blob[:8] != MAGIC:
        sys.exit("bundled entry.png is not a PNG file")
    if len(blob) > LIMIT:
        sys.exit(f"bundled entry.png is {len(blob)} bytes, over the 1 MiB limit")
    width, height = struct.unpack(">II", blob[16:24])
    if (width, height) != (1024, 1024):
        sys.exit(f"bundled entry.png is {width}x{height}, expected 1024x1024")
    return blob


def pick_destination():
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if os.path.isdir(wanted) and os.access(wanted, os.W_OK):
        return os.path.join(wanted, "entry.png")
    fallback = os.path.join(BASE, "entry.png")
    if fallback == BUNDLED:
        return None
    return fallback


def run():
    blob = load_image()
    target = pick_destination()
    if target is None:
        sys.exit("no writable output directory for entry.png")
    # Byte-exact copy: the file the judge sees is the file in the repo.
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        again = handle.read()
    if again != blob:
        sys.exit("entry.png on disk does not match the validated bytes")
    digest = hashlib.sha256(blob).hexdigest()
    print(f"wrote {target}: {len(blob)} bytes, sha256 {digest}")


if __name__ == "__main__":
    run()
