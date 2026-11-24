#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261123 bounty.

The entry image (entry.png, a one-page drawn summary of the world news
of Monday 23 November 2026, produced by draw.py) is committed beside
this file; the program copies it to the grader's output path. It uses
only the standard library, touches no network, and writes the same
bytes on every run.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.png")


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing beside main.py")
    dest = output_path()
    shutil.copyfile(SOURCE, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")


if __name__ == "__main__":
    main()
