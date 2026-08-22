# Vendored subtree used by codex-index-leningrad/UXLC-utils-sparse

`UXLC-utils` is the canonical source.
`codex-index-leningrad/UXLC-utils-sparse/` is a sparse vendored copy
that should be refreshed by running **MAM-basics'
`py/main_lenin_vendor_uxlc.py`**:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_lenin_vendor_uxlc.py
```

That was codex-index-leningrad's own root `main_update_vendored_files.py` until
Phase 3 of `../MAM-basics/doc/PLAN-evacuate-python-from-codex-index-trio.md`,
2026-08-22, which moved that repo's 21 modules to MAM-basics; Phase 4 emptied
codex-index-leningrad of Python the same day, so there is no script there to run
any more, and no venv either. The name changed with the move because
`main_update_vendored_files.py` was held by three repos at once and said nothing
about which vendored files it meant.

The vendored subset is defined by the files that already exist locally under
`codex-index-leningrad/UXLC-utils-sparse/`.

The local-only file `provenance.md` is not copied from `UXLC-utils`. It is
written by the command above, and only when a vendored byte actually moved or a
legacy path was removed, or `--force-provenance` is given — it stamps the source
repo's HEAD and today's date, so writing it unconditionally left it dirty after
any UXLC-utils commit and after any re-run on a later day.

## The subset is data only, as of 2026-08-03

It is `in/UXLC-39/*.xml` (39 files) and `data/lci_*.json` (2), and both of those
trees stayed in this repo when the Python left it. There was also a
`UXLC-utils-sparse/py/` holding seventeen of this repo's `.py`; it was removed the
same day, because its source moved to `../MAM-basics` and nothing in
codex-index-leningrad imported it. Its one entry point,
`main_uxlc_estimate_atom_loc.py`, is run from MAM-basics now and reads this repo
directly. See `../MAM-basics/doc/PLAN-evacuate-python-from-UXLC-utils.md`, Phase 5.

Refreshing the two data trees is a MAM-basics command, since this repo has no
Python to run: `py/main_write_page_break_info.py` writes `data/`, and `in/UXLC-39`
comes from `main_uxlc_download_changes.py`, which cannot run as of 2026-08-03 (see
`CLAUDE.md`).
