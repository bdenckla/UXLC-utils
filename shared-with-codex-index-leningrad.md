# Vendored subtree used by codex-index-leningrad/UXLC-utils-sparse

`UXLC-utils` is the canonical source.
`codex-index-leningrad/UXLC-utils-sparse/` is a sparse vendored copy
that should be refreshed by running that repo's
`main_update_vendored_files.py` script.

The vendored subset is defined by the files that already exist locally under
`codex-index-leningrad/UXLC-utils-sparse/`.

The local-only file `provenance.md` is not copied from `UXLC-utils`.

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
