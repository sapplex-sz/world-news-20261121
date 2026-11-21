#!/usr/bin/env python3
"""Copy the finished news image to the grader output path.

Standard library only. Both runs write the same bytes.
"""

import os
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().parent / "news.png"


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.png"


def main() -> None:
    dest = output_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, dest)


if __name__ == "__main__":
    main()
