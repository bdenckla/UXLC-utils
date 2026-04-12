import sys
from collections import Counter, defaultdict
from pathlib import Path

import _repo_path_setup
import main_fois
import py_misc.my_uxlc as my_uxlc
from py_misc import uni_heb_char_classes as ucc
from pycmn import hebrew_points as hpo
from pycmn import str_defs as sd


REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / ".novc" / "foi_mark_grammar_probe.txt"
DUAL_CANTILLATION_LOCS = {
    ("Exodus", 20),
    ("Deuter", 5),
    ("Genesis", 35, 22),
}
SLA_MARKS = {hpo.SHIND, hpo.SIND}
DAGESH_MARKS = {hpo.DAGOMOSD}
VOWEL_MARKS = set(ucc.VOWEL_POINTS)
AOM_MARKS = set(ucc.ACCENTS)
KNOWN_MISC = {sd.CGJ, hpo.RAFE, hpo.VARIKA}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    rows = []
    stats = collect_stats()
    rows.extend(_summary_lines(stats))
    OUT_PATH.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


def collect_stats():
    uxlc = my_uxlc.read_all_books(main_fois._VERSE_CHILD_HANDLERS)
    sequence_counts = Counter()
    multi_aom_counts = Counter()
    unexpected_counts = Counter()
    example_by_sequence = {}
    example_by_multi_aom = {}
    example_by_unexpected = {}
    total_clusters = 0
    excluded_atoms = 0
    for bkid, chapters in uxlc.items():
        for chidx, chapter in enumerate(chapters, start=1):
            for vridx, verse in enumerate(chapter, start=1):
                if _is_excluded(bkid, chidx, vridx):
                    excluded_atoms += len(verse)
                    continue
                for atidx, atom in enumerate(verse, start=1):
                    for cluster_idx, cluster in enumerate(
                        _split_clusters(atom[1]), start=1
                    ):
                        total_clusters += 1
                        seq = _mark_sequence(cluster)
                        sequence_counts[seq] += 1
                        example_by_sequence.setdefault(
                            seq,
                            _example_tuple(
                                bkid,
                                chidx,
                                vridx,
                                atidx,
                                cluster_idx,
                                atom[0],
                                atom[1],
                                cluster,
                            ),
                        )
                        aom_signature = _aom_signature(cluster)
                        if aom_signature is not None:
                            multi_aom_counts[aom_signature] += 1
                            example_by_multi_aom.setdefault(
                                aom_signature,
                                _example_tuple(
                                    bkid,
                                    chidx,
                                    vridx,
                                    atidx,
                                    cluster_idx,
                                    atom[0],
                                    atom[1],
                                    cluster,
                                ),
                            )
                        unexpected = _unexpected_marks(cluster)
                        if unexpected:
                            unexpected_key = ",".join(unexpected)
                            unexpected_counts[unexpected_key] += 1
                            example_by_unexpected.setdefault(
                                unexpected_key,
                                _example_tuple(
                                    bkid,
                                    chidx,
                                    vridx,
                                    atidx,
                                    cluster_idx,
                                    atom[0],
                                    atom[1],
                                    cluster,
                                ),
                            )
    return {
        "total-clusters": total_clusters,
        "excluded-atoms": excluded_atoms,
        "sequence-counts": sequence_counts,
        "multi-aom-counts": multi_aom_counts,
        "unexpected-counts": unexpected_counts,
        "example-by-sequence": example_by_sequence,
        "example-by-multi-aom": example_by_multi_aom,
        "example-by-unexpected": example_by_unexpected,
    }


def _is_excluded(bkid, chnu, vrnu):
    return (bkid, chnu) in DUAL_CANTILLATION_LOCS or (
        bkid,
        chnu,
        vrnu,
    ) in DUAL_CANTILLATION_LOCS


def _split_clusters(atom_text):
    clusters = []
    current = None
    for ch in atom_text:
        if ch in ucc.LETTERS:
            current = {"letter": ch, "marks": []}
            clusters.append(current)
            continue
        if current is None:
            continue
        current["marks"].append(ch)
    return clusters


def _mark_sequence(cluster):
    return "".join(_mark_class(mark) for mark in cluster["marks"])


def _mark_class(mark):
    if mark in SLA_MARKS:
        return "s"
    if mark in DAGESH_MARKS:
        return "d"
    if mark in VOWEL_MARKS:
        return "v"
    if mark in AOM_MARKS:
        return "a"
    if mark == sd.CGJ:
        return "c"
    return "?"


def _aom_signature(cluster):
    aom_marks = [mark for mark in cluster["marks"] if mark in AOM_MARKS]
    if len(aom_marks) < 2:
        return None
    return "+".join(aom_marks)


def _unexpected_marks(cluster):
    return [
        mark
        for mark in cluster["marks"]
        if _mark_class(mark) == "?" and mark not in KNOWN_MISC
    ]


def _summary_lines(stats):
    rows = []
    rows.append(f"total_clusters: {stats['total-clusters']}")
    rows.append(f"excluded_atoms: {stats['excluded-atoms']}")
    rows.append("")
    rows.append("top_sequences:")
    rows.extend(
        _section_lines(stats["sequence-counts"], stats["example-by-sequence"], 40)
    )
    rows.append("")
    rows.append("multi_aom_sequences:")
    rows.extend(
        _section_lines(stats["multi-aom-counts"], stats["example-by-multi-aom"], 40)
    )
    rows.append("")
    rows.append("unexpected_marks:")
    rows.extend(
        _section_lines(stats["unexpected-counts"], stats["example-by-unexpected"], 20)
    )
    return rows


def _section_lines(counter, examples, limit):
    if not counter:
        return ["  <none>"]
    rows = []
    for key, count in counter.most_common(limit):
        rows.append(f"  {count:>7}  {key}")
        rows.append(f"           {examples[key]}")
    return rows


def _example_tuple(bkid, chnu, vrnu, atnu, cluster_idx, atom_type, atom_text, cluster):
    return (
        f"{bkid} {chnu}:{vrnu}.{atnu} cluster {cluster_idx} "
        f"({atom_type}) atom={atom_text} cluster={cluster['letter']}{''.join(cluster['marks'])}"
    )


if __name__ == "__main__":
    main()
