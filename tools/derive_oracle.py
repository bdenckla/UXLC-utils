"""Per-atom divergence analysis for the Decalogues, toward the CLC _ORACLE.

Aligns UXLC's combined atoms (clc_read) against MAM's cant-alef / cant-bet strands
(dumped by dump_mam_strands.py) and, for each divergence atom, reports the marks each
reading keeps — spelled from the mb_cmn constant names so a candidate _ORACLE cluster
is legible. Flags verses whose strand token counts don't 1:1-align (the maqaf-join /
supplied-mark / anomaly cases) for hand handling.

Run from repo root: python tools/derive_oracle.py
"""

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "py"))

import clc.clc_read as clc_read  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import mb_cmn.hebrew_points as hpo  # noqa: E402
import mb_cmn.hebrew_punctuation as hpu  # noqa: E402
from mb_cmn import str_defs as sd  # noqa: E402

_CGJ = sd.CGJ
_STRANDS = json.loads((_REPO / ".novc" / "mam_strands.json").read_text("utf-8"))

# 1-char base letters (alef..tav, final forms included) — everything else on a word is a mark.
_BASE_LO, _BASE_HI = 0x05D0, 0x05EA


def _is_base(ch):
    return _BASE_LO <= ord(ch) <= _BASE_HI


def _marks(word):
    """The non-letter marks of a word, in order (accents, points, meteg, dagesh, CGJ, maqaf...)."""
    return [ch for ch in word if not _is_base(ch)]


def _skel(word):
    return "".join(ch for ch in word if _is_base(ch))


# codepoint -> "acc.NAME" / "hpo.NAME" / "hpu.NAME" so a cluster reads in constant terms.
_NAME = {}
for _prefix, _mod in (("acc", acc), ("hpo", hpo), ("hpu", hpu)):
    for _n, _v in vars(_mod).items():
        if _n.isupper() and isinstance(_v, str) and len(_v) == 1:
            _NAME.setdefault(_v, f"{_prefix}.{_n}")
_NAME[_CGJ] = "_CGJ"


def _spell(chars):
    return " + ".join(_NAME.get(ch, f"U+{ord(ch):04X}") for ch in chars) or "(none)"


def _bcv(bb, ch, v):
    return f"{bb}{ch}:{v}"


_OUT = []


def print(*args):  # noqa: A001 — collect to a utf-8 report; console here is cp1252
    _OUT.append(" ".join(str(a) for a in args))


def analyze(bk39, bb, chapter, vrange):
    book = clc_read.read_book(bk39)
    verses = book[chapter - 1]
    print(f"\n===== {bk39} {chapter} ({bb}) =====")
    for v in vrange:
        atoms = [a["text"] for a in verses[v - 1]]
        strands = _STRANDS.get(_bcv(bb, chapter, v))
        if strands is None:
            print(f"{bb}{chapter}:{v}: NO MAM STRAND DATA")
            continue
        alef, bet, comb = strands["alef"], strands["bet"], strands["combined"]
        counts = f"uxlc={len(atoms)} mam_comb={len(comb)} alef={len(alef)} bet={len(bet)}"
        if not (len(atoms) == len(alef) == len(bet) == len(comb)):
            print(f"{bb}{chapter}:{v}: COUNT MISMATCH ({counts}) -> needs division/supply handling")
            continue
        div_lines = []
        for i, (ua, a, b) in enumerate(zip(atoms, alef, bet), start=1):
            ma, mb = _marks(a), _marks(b)
            if ma == mb:
                continue
            only_a = [c for c in ma if c not in mb]
            only_b = [c for c in mb if c not in ma]
            in_uxlc = all(c in ua for c in only_a + only_b)
            skel_ok = _skel(ua) == _skel(a) == _skel(b)
            div_lines.append(
                f"    atom {i:2d} {ua}\n"
                f"        alef-only: {_spell(only_a)}\n"
                f"        bet-only : {_spell(only_b)}\n"
                f"        marks-in-uxlc={in_uxlc} skel-aligned={skel_ok}"
            )
        if div_lines:
            print(f"{bb}{chapter}:{v}: {len(div_lines)} divergence atom(s) [{counts}]")
            print("\n".join(div_lines))
        else:
            print(f"{bb}{chapter}:{v}: no per-atom mark divergence [{counts}]")


def main():
    analyze("Exodus", "ex", 20, range(2, 18))
    analyze("Deuter", "dt", 5, range(6, 22))
    out_path = _REPO / ".novc" / "oracle_report.txt"
    out_path.write_text("\n".join(_OUT), encoding="utf-8")
    import builtins
    builtins.print(f"wrote {out_path} ({len(_OUT)} lines)")


if __name__ == "__main__":
    main()
