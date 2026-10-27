# Free Chess Scoresheet Pack

A free, printable pack for keeping a chess paper trail. Regulation-style
scoresheets, opening-log cards, a post-game "what happened" reflection sheet,
lesson-notes pages, clock-settings cards, and a puzzle-drill booklet with an
answer key — all plain HTML/CSS that builds to clean, unbranded PDFs with one
local script. No accounts, no signups, no tracking — download, print, and keep
score like a club regular.

## What's in the pack

Six sheets, each PDF opening with a friendly one-page "getting started" guide
followed by the printable:

| # | Sheet | What it's for |
|---|-------|---------------|
| 1 | Regulation-Style Scoresheet | Event/date/round header, names and ratings, 60 numbered move pairs, result and signatures |
| 2 | Opening Log Cards | Four cut-out cards: one opening per card — main line, plan, the trap, and a keep/tweak/bench verdict |
| 3 | Post-Game Reflection | The what-happened sheet: turning points, what decided it, clock report, one drill for next time |
| 4 | Lesson Notes | Topic, key ideas, example lines, assigned drills with due dates, questions for next time |
| 5 | Clock Settings Cards | Six preset cards (90+30 down to 1+0) plus four blank ones — with space to write your own clock's steps |
| 6 | Puzzle Drill Booklet | Six original starter drills (mate-in-one, verified), blank drill pages for your own puzzles, a session log, and an honest answer key |

Every sheet is large-print-friendly (12pt guide text, generous writing space)
and carries a **pencils only — no pens near the board** note. The starter
puzzles in the booklet were composed for this pack; the test suite verifies
each one is a legal position with exactly one mating move.

Prebuilt PDFs live in [`printables/`](printables/). They're unbranded — no
names, logos, or links — so they're ready to print, share, or include in a
project as-is.

## How to build it yourself

Requirements: Python 3.10+ and [WeasyPrint](https://weasyprint.org/) (plus
pypdf, pytest, and optionally python-chess for the tests).

```bash
pip install weasyprint pypdf pytest python-chess

python3 build.py          # build all sheets into printables/
python3 build.py --clean  # wipe printables/ first, then build
python3 build.py --outdir /tmp/somewhere
```

Each sheet is a plain HTML file in `src/sheets/` sharing one stylesheet,
`src/styles.css`. Edit any sheet, rerun the script, done.

## Running the tests

```bash
python3 -m pytest tests/ -q
```

The tests verify that every sheet builds a valid letter-sized PDF with a
getting-started page and the pencils-only note, that the prebuilt PDFs in
`printables/` parse and stay unbranded, that the build script runs cleanly,
and — using python-chess — that each of the six starter puzzles has exactly
one mate-in-one, matching the printed answer key. (Without python-chess those
specific tests skip gracefully.)

## Who this is for

Anyone at the board who wants their games on paper: club players keeping a
record, improvers logging their openings and lessons, coaches assigning
homework. Nothing here needs an app or an account — though it pairs nicely
with puzzle books and a chess clock whatever brand it may be. Built with a
beginner's pace in mind: plain instructions, generous writing space, and a
pencil in hand.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC. This pack is a free, beginner-friendly
tool published by Asdale Dynamics, LLC, which makes plain-English AI books,
guides, and practical open-source tools.
