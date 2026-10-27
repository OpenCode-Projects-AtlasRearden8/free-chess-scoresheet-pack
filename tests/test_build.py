"""Tests for the Free Chess Scoresheet Pack.

Verifies that every sheet builds a valid PDF, that the committed printables/
output is present, valid, and unbranded, that each sheet carries the
pencils-only note, and that the six original starter puzzles in the booklet
are exactly what the answer key claims: legal positions with a unique
mate-in-one for White.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SHEETS_DIR = ROOT / "src" / "sheets"
STYLES = ROOT / "src" / "styles.css"
PRINTABLES_DIR = ROOT / "printables"
BUILD_SCRIPT = ROOT / "build.py"

EXPECTED_SHEETS = [
    "01-regulation-scoresheet",
    "02-opening-log-cards",
    "03-post-game-reflection",
    "04-lesson-notes",
    "05-clock-settings-cards",
    "06-puzzle-drill-booklet",
]

# One distinctive phrase per sheet, so a bad edit that guts a sheet's content
# is caught even if the PDF still builds.
SHEET_SIGNATURES = {
    "01-regulation-scoresheet": "Scoresheet",
    "02-opening-log-cards": "Opening Log Card",
    "03-post-game-reflection": "Turning point",
    "04-lesson-notes": " homework",
    "05-clock-settings-cards": "increment",
    "06-puzzle-drill-booklet": "Answer key",
}


def sheet_sources() -> list[Path]:
    return sorted(SHEETS_DIR.glob("*.html"))


def build_into(outdir: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT), "--outdir", str(outdir)],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


# --------------------------------------------------------------------------
# Sources and build script
# --------------------------------------------------------------------------

def test_all_expected_sheets_exist():
    for name in EXPECTED_SHEETS:
        assert (SHEETS_DIR / f"{name}.html").is_file(), f"missing source: {name}.html"


def test_shared_stylesheet_exists_and_is_referenced():
    assert STYLES.is_file()
    for name in EXPECTED_SHEETS:
        html = (SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
        assert 'href="../styles.css"' in html, f"{name}.html does not link the shared stylesheet"


def test_sheet_content_is_intact():
    for name, phrase in SHEET_SIGNATURES.items():
        html = (SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
        assert phrase in html, f"{name}.html is missing its signature phrase: {phrase!r}"


@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_every_sheet_has_getting_started_page(name):
    html = (SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
    assert 'class="getting-started"' in html, f"{name}.html lacks a getting-started page"
    assert "How to use it" in html


@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_every_sheet_carries_the_pencils_note(name):
    html = (SHEETS_DIR / f"{name}.html").read_text(encoding="utf-8")
    assert "Pencils only" in html, f"{name}.html lacks the pencils-only note"


def test_build_script_runs_clean(tmp_path):
    outdir = tmp_path / "out"
    build_into(outdir)
    pdfs = sorted(outdir.glob("*.pdf"))
    assert len(pdfs) == len(sheet_sources()) >= len(EXPECTED_SHEETS)


# --------------------------------------------------------------------------
# Built PDFs
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_every_sheet_builds_valid_pdf(tmp_path, name):
    """Each sheet builds a valid, non-empty, letter-sized multi-page PDF."""
    outdir = tmp_path / "out"
    build_into(outdir)

    pdf_path = outdir / f"{name}.pdf"
    assert pdf_path.is_file(), f"{name}.pdf was not built"
    assert pdf_path.stat().st_size > 1000, f"{name}.pdf is suspiciously small"

    reader = PdfReader(str(pdf_path))
    assert len(reader.pages) >= 2, f"{name}.pdf should have a guide page plus the sheet"
    for page in reader.pages:
        box = page.mediabox
        width_in = float(box.width) * 0.0138889  # points -> inches
        height_in = float(box.height) * 0.0138889
        assert abs(width_in - 8.5) < 0.1 and abs(height_in - 11.0) < 0.1, (
            f"{name}.pdf page is {width_in:.2f}x{height_in:.2f}in, expected letter"
        )
        assert page.extract_text(), f"{name}.pdf page has no extractable text"


@pytest.mark.parametrize("name", EXPECTED_SHEETS)
def test_built_pdf_carries_the_pencils_note(tmp_path, name):
    outdir = tmp_path / "out"
    build_into(outdir)
    reader = PdfReader(str(outdir / f"{name}.pdf"))
    text = " ".join(p.extract_text() or "" for p in reader.pages)
    assert "Pencils only" in text, f"{name}.pdf text lacks the pencils-only note"


# --------------------------------------------------------------------------
# Committed printables/
# --------------------------------------------------------------------------

def test_committed_printables_are_valid():
    for name in EXPECTED_SHEETS:
        pdf_path = PRINTABLES_DIR / f"{name}.pdf"
        assert pdf_path.is_file(), f"missing prebuilt PDF: printables/{name}.pdf"
        assert pdf_path.stat().st_size > 1000
        reader = PdfReader(str(pdf_path))
        assert len(reader.pages) >= 2
        for page in reader.pages:
            assert page.extract_text(), f"{pdf_path.name} has a page with no extractable text"


def test_pdfs_are_unbranded():
    """No branding: no names, company names, or URLs inside the PDFs."""
    forbidden = ["asdale", "dylan", "http://", "https://", "www.", ".com"]
    for pdf_path in sorted(PRINTABLES_DIR.glob("*.pdf")):
        text = " ".join(
            page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages
        ).lower()
        for token in forbidden:
            assert token not in text, f"{pdf_path.name} contains forbidden token: {token}"


# --------------------------------------------------------------------------
# The booklet's starter puzzles (python-chess, if available)
# --------------------------------------------------------------------------

FEN_RE = re.compile(r'data-fen="([^"]+)"\s+data-solution="([^"]+)"')


def booklet_puzzles() -> list[tuple[str, str]]:
    html = (SHEETS_DIR / "06-puzzle-drill-booklet.html").read_text(encoding="utf-8")
    return FEN_RE.findall(html)


def test_booklet_declares_six_puzzles():
    puzzles = booklet_puzzles()
    assert len(puzzles) >= 6, "booklet should embed six starter puzzles"


try:
    import chess as _chess  # noqa: F401
    HAS_CHESS = True
except ImportError:  # pragma: no cover
    HAS_CHESS = False


@pytest.mark.skipif(not HAS_CHESS, reason="python-chess is not installed")
@pytest.mark.parametrize("fen,solution", booklet_puzzles())
def test_starter_puzzle_is_a_unique_mate_in_one(fen, solution):
    """Every starter puzzle: legal position, and the key move is the ONLY mate."""
    board = _chess.Board(fen)
    assert board.is_valid(), f"illegal position: {fen}"
    assert not board.is_check(), f"{fen} already has the black king in check"
    assert board.turn == _chess.WHITE, f"{fen} is not White to move"

    mates = []
    for mv in board.legal_moves:
        board.push(mv)
        if board.is_checkmate():
            mates.append(mv)
        board.pop()

    assert len(mates) == 1, f"{fen} has {len(mates)} mating moves, expected exactly one"
    assert board.san(mates[0]) == solution, (
        f"{fen}: printed key says {solution!r}, but the (unique) mate is "
        f"{board.san(mates[0])!r}"
    )


@pytest.mark.skipif(not HAS_CHESS, reason="python-chess is not installed")
@pytest.mark.parametrize("fen,solution", booklet_puzzles())
def test_answer_key_lists_every_solution(fen, solution):
    html = (SHEETS_DIR / "06-puzzle-drill-booklet.html").read_text(encoding="utf-8")
    assert solution in html, f"answer key does not list {solution!r}"
    fen_only = fen.split()[0]
    assert fen_only in html, f"answer key / booklet does not print FEN {fen_only!r}"
