# UXLC-utils

Data and documentation around UXLC (the Unicode/XML Leningrad Codex), together with the **CLC**
(Charitable Leningrad Codex), a planned new edition built charitably on top of it — see
[`doc/clc-design.md`](doc/clc-design.md). **This repository contains no code.** As of 2026-08-03
all of its Python lives in the sibling repository
[MAM-basics](https://github.com/bdenckla/MAM-basics), under `py/`, and generates into this one.

## What is here

- `in/` — inputs: the canonical UXLC book XML (`in/UXLC-39`), the non-canonical members of
  tanach.us' `Tanach.xml` zip (`in/UXLC-rest`), the UXLC change logs and hand-curated tables
  (`in/UXLC-misc`, with corrected overrides in `in/UXLC-misc-fixed`), and every UXLC-coded note
  page for all 39 books (`in/UXLC-notes`).
- `out/` — generated JSON: the change-log derivatives under `out/UXLC-misc/`, plus
  `uxlc-words.json` and `uxlc-words-fragile.json`.
- `gh-pages/` — the generated static site (below).
- `data/` — generated lookup tables other repos consume, `lci_augrecs.json` and `lci_recs.json`.
- `doc/` — the CLC design document and its skeleton plan.

Two files are exceptions to the usual reading of those directory names.
`in/UXLC-misc/2026.04.01-map-to-book-of-job.json` lives under `in/` but is written by a program,
not by hand; `out/UXLC-misc/map-changes-to-book-of-job.md` lives under `out/` but is hand-authored
prose that no program writes.

## Regenerating it

From a clone of MAM-basics sitting beside this one, with that repo's own interpreter:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_uxlc_mega.py
```

then, because it is not one of that pipeline's five steps:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_clc.py
```

Together those cover all of `gh-pages/`, `out/` and `data/` that is generated at all. A third
generator, `main_map_changes_to_book_of_job.py`, writes the one tracked file under `in/` and needs
a `../book-of-job` clone. `CLAUDE.md` lists every entry point and says what each writes — including
the two downloaders, which as of 2026-08-03 cannot run because tanach.us' `robots.txt` disallows
the paths they fetch.

Regenerating should produce **no diff**. An unexplained one is a bug, in this repo's data or in
MAM-basics' code; that is how the real defects here have actually been found.

## GitHub Pages

The static site under `gh-pages/` is deployed by `.github/workflows/pages.yml`, which involves no
Python and is unaffected by the move. Published sections:

- `https://bdenckla.github.io/UXLC-utils/` — site root, `gh-pages/index.html`
- `https://bdenckla.github.io/UXLC-utils/amb-early-mtg/` — the ambiguous-early-meteg survey
- `https://bdenckla.github.io/UXLC-utils/fois/` — the features-of-interest catalog
- `https://bdenckla.github.io/UXLC-utils/clc/` — the CLC edition's pages

`gh-pages/` deliberately stays in this repository: moving it would break published links.
