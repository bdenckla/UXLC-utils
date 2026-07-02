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
# A divergent patax/qamats stacked on one letter (QUPO: the vowel itself splits the readings,
# e.g. ex 20:3 / dt 5:7's פני) — same position-safe subtraction bucket as rafe/dagesh (§7.7).
_VOWEL_QUPO = {hpo.QAMATS, hpo.PATAX}
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


def _mark_runs(word):
    """Split a MAM strand word into one run of marks per base letter — the marks trailing
    each letter up to the next letter or word end, so a trailing sof-pasuq/maqaf attaches to
    the LAST letter's run. Drops the tsinnorit stress-helper and the CGJ sequencing control,
    like _mam_markset. Runs align positionally between alef_word/bet_word (the two readings
    share the same consonants, §7.7). Seeded with one leading run so a word with no base
    letter at all (dt 5:10 tokenizes a lone trailing sof-pasuq as its own MAM "word") still
    gets a run to hold it, instead of indexing into an empty list."""
    runs = [[]]
    for ch in word:
        if _is_base(ch):
            runs.append([])
        elif ch != _TSINNORIT and ch != _CGJ:
            runs[-1].append(ch)
    return [frozenset(run) for run in runs]


def _mam_divergence(alef_word, bet_word):
    """Per-LETTER positional divergence between the two MAM readings of one word: unlike a
    whole-word markset diff (_mam_markset), this isolates a divergence to its exact letter —
    needed for a QUPO word, where the same mark type (e.g. qamats) can appear TWICE: once as
    an unrelated, merely coincidental, SHARED vowel earlier in the word, and once as the
    letter that actually splits the two readings. A flat whole-word set diff cannot tell those
    two occurrences apart (a set has no notion of "at this position") and silently treats the
    divergent occurrence as shared too, leaking it into both resolutions."""
    a_runs, b_runs = _mark_runs(alef_word), _mark_runs(bet_word)
    assert len(a_runs) == len(b_runs), (alef_word, bet_word)  # same consonants (§7.7)
    alef_only, bet_only = set(), set()
    for ra, rb in zip(a_runs, b_runs):
        alef_only |= ra - rb
        bet_only |= rb - ra
    return alef_only, bet_only


def _is_accent(ch):
    """A cantillation accent (U+0591–U+05AF) or the meteg/silluq mark (U+05BD)."""
    return 0x0591 <= ord(ch) <= 0x05AF or ch == hpo.MTGOSLQ


def _build_atom_entry(uxlc, alef_word, bet_word):
    """Return (entry_dict_in_chars, notes, defer).

    Divergence is the SYMMETRIC DIFFERENCE of the two MAM readings' marksets — the two
    readings share the same word (vowels/points identical unless the divergence is itself
    a QUPO vowel split), so only accents, silluq, word-division punctuation, and (for a
    בגדכפת letter) dagesh/rafe, or (for a QUPO letter) patax/qamats, differ.

    Marks UXLC may handle unevenly are nonetheless encodeable:

      * **rafe/dagesh** (Policy 1, faithful — Ben's call). A divergent dagesh routes to the
        HARD reading (the MAM strand that has it). MAM never writes rafe, so the rafe UXLC
        stacked is in neither markset; it is the SOFT reading's own mark, so we pull it from
        UXLC into the strand WITHOUT the dagesh. No rafe is ever SUPPLIED: where UXLC wrote
        none (ex 20:9 כל), the soft letter stays bare. Pure subtraction.
      * **QUPO vowel split** (patax vs. qamats stacked on one letter, e.g. ex 20:3 / dt 5:7's
        פני). Both vowels are already in UXLC's combined bytes, so — like rafe/dagesh — this
        is pure position-safe subtraction: each reading keeps its own vowel, drops the other's.
      * **supplied punctuation** (the additive charity — Gen 35:22's mechanism, extended to
        any mark in ``dc._SUPPLIABLE`` — maqaf as well as sof-pasuq). A reading that needs a
        word-division mark UXLC lacks SUPPLIES it via the entry's ``add`` field — bracketed/
        green, never baked into the subtracted text.
      * **omitted accent** (Ben's policy: accents are NEVER supplied, only NOTED). An accent a
        reading's chanting wants but UXLC left untangled (it wrote only the other reading's
        accent) goes into the entry's ``omit`` field — a per-strand NOTE; nothing is added to the
        strand text. So the strand simply shows the word with that accent absent, faithfully.

    Still DEFERs: a mark outside all of the recognized buckets (not an accent, not word-division
    punctuation, not rafe/dagesh, not a QUPO vowel), or a punctuation mark UXLC lacks that is
    not in ``dc._SUPPLIABLE`` (e.g. a missing legarmeh — never supplied, unlike maqaf/sof-pasuq)."""
    a_set, b_set = _mam_markset(alef_word), _mam_markset(bet_word)
    notes = []
    # Per-LETTER divergence (_mam_divergence), not a_set - b_set: a QUPO word's own vowel can
    # coincide in TYPE with an unrelated, merely coincidental, shared vowel earlier in the same
    # word (ex 20:3 / dt 5:7's פני — qamats on both פ's shared syllable AND, divergently, on
    # נ), and a flat whole-word set diff cannot distinguish those two occurrences.
    alef_only, bet_only = _mam_divergence(alef_word, bet_word)
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
        if not (_is_accent(m) or m in _PUNCT or m in _RAFE_DAGESH or m in _VOWEL_QUPO):
            notes.append(f"  ** non-accent divergence {_NAME.get(m, hex(ord(m)))} "
                         "(unrecognized mark class) — DEFER")
            return None, notes, True
        if m not in uxlc:
            strand = dc._STRAND_ALEF if m in alef_only else dc._STRAND_BET
            if m in dc._SUPPLIABLE:
                supplied.setdefault(strand, []).append(m)
                notes.append(f"  ++ SUPPLIED {_NAME.get(m, hex(ord(m)))} -> {strand} "
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
    # is not in UXLC, so it contributes no index (applied out-of-band via "add"/"omit"). Seed
    # from the NON-vowel marks only: a QUPO vowel's TYPE (patax/qamats) can also occur as an
    # unrelated SHARED vowel elsewhere in the same atom (ex 20:3 / dt 5:7's פני — see
    # _mam_divergence's docstring), so a plain by-TYPE scan of uxlc would match that unrelated
    # occurrence too. Instead anchor on the safe (non-recurring) marks, then absorb a QUPO
    # vowel only if it is immediately ADJACENT to that span: a vowel point always attaches to
    # the letter directly preceding it, so adjacency to an already-anchored divergent mark
    # means it sits on the SAME (diverging) letter, not a different, merely-coincidental one.
    in_uxlc_div = diverging - supplied_marks - omitted_marks
    safe_div = in_uxlc_div - _VOWEL_QUPO
    div_idx = [i for i, ch in enumerate(uxlc) if ch in (safe_div or in_uxlc_div)]
    lo, hi = min(div_idx), max(div_idx)
    # Extend only into a QUPO vowel that is ITSELF a divergent type somewhere in this atom
    # (``in_uxlc_div``, not the whole static _VOWEL_QUPO class) — else an unrelated, genuinely
    # SHARED qamats/patax that happens to sit next to a real (non-vowel) divergence would be
    # swept in too (harmless — it would survive both resolutions unchanged — but needlessly
    # widens the cluster).
    while lo > 0 and uxlc[lo - 1] in _VOWEL_QUPO and uxlc[lo - 1] in in_uxlc_div:
        lo -= 1
    while (hi + 1 < len(uxlc) and uxlc[hi + 1] in _VOWEL_QUPO
           and uxlc[hi + 1] in in_uxlc_div):
        hi += 1
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
    # other's — so a sof-pasuq a reading lacks is suppressed there (Ben's rule). EXCEPTION: a
    # mark TYPE that is independently shared elsewhere in the word (whole-word marksets,
    # ``shared_types`` below — e.g. a QUPO word's own qamats, present on BOTH readings' shared
    # prefix letter as well as, divergently, on the QUPO letter itself) legitimately survives
    # in the other strand's result too — that is its OWN, unrelated occurrence, not a leak.
    shared_types = a_set & b_set
    for ch in aset:
        assert ch in got_a, f"alef-only {hex(ord(ch))} missing"
        assert ch in shared_types or ch not in got_b, f"alef-only {hex(ord(ch))} leaked"
    for ch in bset:
        assert ch in got_b, f"bet-only {hex(ord(ch))} missing"
        assert ch in shared_types or ch not in got_a, f"bet-only {hex(ord(ch))} leaked"
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

    ``ok`` is False if the verse must DEFER (an unrecognized mark divergence, a non-suppliable
    punctuation mark UXLC lacks, or an atom-count mismatch); True if encodeable now — by pure
    subtraction, with a SUPPLIED maqaf/sof-pasuq (``uses_supply``), and/or with an OMITTED-accent
    note (``uses_omit``: an accent UXLC left untangled, noted not supplied — Ben's policy)."""
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
    ("Exodus", "ex", 20, v) for v in (2, 3, 4, 5, 6, 8, 9, 10, 13, 14, 15)
] + [
    ("Deuter", "dt", 5, v) for v in (6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19)
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
    body.append("\n# DEFER (an atom-count mismatch, or a divergence outside the recognized "
                "mark classes): " + ", ".join(ref for ref, _ in defer))
    body.append("\n\n# ---- diagnostics ----\n" + "\n".join(diags))
    out.write_text("\n".join(body), encoding="utf-8")
    builtins.print(f"wrote {out}")
    builtins.print(f"ENCODE pure:   {', '.join(r for r, _ in pure)}")
    builtins.print(f"ENCODE supply: {', '.join(r for r, _ in supply)}")
    builtins.print(f"ENCODE omit:   {', '.join(r for r, _ in omit)}")
    builtins.print(f"DEFER:         {', '.join(r for r, _ in defer)}")


if __name__ == "__main__":
    main()
