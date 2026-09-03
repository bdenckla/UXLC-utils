# CLAUDE.md

## UXLC-utils is a redirect host

`gh-pages/` consists of generated redirect stubs. Do not edit a stub by hand. Regenerate the
stubs from the primary MAM-basics checkout with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_redirect_stubs.py build --repo UXLC-utils --publish
```

UXLC-utils holds no Python and no data. UXLC-utils' data and generators are in
`../MAM-basics`.

## UXLC-utils issue numbers

UXLC-utils' issues remain in `bdenckla/UXLC-utils`, so a bare `#NN` in this repository names an
UXLC-utils issue. New issues, including work on the generators now in MAM-basics, are filed in
MAM-basics.
