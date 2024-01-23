""" Exports read_them_in2, atoms """

import csv
import re
import unicodedata
from typing import List
import itertools
import my_uxlc_cvp as cvp
import my_uxlc_lci_rec as lci_rec
import my_hebrew_punctuation as hpu


def read_them_in3(uxlc, lci_recs):
    """ Read in high resolution page break info from multiple CSV files """
    sections = 'Exo thru Deu', 'Prophets', 'Writings'
    hi_res_starts = tuple(
        _read_sec(uxlc, lci_recs, sec) for sec in sections)
    hi_res_starts_f = sum(hi_res_starts, tuple())
    hi_res_starts_per_page = {v[0]: v[1:] for v in hi_res_starts_f}
    return hi_res_starts_per_page


def _read_sec(uxlc, lci_recs, section):
    """ Read in high resolution page break info from a single CSV file """
    fn_parts = 'LC page-spanning verses', section, 'triple alefs added.csv'
    filename = ' -- '.join(fn_parts)
    path = f'in/UXLC-misc/{filename}'
    with open(path, encoding='utf-8') as csv_in_fp:
        raw_rows = tuple(map(_make_row, csv.reader(csv_in_fp)))
    real_raw_rows = tuple(filter(_raw_row_is_real, raw_rows))
    cooked_rows = tuple(map(_cook_row, real_raw_rows[1:]))
    split_verses = dict(cooked_rows)
    assert len(split_verses) == len(cooked_rows)
    hi_res_starts = tuple(
        _make_hi_res(uxlc, split_verses, lcir) for lcir in lci_recs)
    hi_res_starts_real = tuple(filter(None, hi_res_starts))
    return hi_res_starts_real


def _make_row(list_of_cell_vals):
    return list_of_cell_vals


def _raw_row_is_real(raw_row):
    verse_str, pgid = raw_row
    pgids_of_bad_pages = {}
    return verse_str != '' and pgid not in pgids_of_bad_pages


def _cook_row(raw_row):
    verse_str, pgid = raw_row
    parts = verse_str.split(" 'אאא' ")
    assert len(parts) == 2
    parts_as_atom_lists = atoms(parts[0]), atoms(parts[1])
    verse = *parts_as_atom_lists, *parts
    return pgid, verse


def atoms(string):
    """ Split a string into its atoms. """
    patt = f'([ {hpu.MAQ}])'
    words_and_seps = re.split(patt, string)
    if words_and_seps[-1] == '':
        words_and_seps.pop()
    remaps = {' ': '', hpu.PAS: ' ' + hpu.PAS, hpu.MAQ: hpu.MAQ}
    accum = []
    for word_or_sep in words_and_seps:
        remap = remaps.get(word_or_sep)
        if remap is not None:
            accum[-1] += remap
        else:
            accum.append(word_or_sep)
    return accum


def _make_hi_res(uxlc, split_verses, lcir):
    split_verse = _check(uxlc, split_verses, lcir)
    return split_verse and _make_hi_res2(lcir, split_verse)


def _check(uxlc, split_verses, lcir):
    pg_sp_vr = _page_spanning_verse(uxlc, lcir)
    if pg_sp_vr is None:
        return None
    pgid = lci_rec.get_pgid(lcir)
    split_verse = split_verses.get(pgid)
    if split_verse is None:
        return None
    unsplit_verse = split_verse[0] + split_verse[1]
    unsplit_verse_n = _norm_atoms(unsplit_verse)
    pg_sp_vr_n = _norm_atoms(pg_sp_vr)
    _check2(unsplit_verse_n, pg_sp_vr_n)
    return split_verse


def _page_spanning_verse(uxlc, lcir):
    bcv = lci_rec.starts_with_part_b(lcir)
    if bcv is None:
        return None
    bkid = bcv[0]
    book = uxlc[bkid]
    zb_chidx = bcv[1] - 1  # zb_chidx: zero-based chapter index
    zb_vridx = bcv[2] - 1  # zb_vridx: zero-based verse index
    return book[zb_chidx][zb_vridx]


def _make_hi_res2(lcir, split_verse):
    pgid = lci_rec.get_pgid(lcir)
    bkid = lci_rec.get_bkid(lcir)
    cvp_start = lci_rec.get_cvp_start(lcir)
    assert cvp.get_povr(cvp_start) == 'b'
    atom_num = 1 + len(split_verse[0])  # one-based
    chapnver = cvp.chapnver(cvp_start)
    new_cvp = cvp.make(*chapnver, atom_num)
    return pgid, bkid, new_cvp


def _check2(unsplit_verse_n, pg_sp_vr_n):
    if unsplit_verse_n != pg_sp_vr_n:
        for atom_pair in itertools.zip_longest(unsplit_verse_n, pg_sp_vr_n):
            assert atom_pair[0] == atom_pair[1]


def _norm_atoms(in_atoms: List[str]):
    return list(map(_norm_str, in_atoms))


def _norm_str(string: str):
    return unicodedata.normalize('NFC', string)
