"""Generate + self-verify a CLC _ORACLE entry for one dual-cant verse.

Builds each divergence atom's cluster/alef/bet from UXLC's combined bytes using the MAM
cant-alef / cant-bet strands as the oracle for which mark each reading keeps. Punctuation
present in UXLC (maqaf / sof pasuq) is treated as SHARED and left in both strands (CLC
never re-divides); a division mark a reading needs but UXLC lacks is a SUPPLIED mark.
Verifies by simulating clc_dual_cant.split_word, then prints the entry as constant-spelled
Python for pasting into _ORACLE.

Run from repo root: python .novc/gen_entry.py
"""

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "py"))

import clc.clc_read as clc_read  # noqa: E402
import clc.clc_dual_cant as dc  # noqa: E402
import mb_cmn.hebrew_accents as acc  # noqa: E402
import mb_cmn.hebrew_letters as hl  # noqa: E402
import mb_cmn.hebrew_points as hpo  # noqa: E402
import mb_cmn.hebrew_punctuation as hpu  # noqa: E402
from mb_cmn import str_defs as sd  # noqa: E402

_CGJ = sd.CGJ
_TSINNORIT = acc.ZSH_OR_TSIT
_PUNCT = {hpu.MAQ, hpu.SOPA, getattr(hpu, "PASOLEG", "׀")}
# A divergent dagesh / rafe on a בגדכפת letter — the hard/soft alternation the two readings
# disagree on (driven by the previous word's accent: disjunctive→hard/dagesh, conjunctive→soft).
_RAFE_DAGESH = {hpo.DAGOMOSD, hpo.RAFE}
_STRANDS = json.loads((_REPO / ".novc" / "mam_strands.json").read_text("utf-8"))

_BASE_LO, _BASE_HI = 0x05D0, 0x05EA


def _is_base(ch):
    return _BASE_LO <= ord(ch) <= _BASE_HI


# codepoint -> constant spelling, incl. letters (hl.*) for intervening letters in a cluster.
_NAME = {}
for _pfx, _mod in (("acc", acc), ("hpo", hpo), ("hpu", hpu), ("hl", hl)):
    for _n, _v in vars(_mod).items():
        if _n.isupper() and isinstance(_v, str) and len(_v) == 1:
            _NAME.setdefault(_v, f"{_pfx}.{_n}")
_NAME[_CGJ] = "_CGJ"


def _spell(s):
    # An empty resolution (a strand that drops its only divergent mark — e.g. an omitted
    # accent's bet) must spell as the literal "" so the generated source is valid Python.
    return " + ".join(_NAME.get(ch, f"chr(0x{ord(ch):04X})") for ch in s) or '""'


# strand char ("alef"/"bet") -> the _ORACLE source constant, so a generated "add" field
# pastes verbatim (clc_dual_cant spells add keys with these module constants).
_STRAND_CONST = {dc._STRAND_ALEF: "_STRAND_ALEF", dc._STRAND_BET: "_STRAND_BET"}


def _entry_src(entry):
    """Spell one _ORACLE entry dict (incl. an optional supplied ``add`` or omitted ``omit``)."""
    parts = [f'"cluster": {_spell(entry["cluster"])}',
             f'"alef": {_spell(entry["alef"])}',
             f'"bet": {_spell(entry["bet"])}']
    for field in ("add", "omit"):  # {strand: [mark, ...]} fields, spelled the same way
        if field in entry:
            spelled = ", ".join(
                f'{_STRAND_CONST[strand]}: [{", ".join(_spell(m) for m in marks)}]'
                for strand, marks in entry[field].items()
            )
            parts.append(f'"{field}": {{{spelled}}}')
    return "{" + ", ".join(parts) + "}"


def _mam_markset(word):
    """The marks a MAM strand word keeps: accents, points, meteg/silluq AND punctuation
    (maqaf / sof pasuq / legarmeh) — punctuation tracks intimately with accents, so a
    sof-pasuq a reading lacks is a real divergence (suppressed in that strand). Drops the
    tsinnorit stress-helper and the CGJ sequencing control."""
    return {ch for ch in word if not _is_base(ch) and ch != _TSINNORIT and ch != _CGJ}


def _is_accent(ch):
    """A cantillation accent (U+0591–U+05AF) or the meteg/silluq mark (U+05BD)."""
    return 0x0591 <= ord(ch) <= 0x05AF or ch == hpo.MTGOSLQ


def _build_atom_entry(uxlc, alef_word, bet_word):
    """Return (entry_dict_in_chars, notes, defer).

    Divergence is the SYMMETRIC DIFFERENCE of the two MAM readings' marksets — the two
    readings share the same word (vowels/points identical), so only accents, silluq,
    word-division punctuation, and (for a בגדכפת letter) dagesh/rafe differ. A genuine
    VOWEL divergence (a QUPO patax-vs-qamats word) we still DEFER for hand review.

    Two marks UXLC may handle unevenly are nonetheless encodeable:

      * **rafe/dagesh** (Policy 1, faithful — Ben's call). A divergent dagesh routes to the
        HARD reading (the MAM strand that has it). MAM never writes rafe, so the rafe UXLC
        stacked is in neither markset; it is the SOFT reading's own mark, so we pull it from
        UXLC into the strand WITHOUT the dagesh. No rafe is ever SUPPLIED: where UXLC wrote
        none (ex 20:9 כל), the soft letter stays bare. Pure subtraction.
      * **supplied sof-pasuq** (the additive charity — Gen 35:22's mechanism). A reading that
        ends a verse where UXLC wrote no sof-pasuq SUPPLIES it via the entry's ``add`` field —
        bracketed/green, never baked into the subtracted text; the receiving word must end in
        silluq.
      * **omitted accent** (Ben's policy: accents are NEVER supplied, only NOTED). An accent a
        reading's chanting wants but UXLC left untangled (it wrote only the other reading's
        accent) goes into the entry's ``omit`` field — a per-strand NOTE; nothing is added to the
        strand text. So the strand simply shows the word with that accent absent, faithfully.

    A non-accent SUPPLIED mark that is not a sof-pasuq (e.g. a maqaf UXLC lacks) still DEFERs."""
    a_set, b_set = _mam_markset(alef_word), _mam_markset(bet_word)
    notes = []
    alef_only = a_set - b_set
    bet_only = b_set - a_set
    diverging = alef_only | bet_only
    if not diverging:
        return None, notes, False
    # Policy 1 rafe pull: UXLC's stacked rafe (in neither MAM markset) is the soft reading's
    # mark — assign it to the strand WITHOUT the divergent dagesh, so it is kept there and
    # dropped from the hard strand (the existing subtraction + verify then route it).
    dagesh, rafe = hpo.DAGOMOSD, hpo.RAFE
    if dagesh in diverging and rafe in uxlc and rafe not in a_set and rafe not in b_set:
        soft_only = bet_only if dagesh in alef_only else alef_only
        soft_only.add(rafe)
        diverging = alef_only | bet_only
        notes.append(f"  ~~ rafe/dagesh: dagesh -> {'alef' if dagesh in alef_only else 'bet'} "
                     f"(hard), rafe -> {'bet' if dagesh in alef_only else 'alef'} (soft)")
    supplied = {}  # strand -> [marks SUPPLIED to it] (additive charity; only sof-pasuq)
    omitted = {}   # strand -> [accents it WANTS but UXLC omitted] (noted, never supplied)
    for m in sorted(diverging, key=ord):
        if not (_is_accent(m) or m in _PUNCT or m in _RAFE_DAGESH):
            notes.append(f"  ** non-accent divergence {_NAME.get(m, hex(ord(m)))} "
                         "(QUPO vowel split) — DEFER")
            return None, notes, True
        if m not in uxlc:
            strand = dc._STRAND_ALEF if m in alef_only else dc._STRAND_BET
            if m == hpu.SOPA:
                supplied.setdefault(strand, []).append(m)
                notes.append(f"  ++ SUPPLIED hpu.SOPA -> {strand} "
                             "(additive charity, encodeable via 'add')")
            elif _is_accent(m):
                omitted.setdefault(strand, []).append(m)
                notes.append(f"  ~~ OMITTED ACCENT {_NAME.get(m, hex(ord(m)))} -> {strand} "
                             "(noted, NOT supplied — encodeable via 'omit')")
            else:
                notes.append(f"  ** SUPPLIED {_NAME.get(m, hex(ord(m)))} (UXLC lacks it) — DEFER")
                return None, notes, True
    supplied_marks = {m for ms in supplied.values() for m in ms}
    omitted_marks = {m for ms in omitted.values() for m in ms}
    # The cluster spans only the diverging marks PRESENT in UXLC; a supplied or omitted mark
    # is not in UXLC, so it contributes no index (applied out-of-band via "add"/"omit").
    in_uxlc_div = diverging - supplied_marks - omitted_marks
    div_idx = [i for i, ch in enumerate(uxlc) if ch in in_uxlc_div]
    lo, hi = min(div_idx), max(div_idx)
    # A cluster opening on a dagesh/rafe begins one base letter earlier, so the carrier
    # בגדכפת consonant anchors it (position-safe, matching the rafe/dagesh test's shape).
    if uxlc[lo] in _RAFE_DAGESH and lo > 0 and _is_base(uxlc[lo - 1]):
        lo -= 1
    cluster = uxlc[lo:hi + 1]
    aset = alef_only - supplied_marks - omitted_marks
    bset = bet_only - supplied_marks - omitted_marks
    alef_res = "".join(c for c in cluster if c not in bset and c != _CGJ)
    bet_res = "".join(c for c in cluster if c not in aset and c != _CGJ)
    entry = {"cluster": cluster, "alef": alef_res, "bet": bet_res}
    if supplied:
        entry["add"] = {strand: list(marks) for strand, marks in supplied.items()}
    if omitted:
        entry["omit"] = {strand: list(marks) for strand, marks in omitted.items()}
    # verify against the real splitter
    assert cluster in uxlc, "cluster not substring"
    got_a = dc.split_word(uxlc, {"cluster": cluster, "alef": alef_res, "bet": bet_res}, "alef")
    got_b = dc.split_word(uxlc, {"cluster": cluster, "alef": alef_res, "bet": bet_res}, "bet")
    # Each reading keeps its own divergent marks (accents AND punctuation) and drops the
    # other's — so a sof-pasuq a reading lacks is suppressed there (Ben's rule).
    for ch in aset:
        assert ch in got_a and ch not in got_b, f"alef-only {hex(ord(ch))} leaked"
    for ch in bset:
        assert ch in got_b and ch not in got_a, f"bet-only {hex(ord(ch))} leaked"
    # Guard: a sof-pasuq must sit on a word whose last accent is silluq (U+05BD), never
    # etnaxta etc. (Ben's rule) — for one already in the subtracted text. EXCEPTION: where
    # this strand's silluq is itself OMITTED (UXLC wrote the sof-pasuq but not its silluq —
    # dt 5:17 elyon), the sof-pasuq faithfully stands alone and the omit-note records the gap.
    for strand_name, got in ((dc._STRAND_ALEF, got_a), (dc._STRAND_BET, got_b)):
        if hpu.SOPA in got and hpo.MTGOSLQ not in omitted.get(strand_name, []):
            accents = [c for c in got if _is_accent(c)]
            assert accents and accents[-1] == hpo.MTGOSLQ, f"sof-pasuq not on a silluq word: {got!r}"
    # ...and for a SUPPLIED sof-pasuq, the receiving strand's word ends in silluq.
    for strand, marks in supplied.items():
        if hpu.SOPA in marks:
            got = got_a if strand == dc._STRAND_ALEF else got_b
            accents = [c for c in got if _is_accent(c)]
            assert accents and accents[-1] == hpo.MTGOSLQ, \
                f"supplied sof-pasuq not on a silluq word ({strand}): {got!r}"
    return entry, notes, False


def gen_verse(bk39, bb, ch, v):
    """Return (py_source, diagnostics, ok, uses_supply, uses_omit).

    ``ok`` is False if the verse must DEFER (a QUPO vowel split, a non-sof-pasuq supplied
    punctuation mark, or a count mismatch); True if encodeable now — by pure subtraction,
    with a SUPPLIED sof-pasuq (``uses_supply``), and/or with an OMITTED-accent note
    (``uses_omit``: an accent UXLC left untangled, noted not supplied — Ben's policy)."""
    book = clc_read.read_book(bk39)
    atoms = [a["text"] for a in book[ch - 1][v - 1]]
    strands = _STRANDS[f"{bb}{ch}:{v}"]
    alef, bet = strands["alef"], strands["bet"]
    if not (len(atoms) == len(alef) == len(bet)):
        return "", f"=== {bb}{ch}:{v}: DEFER (count mismatch " \
            f"uxlc={len(atoms)} alef={len(alef)} bet={len(bet)})", False, False, False
    lines = [f'        ({ch}, {v}): {{']
    diag = [f"=== {bb}{ch}:{v} ({bk39}) ==="]
    ok, uses_supply, uses_omit = True, False, False
    for i, (ua, a, b) in enumerate(zip(atoms, alef, bet), start=1):
        entry, notes, defer = _build_atom_entry(ua, a, b)
        diag.extend(notes)
        if defer:
            ok = False
        if entry is None:
            continue
        if "add" in entry:
            uses_supply = True
        if "omit" in entry:
            uses_omit = True
        lines.append(f"            {i}: {_entry_src(entry)},")
        extra = "".join(f"  {f}={entry[f]!r}" for f in ("add", "omit") if f in entry)
        diag.append(f"  atom {i:2d} {ua}  cluster={_spell(entry['cluster'])}"
                    f"  alef={_spell(entry['alef'])}  bet={_spell(entry['bet'])}{extra}")
    lines.append("        },")
    return "\n".join(lines), "\n".join(diag), ok, uses_supply, uses_omit


# All dual-cant verses with a per-atom mark divergence (from oracle_report.txt).
_CANDIDATES = [
    ("Exodus", "ex", 20, v) for v in (2, 3, 5, 6, 8, 9, 13, 14, 15)
] + [
    ("Deuter", "dt", 5, v) for v in (6, 7, 9, 10, 13, 17, 18, 19)
]


def main():
    import builtins
    pure, supply, omit, defer, diags = [], [], [], [], []
    for bk39, bb, ch, v in _CANDIDATES:
        src, diag, ok, uses_supply, uses_omit = gen_verse(bk39, bb, ch, v)
        diags.append(diag)
        ref = f"{bb}{ch}:{v}"
        if not ok:
            bucket = defer
        elif uses_omit:
            bucket = omit       # an omitted-accent note (may also carry supply/rafe-dagesh)
        elif uses_supply:
            bucket = supply
        else:
            bucket = pure
        bucket.append((ref, src))
    out = _REPO / ".novc" / "entries.txt"
    body = ["# ENCODE NOW (pure subtraction, no supply):", ""]
    for ref, src in pure:
        body.append(f"# {ref}")
        body.append(src)
    body.append("\n# ENCODE NOW (pure subtraction + a SUPPLIED sof-pasuq, the additive "
                "charity — Gen 35:22's mechanism):\n")
    for ref, src in supply:
        body.append(f"# {ref}")
        body.append(src)
    body.append("\n# ENCODE NOW (subtraction + an OMITTED-ACCENT note — an accent UXLC left "
                "untangled, NOTED not supplied, Ben's policy; may also carry rafe/dagesh):\n")
    for ref, src in omit:
        body.append(f"# {ref}")
        body.append(src)
    body.append("\n# DEFER (a QUPO vowel split, a non-sof-pasuq supplied punctuation mark, "
                "or a maqaf count mismatch): " + ", ".join(ref for ref, _ in defer))
    body.append("\n\n# ---- diagnostics ----\n" + "\n".join(diags))
    out.write_text("\n".join(body), encoding="utf-8")
    builtins.print(f"wrote {out}")
    builtins.print(f"ENCODE pure:   {', '.join(r for r, _ in pure)}")
    builtins.print(f"ENCODE supply: {', '.join(r for r, _ in supply)}")
    builtins.print(f"ENCODE omit:   {', '.join(r for r, _ in omit)}")
    builtins.print(f"DEFER:         {', '.join(r for r, _ in defer)}")


if __name__ == "__main__":
    main()
