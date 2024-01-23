""" Exports read_them_in1 """

import re
import xml.etree.ElementTree
import my_sef_cmn
import my_uxlc_misc_path
import my_uxlc_cvp as cvp
import my_uxlc_lci_rec as lci_rec
import my_xml_node


def read_them_in1():
    """ Return lci_recs: Leningrad Codex Index records """
    lci_rawrecs = _read_raw()
    lci_recs = tuple(map(_make_from_rawrec, lci_rawrecs))
    return lci_recs


def _read_raw():
    xml_input_path = my_uxlc_misc_path.get('LCIndex.xml')
    # Downloaded from https://tanach.us/XSL/LCIndex.xml
    tree = xml.etree.ElementTree.parse(xml_input_path)
    root = tree.getroot()
    root_dic = my_xml_node.to_dic(root)
    bt_tr = root_dic['BODY']['table']['tr']
    td_dics = bt_tr[1:]
    td_tups = tuple(_get_td_tup(dic) for dic in td_dics)
    return td_tups


def _get_td_tup(dic):
    assert tuple(dic.keys()) == ('td',)
    val = dic['td']
    assert isinstance(val, list)
    val1 = _midpad(val)
    assert len(val1) in (3, 4)
    padlen = 4 - len(val1)
    pad = (None,) * padlen
    return tuple(val1) + pad


def _midpad(row):
    row0_vals_to_midpad = {'120B', '121A', '326B'}
    if row[0] in row0_vals_to_midpad:
        assert len(row) == 2
        return [row[0], None, None, row[1]]
    return row


def _make_from_rawrec(lci_rawrec):
    pgid, book, cvp_range_raw, note = lci_rawrec
    assert pgid == _standardize_pgid(pgid)
    bkid = _reformat_book(book)
    cvp_range = _reformat_range(cvp_range_raw)
    return lci_rec.make(pgid, bkid, cvp_range, note)


def _standardize_pgid(raw_pgid):
    leaf_int, ca_or_cb = lci_rec.parse_pgid(raw_pgid)
    return lci_rec.unparse_pgid(leaf_int, ca_or_cb)


def _reformat_range(cvp_range_str):
    if cvp_range_str is None:
        return None
    ccvp = r'(\d+):(\d+)([ab])?'
    # ccvp chapter, colon, verse, part ('a' or 'b' or None)
    # c:v, c:va, c:vb
    patt = f'{ccvp}-{ccvp}'
    match = re.fullmatch(patt, cvp_range_str)
    groups = match.groups()
    start_raw = groups[0:3]
    stop_raw = groups[3:6]
    start = _make_cvp_from_str3(start_raw)
    stop = _make_cvp_from_str3(stop_raw)
    return start, stop


def _make_cvp_from_str3(str3):
    # str3: string triple of chapter, verse, and part.
    # Part is 'a', 'b' or None
    chnu_str, vrnu_str = str3[0:2]
    part_of_verse = str3[2]
    return cvp.make(int(chnu_str), int(vrnu_str), part_of_verse)


def _reformat_book(lci_bkna):
    if lci_bkna is None:
        return None
    sef_bknas = frozenset(my_sef_cmn.SEF_BKNA.values())
    sef_bkna_fr_lci_bkna = {
        # This dict gets a Sefaria book name from an LC Index book name
        '1 Samuel': 'I Samuel',
        '2 Samuel': 'II Samuel',
        '1 Kings': 'I Kings',
        '2 Kings': 'II Kings',
        '1 Chronicles': 'I Chronicles',
        '2 Chronicles': 'II Chronicles',
    }
    sef_bkna = sef_bkna_fr_lci_bkna.get(lci_bkna) or lci_bkna
    assert sef_bkna in sef_bknas
    return _BKID_FR_SEF_BKNA[sef_bkna]


_BKID_FR_SEF_BKNA = {
    sef_bkna: bkid for bkid, sef_bkna in my_sef_cmn.SEF_BKNA.items()}
