# STATUS — Free Chess Scoresheet Pack

Last updated: 2026-10-27

## What was built

A complete, free printable pack for keeping a chess paper trail, built to the
original goal spec:

- **6 sheets**, each a plain HTML/CSS source in `src/sheets/` sharing
  `src/styles.css`:
  1. Regulation-Style Scoresheet (`01-regulation-scoresheet.html`) —
     event/round/board/date/section/time-control header, White and Black
     names + ratings, two-column 60-move grid, result checkboxes
     (1–0 / 0–1 / ½–½ / other), signatures, arbiter initials.
  2. Opening Log Cards (`02-opening-log-cards.html`) — four dashed cut-out
     cards: opening + ECO code, "sounds like" plan, main line, aim, trap to
     watch, W–D–L tally, keep/tweak/bench verdict.
  3. Post-Game Reflection (`03-post-game-reflection.html`) — the what-happened
     sheet: result and opponent strength, one-sentence summary, two turning
     points, "decided by" checklist, clock report, time-trouble question,
     proud-of and one-drill boxes, 1–5 feeling row.
  4. Lesson Notes (`04-lesson-notes.html`) — topic/date/source, three key
     ideas, four example-line slots, "where it clicked" box, five drill rows
     with due dates, questions for next time.
  5. Clock Settings Cards (`05-clock-settings-cards.html`) — six preset cards
     (90+30, 15+10, 10+5, 5+3, 3+2, 1+0) with plain-English increment/delay
     explainer pages, plus four blank "my preset" cards with mode checkboxes
     and the keep-it-real "Steps on my clock (my words)" lines.
  6. Puzzle Drill Booklet (`06-puzzle-drill-booklet.html`) — six original
     starter drills (all "White to move, mate in one", 8×8 unicode diagrams
     with correct square shading, FEN per position), four blank drill pages
     with sketch grids for the user's own puzzles, a 14-row session log, and
     a full answer key.
- **Friendly getting-started page per sheet**: each PDF opens with a
  one-page "How to use it" intro before the printable.
- **Pencils-only note on every sheet** — and inside every PDF (verified by
  tests, not just by intent).
- **Large-print-friendly**: 12pt body/guide text, 24pt headings, generous
  writing space throughout. The one deliberate exception is the scoresheet
  move grid (~14pt rows, matching regulation-blank tightness) — noted in the
  README.
- **One build script**: `build.py` renders all six HTML sheets via
  WeasyPrint into `printables/`. Supports `--outdir` and `--clean`. Uses a
  named CSS page (`@page scoresheet` with tighter margins) so all 60 move
  rows plus result/signature fit one page.
- **Unbranded PDFs:** no names, logos, or URLs in any output (enforced by a
  test that scans the extracted text of all six PDFs).
- **Original starter puzzles:** the six mate-in-one positions were composed
  for this pack (no outside puzzle copyright), and each is verified by the
  test suite using python-chess: valid position, White to move, not already
  in check, **exactly one** legal mating move, and it matches the printed
  answer key. The key also prints each FEN.
- **README.md** with sheet table, build/test instructions, and credit to
  Asdale Dynamics, LLC. **LICENSE** is MIT with the exact line
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- No secrets, no personal data, no network calls, no signups anywhere.

## How to run it

```bash
pip install weasyprint pypdf pytest python-chess   # one-time setup
python3 build.py                                  # build all PDFs into printables/
python3 build.py --clean                          # wipe and rebuild
python3 -m pytest tests/ -q                        # run the test suite
```

Requirements: Python 3.10+ (tested on 3.13), WeasyPrint (tested with 70.0),
pypdf/pytest for tests. python-chess is optional for tests — six puzzle tests
skip gracefully without it.

## Verification results

- `python3 build.py --clean` → **6/6 PDFs built** (26–54 KB), exit code 0.
- `python3 -m pytest tests/ -q` → **43 passed** in ~36 s:
  - all 6 expected sheet sources exist and link the shared stylesheet
  - each sheet's distinctive content phrase is present (catches gutting edits)
  - every sheet has a getting-started page and the pencils-only note
  - build script runs cleanly into a temp dir and produces 6 PDFs
  - each of the 6 sheets builds a valid PDF (≥2 pages, letter 8.5×11 in ±0.1,
    extractable text on every page, non-trivial size)
  - every built PDF carries the pencils-only note in its extracted text
  - all 6 committed `printables/` PDFs exist, parse, and have text
  - no forbidden branding tokens ("asdale", "dylan", "http(s)://", "www.",
    ".com") in any PDF's text
  - all 6 starter puzzles verify with python-chess: legal, not in check,
    White to move, exactly one mate-in-one, matching the printed key; the
    key table lists every solution
- `python3 -m py_compile build.py tests/test_build.py` → passes.
- Visual QA of layouts was done by rendering every page to PNG (pdftoppm)
  and inspecting: no orphan footnotes, no clipped tables, diagrams render on
  a correct checkerboard with chess glyphs (DejaVu Sans), cards cut along
  dashed borders cleanly. Pagination tuned so each sheet's printable part
  fits exactly: scoresheet 2 pages, cards 3, reflection 2, lesson 2, clock
  3, booklet 7.

## Known gaps / possible improvements

- US Letter only; an A4 variant needs a second `@page` rule or a build flag.
- The scoresheet grid holds 60 move pairs; longer games need a second sheet
  (the sheet says so itself). A second-page variant with more rows could be
  added.
- The booklet's blank drill pages use empty sketch grids rather than
  pre-printed coordinates; coordinate labels (a–h/1–8) would help absolute
  beginners sketch exact positions.
- Tests re-run the full build per parametrized case (~36 s total); a session
  fixture could share one build run for speed.
- Clock preset cards cover increment-style presets and one flat-sprint
  preset; a dedicated USCF-delay (e.g. "G/90 d5") preset row was left off
  the six-card page but fits the blank cards fine.
- Visual QA is by test assertions plus manual PNG inspection rather than a
  scripted screenshot-diff test.
