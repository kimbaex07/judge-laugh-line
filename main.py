#!/usr/bin/env python3
"""Write the entry one-liner to $MAKEFUN_OUTPUT_DIR/entry.txt.

Reads entry.txt next to this script, validates the gate (1-200 characters,
not whitespace-only, a single line), and writes the exact bytes to the
output directory. Pure Python standard library only.
"""

import os
import sys
from pathlib import Path

ENTRY_NAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / ENTRY_NAME
    text = source.read_text(encoding="utf-8")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        print(
            f"entry.txt must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(text)}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("entry.txt must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry.txt must be a single line", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / ENTRY_NAME
    out_path.write_bytes(text.encode("utf-8"))
    os.chmod(out_path, 0o644)
    print(f"wrote {out_path} ({len(text)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
