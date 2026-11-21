#!/usr/bin/env python3
"""make.fun entry runner for news-image-20261120.

Copies entry.png byte-for-byte into $MAKEFUN_OUTPUT_DIR (default /output),
verifies the copy is identical, prints OK. Standard library only, no network.
This runner copies the finished front page to the make.fun output directory.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
CHUNK = 1 << 20


def digest(path: str) -> tuple[int, str]:
    """Return (size, sha256) for a file, read in chunks."""
    h = hashlib.sha256()
    size = 0
    with open(path, "rb") as fh:
        while True:
            block = fh.read(CHUNK)
            if not block:
                break
            size += len(block)
            h.update(block)
    return size, h.hexdigest()


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, ENTRY_NAME)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    target = os.path.join(output_dir, ENTRY_NAME)

    if not os.path.isfile(source):
        print("ERROR: missing source %s" % source, file=sys.stderr)
        return 1

    try:
        os.makedirs(output_dir, exist_ok=True)
        # copyfile only copies bytes; the size/sha256 read-back below is what
        # proves the copy is byte-identical to the source.
        shutil.copyfile(source, target)
    except OSError as exc:
        print("ERROR: could not write %s: %s" % (target, exc), file=sys.stderr)
        return 1

    try:
        source_size, source_sha = digest(source)
        target_size, target_sha = digest(target)
    except OSError as exc:
        print("ERROR: could not read back copy: %s" % exc, file=sys.stderr)
        return 1

    if source_size != target_size or source_sha != target_sha:
        print(
            "ERROR: copy is not byte-identical (size %d vs %d)" % (source_size, target_size),
            file=sys.stderr,
        )
        return 1

    print("OK %s %d bytes sha256=%s" % (target, target_size, target_sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
