#!/usr/bin/env python3
"""Build script for the Free Chess Scoresheet Pack.

Renders every HTML sheet in src/sheets/ to an unbranded PDF in printables/,
using WeasyPrint (local, no network, no signups).

Usage:
    python3 build.py            # build all sheets into printables/
    python3 build.py --outdir DIR
    python3 build.py --clean
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
SHEETS_DIR = ROOT / "src" / "sheets"
DEFAULT_OUTDIR = ROOT / "printables"


def sheet_order() -> list[Path]:
    """All sheet sources, sorted so numbered files keep their order."""
    files = sorted(SHEETS_DIR.glob("*.html"))
    if not files:
        raise SystemExit(f"No HTML sheets found in {SHEETS_DIR}")
    return files


def build_all(outdir: Path) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    built: list[Path] = []
    for src in sheet_order():
        dest = outdir / (src.stem + ".pdf")
        HTML(filename=str(src)).write_pdf(str(dest))
        size_kb = dest.stat().st_size / 1024
        print(f"  built {dest.name} ({size_kb:.0f} KB)")
        built.append(dest)
    return built


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build printable chess PDFs from HTML sheets.")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR,
                        help="Output directory (default: printables/)")
    parser.add_argument("--clean", action="store_true",
                        help="Remove the output directory before building")
    args = parser.parse_args(argv)

    if args.clean and args.outdir.exists():
        shutil.rmtree(args.outdir)

    print(f"Building chess scoresheet pack sheets -> {args.outdir}")
    built = build_all(args.outdir)
    print(f"Done: {len(built)} PDF(s) built.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
