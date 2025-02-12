"""Exports read_them_in2"""

import csv
import re
import my_tanakh_book_names as tbn
import my_uxlc_cvp as cvp
import my_uxlc_lci_rec as lci_rec
import my_uxlc_hi_res_gen_no as hi_res_gen_no

# gpgid: Genesis page id: PP-LLC e.g. 01-01B, 61-31B
# where:
#    PP = two-digit, zero-padded page number (01 to 61)
#    LL = two-digit, zero-padded leaf number (01 to 31)
#    C  = A or B


def read_them_in2(uxlc, lci_recs):
    """Read in line info from a CSV file"""
    path = "in/UXLC-misc/LC Genesis line breaks.csv"
    with open(path, encoding="utf-8") as csv_in_fp:
        raw_rows = tuple(map(_make_row, csv.reader(csv_in_fp)))
    real_raw_rows = tuple(filter(_raw_row_is_real, raw_rows))
    pages = _get_pages(real_raw_rows)
    stastos = _get_stastos(pages)
    hi_res_starts = tuple(_make_hi_res(uxlc, stastos, lcir) for lcir in lci_recs)
    hi_res_starts_real = tuple(filter(None, hi_res_starts))
    hi_res_dic = {v[0]: v[1:] for v in hi_res_starts_real}
    return hi_res_dic, stastos


def _make_hi_res(uxlc, split_verses, lcir):
    atom_number = _atom_number(uxlc, split_verses, lcir)
    return atom_number and _make_hi_res2(lcir, atom_number)


def _atom_number(uxlc, stastos, lcir):
    pg_sp_vr = _page_spanning_verse(uxlc, lcir)
    if pg_sp_vr is None:
        return None
    pgid = lci_rec.get_pgid(lcir)
    stasto = stastos.get(pgid)
    if stasto is None:
        bkid = lci_rec.get_bkid(lcir)
        assert bkid != tbn.BK_GENESIS
        return None
    page_start_cell_str = stasto[0]
    page_start_cell_atoms = _atomize(page_start_cell_str)
    atom_number = _find_unique(pg_sp_vr, page_start_cell_atoms)
    return atom_number


def _find_unique(pg_sp_vr, cell_atoms, offset=0):
    page_start_atom = cell_atoms[offset]
    count = pg_sp_vr.count(page_start_atom)
    if count > 1:
        return _find_unique(pg_sp_vr, cell_atoms, offset + 1)
    assert count == 1
    atom_number = 1 + pg_sp_vr.index(page_start_atom)
    return atom_number - offset


def _atomize(cell_str):
    sep_patt = "([\u0591-\u05f4\u034f\u200d]+)"
    words_and_seps = re.split(sep_patt, cell_str)
    rejoined = " ".join(words_and_seps[1::2])
    atoms = hi_res_gen_no.atoms(rejoined)
    return atoms


def _page_spanning_verse(uxlc, lcir):
    bcv = lci_rec.starts_with_part_b(lcir)
    if bcv is None:
        return None
    bkid = bcv[0]
    book = uxlc[bkid]
    zb_chidx = bcv[1] - 1  # zb_chidx: zero-based chapter index
    zb_vridx = bcv[2] - 1  # zb_vridx: zero-based verse index
    return book[zb_chidx][zb_vridx]


def _make_hi_res2(lcir, atom_number):
    pgid = lci_rec.get_pgid(lcir)
    bkid = lci_rec.get_bkid(lcir)
    cvp_start = lci_rec.get_cvp_start(lcir)
    assert cvp.get_povr(cvp_start) == "b"
    chapnver = cvp.chapnver(cvp_start)
    new_cvp = cvp.make(*chapnver, atom_number)
    return pgid, bkid, new_cvp


def _get_stastos(pages):
    stastos = {pgid: _get_stasto(rows) for pgid, rows in pages.items()}
    return stastos


def _get_stasto(rows):
    start = _first_real(rows, 0)
    stop = _last_real(rows, -1) or _last_real(rows, -2)
    assert start
    assert stop
    return start, stop


def _first_real(rows, colidx):
    for posrowidx in range(0, len(rows)):  # e.g. [0, 27)
        rowidx = posrowidx
        if cell := rows[rowidx][colidx]:
            return cell
    return cell


def _last_real(rows, colidx):
    for posrowidx in range(0, len(rows)):  # e.g. [0, 27)
        rowidx = -1 - posrowidx  # e.g. [-1, -28)
        if cell := rows[rowidx][colidx]:
            return cell
    return cell


def _get_pages(real_raw_rows):
    pages = {}
    for raw_row in real_raw_rows:
        gpgid = raw_row[0]
        cols = raw_row[1:]
        pgid = _get_pgid_from_gpgid(gpgid)
        if page := pages.get(pgid):
            page.append(cols)
        else:
            pages[pgid] = [cols]
    return pages


def _get_pgid_from_gpgid(gpgid):
    match = re.fullmatch(r"\d\d-(\d\d[AB])", gpgid)
    assert match
    pgid_end = match.group(1)
    return "0" + pgid_end


def _make_row(list_of_cell_vals):
    return list_of_cell_vals


def _raw_row_is_real(raw_row):
    if is_real := any(raw_row):
        assert raw_row[0]
        assert any(raw_row[1:])
    return is_real
