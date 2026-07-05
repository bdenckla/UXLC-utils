# UXLC-utils — repo conventions

Tooling around UXLC (the Unicode/XML Leningrad Codex) and the **CLC** (Charitable
Leningrad Codex), a planned new edition built charitably on top of UXLC. Design doc:
[`doc/clc-design.md`](doc/clc-design.md). CLC code lives in `py/clc/`; its rendered
output (served at `bdenckla.github.io/UXLC-utils/...`) lives in `gh-pages/clc/`.

## Reading MAM data — use the parsed form + the vendored readers, never the raw source

CLC draws on MAM (Miqra according to the Masorah) from the sibling repos. **Before
writing any code that reads MAM, grep for how it is already read here** — the readers
almost certainly already exist in this repo.

- **Doc-notes / verse structure**: read from **`../MAM-parsed`** (preferably the
  **`/plus`** variety), the already-parsed structured JSON. Do **not** regex-parse the
  raw wikisource source (`MAM-basics/in/mam-go/A-Torah.csv`) — that reinvents the
  wikisource template parser that MAM-parsed already ran.
- **Use the vendored helpers in [`py/mb_diff_mpu/`](py/mb_diff_mpu/)** to walk the
  /plus format — the same module `py/clc/clc_dual_cant.py` and `clc_render.py` use:
  - `mpplus_param_access.get_param(tmpl, key)` — robust template-param access across
    historical formats (don't hand-roll `tmpl.get("tmpl_params", {})`).
  - `mpplus_flatten` — `flatten_element`, `flatten_ep*`, `is_parashah_template`,
    ketiv/qere predicates, and `flatten_ep_with_docnote_for_diff` /
    `find_relevant_docnote` for נוסח doc-note spans.
- The /plus format is **documented**: `../MAM-parsed/README.md` → the structure
  reference `gh-pages/plus/html/mpplus*.html` (e.g. `mpplus_docnote.html`,
  `mpplus_dualcant.html`). Read the spec instead of reverse-engineering. (The README
  warns the /plus format is **not yet stable**.)
- Verse structure quick ref: a /plus verse is `[CP, DP, EP]`; `EP` (index 2) is the
  body sequence. A dual-cantillation verse wraps its combined text in
  `{"tmpl_name": "מ:כפול", "tmpl_params": {"כפול": …, "א": …, "ב": …}}`, where `כפול`
  carries the doc-notes and `א`/`ב` are the rendered strands (Decalogue: א=תחתון/taxton,
  ב=עליון/elyon; Reuben: א=פשוטה, ב=מדרשית).

## Cross-repo reuse — vendoring, not live imports

- **Do not `sys.path`-import from `MAM-basics/py`** in real/official code. The
  sanctioned mechanism for reusing MAM-basics code is **vendoring** (copy the module
  in; see `py/main_update_vendored_files.py` and the vendored `py/mb_cmn`,
  `py/mb_diff_mpu`).
- **Only directories whose names start with `mb_` are vendorable.** A non-`mb_` dir
  like `py_misc` is **neither importable nor vendorable** — code needing its
  functionality (e.g. the versification converter) must get it via a public `mb_*`
  entry point, or the functionality must move upstream into an `mb_` dir first.

## `tools/` — throwaway scaffolding vs. official code

Some `tools/dump_mam_*.py` scripts are **throwaway scaffolding** tied to in-flight
issues: they emit a scratch JSON under `.novc/` (gitignored) that a human reads to
hand-encode the CLC oracle, then retire. Such scripts may carry shortcuts that are
**not acceptable in long-term code** (they say so in their headers). Do not copy their
shortcuts (absolute cross-repo paths, live `MAM-basics/py` imports) into real code.

## Source hygiene (enforced)

- **No orphan combining marks in source.** Never write a bare combining mark as a
  literal (a diacritic/point with no base letter). Use `"\N{UNICODE NAME}"`, or build
  the char from `chr(0x…)` with a naming comment. `tools/source_hygiene.py` fails the
  build (and the pre-commit hook) on violations.
- **UTF-8 stdio.** Every `py/main_*.py` reconfigures stdout/stderr to UTF-8 as the
  first lines of `main()` (Windows redirects to cp1252 otherwise, crashing Hebrew
  prints). Prefer writing non-ASCII output to UTF-8 files over stdout.
- Source is standardized on **NFC**; text files are pinned to **LF** (`.gitattributes`).
