"""Dump MAM-simple cant alef/bet/combined strands for the Decalogues (Ex 20, Deut 5).

The oracle SIGNAL for the CLC dual-cant detangler: for each dual-cant verse, MAM's
already-separated cant-alef / cant-bet / cant-combined token streams. Reads from the
sibling wlc-utils (the loader) + MAM-simple (the data) repos; writes a JSON that the
CLC oracle-derivation step consumes. Exploratory scratch — not committed.

Run: python tools/dump_mam_strands.py
"""

import json
import sys
from pathlib import Path

_WLC_PY = Path(r"C:\Users\BenDe\GitRepos\wlc-utils\py")
sys.path.insert(0, str(_WLC_PY))

from accgram.mam_simple_verse import load_mam_simple_for_refs  # noqa: E402
import repo_paths  # noqa: E402
from mb_cmn import hebrew_punctuation as hpu  # noqa: E402

# wlc book codes (bb) -> the Decalogue refs, matching dual_cant_detangle.PASSAGES.
REFS = {
    "ex": {(20, v) for v in range(2, 18)},
    "dt": {(5, v) for v in range(6, 22)},
}


def _fold_pasoleg(words):
    """MAM-simple tokenizes a standalone pasoleg (a space then hpu.PASOLEG) as its own word;
    UXLC embeds it directly in the preceding word's atom instead. Fold it the same way so
    word counts line up with UXLC (issue #20's count-mismatch verses, issue #29).

    "Pasoleg" (echoing the PASOLEG constant, a paseq+legarmeh portmanteau) means the raw
    U+05C0 character regardless of whether it functions as narrow-sense paseq or legarmeh
    (design doc §7.16) -- that grammatical distinction is irrelevant to tokenization, which
    only cares about the codepoint."""
    out = []
    for w in words:
        if w == hpu.PASOLEG and out:
            out[-1] += hpu.PASOLEG
        else:
            out.append(w)
    return out


def main():
    data = load_mam_simple_for_refs(
        repo_paths.mam_simple_dir(), REFS, include_strands=True
    )
    out = {}
    for bcv, info in data.items():
        verse = info["mam_simple_verse"]
        out[bcv] = {
            "combined": verse.get("vels"),
            "alef": _fold_pasoleg(verse.get("vels_cant_alef")),
            "bet": _fold_pasoleg(verse.get("vels_cant_bet")),
        }
    out_path = Path(__file__).resolve().parent.parent / ".novc" / "mam_strands.json"
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out_path} ({len(out)} verses)")
    # Quick peek: which verses' alef and bet strands actually differ (the divergences).
    def _ref_key(bcv):
        bb = bcv[:2]
        chnu, vrnu = bcv[2:].split(":")
        return (bb, int(chnu), int(vrnu))

    for bcv in sorted(out, key=_ref_key):
        a, b = out[bcv]["alef"], out[bcv]["bet"]
        flag = "DIFFER" if a != b else "same"
        print(f"  {bcv}: alef={len(a)} bet={len(b)} combined={len(out[bcv]['combined'])}  [{flag}]")


if __name__ == "__main__":
    main()
