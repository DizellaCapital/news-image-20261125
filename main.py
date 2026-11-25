#!/usr/bin/env python3
"""Entry point for the Wednesday 25 November 2026 front page (v3).

Stdlib only, no network. The artwork itself is produced by render.py
(Pillow, run locally at build time) and shipped as entry.png next to
this file; this script only verifies that shipped PNG and copies it to
the output directory the grader provides.

Usage:  python3 main.py            (writes ./output/entry.png)
        MAKEFUN_OUTPUT_DIR=/x python3 main.py   (writes /x/entry.png)

The copy is byte-for-byte identical to the shipped entry.png, so the
output is fully deterministic across runs and machines.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1 * 1024 * 1024
EXPECTED_SIZE = (1024, 1024)


def read_png_size(path):
    """Parse width/height out of a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk: %s" % path)
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(SOURCE):
        print("missing shipped artwork: %s" % SOURCE, file=sys.stderr)
        return 1

    size = read_png_size(SOURCE)
    if size != EXPECTED_SIZE:
        print("bad PNG size %s, expected %s" % (size, EXPECTED_SIZE),
              file=sys.stderr)
        return 1
    nbytes = os.path.getsize(SOURCE)
    if nbytes > MAX_BYTES:
        print("PNG too large: %d bytes > %d" % (nbytes, MAX_BYTES),
              file=sys.stderr)
        return 1

    shutil.copyfile(SOURCE, target)
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (target, size[0], size[1], nbytes, sha256_of(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
