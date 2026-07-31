# UXLC-utils / CLC dev tools

The **dual-cantillation `_ORACLE` derivation scripts** (issues #20/#28/#29) and the later
**MAM-alignment harvest scripts** (issues #42–45) that once lived here were **throwaway
scaffolding**: each reached into the sibling wlc-utils / MAM-basics / MAM-parsed repos and
emitted a regenerable `.novc/` dump that a human read to hand-encode
`py/clc/clc_dual_cant.py`'s `_ORACLE` and `py/clc/clc_versification.py`'s Decalogue verse
map — then retired once those issues closed. They carried shortcuts unacceptable in
long-term code (absolute cross-repo paths, live `MAM-basics/py` imports), which is exactly
why they were disposable. The hand-encoded results and their `*_test.py` files are the
durable record; nothing at runtime reads `.novc/`.

What remains here is `repo_maintenance.py`, plus the tracked git hook. **Everything else
that used to live here now lives under `py/`, behind a `py/main_*.py` entry point**
(issue #56): a script under `tools/` that wanted to import repo code had to put `py/` on
`sys.path` itself, and the standard is zero such inserts per repo. Nothing in `tools/` may
import repo code anymore — `repo_maintenance.py` only shells out to entry points.

## Repo maintenance

- `repo_maintenance.py` — the routine hygiene pass: wipes the gitignored `.novc/` scratch dir
  (everything in it is a regenerable download cache or tool output), syncs the vendored
  files, runs `black --check`, runs `py/main_source_hygiene.py`, runs `py/main_test.py`, then
  runs `py/main_0_mega.py` (every parameterless, non-download rebuild step; the two download
  scripts are deliberately excluded and must be run by hand). Run
  `python tools/repo_maintenance.py` from anywhere; `--skip-novc`, `--skip-vendored`,
  `--skip-black`, `--skip-hygiene`, `--skip-tests`, `--skip-rebuild`, and
  `--continue-on-test-failure` narrow it. Does not touch Claude auto-memory or
  `~/.claude/plans/` — that's a separate, on-demand, user-level Skill (`prune-claude-state`)
  since it needs live GitHub-issue cross-checks and a human confirming any deletion.
- `git-hooks/pre-commit` — a tracked hook that runs the source-hygiene scanner. Enable once,
  from the repo root: `git config core.hooksPath tools/git-hooks`.

## Where the moved tools went

### Tests — `py/main_test.py` (issue #56)

Every `*_test.py` in the repo runs under this one entry point, from the repo root:
`python py/main_test.py` for all of them, `--<flag>` for one, `--list` for the registry.
Running it puts `py/` at `sys.path[0]`, which is the only reason the test modules can say
`import clc.clc_kq` — so they are no longer independently runnable and carry no
`if __name__ == "__main__"` block. `TEST_MODULE_SPECS` is hand-maintained, so the runner
also walks `py/` for `*_test.py` on every run and fails if a file is missing from it; an
unregistered test file would otherwise report nothing at all rather than skipping visibly.

### Source-hygiene guard (issues #22, #26) — `py/repo_hygiene/`

A Unicode source-hygiene guard that fails on any **orphan combining mark**: a string literal
whose raw source starts with a bare combining mark (the "floating diacritic on the opening
quote" antipattern). The fix is a named escape, `"\N{UNICODE NAME}"`. It flags a *raw* mark
but accepts every escape form, so already-fixed code stays clean.

- `py/repo_hygiene/source_hygiene.py` — the shared scanner (a library, not runnable). Walks
  hand-authored `*.py` under `py/` and `tools/` (pruning `__pycache__` and the vendored
  `mb_cmn` / `mb_diff_mpu` packages), locates string literals via the AST, and tests each
  literal's **raw source segment**. A pluggable `Check` tuple lets the sibling h-with-dot
  guard (issues #21/#26) plug into the same harness.
- `py/main_source_hygiene.py` — the CLI the pre-commit hook runs. Prints each offender as
  `path:line  U+XXXX NAME` and exits non-zero when the tree is dirty.
- `py/repo_hygiene/source_hygiene_test.py` — pins the live tree clean plus synthetic
  positive/negative controls. `python py/main_test.py --source-hygiene`.
- `py/repo_hygiene/nfc_h_dot_below_test.py` — the NFC h-with-dot-below enforcement guard.
  `python py/main_test.py --nfc-h-dot-below`.

Escape hatch: a trailing `# combining-ok` on the offending line suppresses it.

### Note-page verification (issues #24, #25) — `py/main_verify_notes_zip.py`

A cross-check for the committed tanach.us note pages. `in/UXLC-notes/` now holds every UXLC
`<x>`-coded note page for all 39 books (issue #25; downloaded via
`py/main_clc_download_notes.py`, which fetches every code, not just the note-surfacing seed
`clc_collect.NOTED_CODES` the CLC build currently reads):

- `py/main_verify_notes_zip.py` → `.novc/notes_zip_verify.txt` — confirms each committed
  `in/UXLC-notes/<book>/*.html` against the frozen `Notes.zip` snapshot. Classifies every
  page as byte-`IDENTICAL`, `PROSE-EQUAL` (differs only in tanach.us template chrome; the
  prose CLC extracts is identical), or `PROSE-DIFFERS`, and dumps the prose for any mismatch.
  Independently, it also confirms every committed page's own prose extraction is non-empty,
  flagging any that aren't as `NO-PROSE-EXTRACTED` (issue #25 step 2) -- in practice this is
  a handful of NoteMaker-generated `c` ("text is correct relative to LC") pages whose only
  content is the change-log `<h2>`, which is deliberately not prose. Read-only; the zip path
  defaults to the frozen snapshot and can be overridden with an argument.
