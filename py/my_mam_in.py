"""
Exports:
    Minirow
    MinirowExt
    read_books_from_mam_parsed
    read_mam_parsed
    read_section_from_csv_lightly
    csv_path
"""
import csv
import json
import collections

import my_utils
import my_hebrew_verse_numerals as hvn
import my_tanakh_book_names as tbn
import my_mam_book_names
import my_mam_wiki_tmpl_n_tag_parser as ttp
import my_mam_book_names_and_std_book_names as mbkn_a_sbkn
import my_mam_wiki_tmpl as wtp1


def read_books_from_mam_parsed(bk39ids=None, plus_or_plain='plus'):
    """ Read all bk24s covering bk39ids """
    real_bk39ids = bk39ids or tbn.ALL_BOOK_IDS
    books_out = {}
    for bk24id in _bk24ids(real_bk39ids):
        folder = f'../MAM-parsed/{plus_or_plain}'
        in_path = f'{folder}/{bk24id}.json'
        read_mam_parsed(in_path, books_out, plus_or_plain)
    return books_out


def read_section_from_csv_lightly(section_name, mam_info=None):
    """ Read a single section "lightly" (without much processing) """
    light_books_out = {}
    _read_csv_lightly(section_name, light_books_out, mam_info)
    return light_books_out


def csv_path(section_name, alt_mam_dir=None):
    """ Return path to CSV file for the named section. """
    csv_name = _MAM_CSV_NAME[section_name]
    mam_dir = alt_mam_dir or 'in/mam-go'
    return mam_dir + '/' + csv_name


_ROW = collections.namedtuple('_ROW', 'A, B, C, D, E')
# Below is good for debugging since it has unparsed (raw string) cells C & E
# Minirow = collections.namedtuple('Minirow', 'C, D, E, CP, EP')
Minirow = collections.namedtuple('Minirow', 'CP, DP, EP')
MinirowExt = collections.namedtuple('MinirowExt', 'CP, DP, EP, next_CP')
_CSV_TORAH = 'Miqra_al_pi_ha-Masorah - תורה.csv'
_CSV_NEV_RISH = 'Miqra_al_pi_ha-Masorah - נביאים ראשונים.csv'
_CSV_NEV_AX = 'Miqra_al_pi_ha-Masorah - נביאים אחרונים.csv'
_CSV_SIF_EM = 'Miqra_al_pi_ha-Masorah - ספרי אמ_ת.csv'  # See note below
_CSV_XAM_MEG = 'Miqra_al_pi_ha-Masorah - חמש מגילות.csv'
_CSV_KET_ACH = 'Miqra_al_pi_ha-Masorah - כתובים אחרונים.csv'
# The double quote in the tab name ספרי אמ"ת becomes an underscore
# in the file name of the file that results from downloading that tab.
# (The double quote itself "should" be a gershayim.)
_MAM_CSV_NAME = {
    tbn.SEC_TORAH: _CSV_TORAH,
    tbn.SEC_NEV_RISH: _CSV_NEV_RISH,
    tbn.SEC_NEV_AX: _CSV_NEV_AX,
    tbn.SEC_SIF_EM: _CSV_SIF_EM,
    tbn.SEC_XAM_MEG: _CSV_XAM_MEG,
    tbn.SEC_KET_ACH: _CSV_KET_ACH,
}


def _bk24ids(bk39ids):
    # We use a dic to preserve order
    dic = {tbn.bk24id(bk39id): 1 for bk39id in bk39ids}
    return tuple(dic.keys())


# XXX TODO: what is the maximum verse number?

def read_mam_parsed(in_path, io_books, plus_or_plain):
    """ Read MAM-parsed JSON at in_path into io_books. """
    # book39: a book in the "1 of 39" division of books
    with open(in_path, encoding='utf-8') as json_in_fp:
        sec = json.load(json_in_fp)
    for book39 in sec['book39s']:
        he_bn_sbn = book39['book24_name'], book39['sub_book_name']
        bkid = mbkn_a_sbkn.MAM_BNP_TO_BKID[he_bn_sbn]
        out_book = _initial_book(book39, plus_or_plain)
        _read_mam_parsed_chapters(
            book39['chapters'], out_book, plus_or_plain)
        my_utils.init(io_books, bkid, out_book)


def _initial_book(book39, plus_or_plain):
    initial_book = {}
    if plus_or_plain == 'plus':
        initial_book['good_ending'] = _convert_ge(book39['good_ending'])
    else:
        assert plus_or_plain == 'plain'
        initial_book['good_ending'] = _good_ending(book39['chapters'])
    initial_book['verses'] = {}
    return initial_book


def _good_ending(chapters):
    last_he_chnu = tuple(chapters.keys())[-1]
    last_chapter = chapters[last_he_chnu]
    # Good endings are always wrapped in doc templates,
    # and they are the only thing in the CP of a triple-tav row
    # that is wrapped in a doc template.
    minirow = _make_mre(last_chapter['תתת'], 'plain')
    for wtel in minirow.CP:
        if wtp1.is_doc_template(wtel):
            return wtel
    return None


def _convert_ge(good_ending):
    if good_ending is None:
        return None
    out_ge = dict(good_ending)
    he_chnu = good_ending['last_chapnver'][0]
    he_vrnu = good_ending['last_chapnver'][1]
    out_ge['last_chapnver'] = tbn.mk_cvtmam(
        hvn.STR_TO_INT_DIC[he_chnu],
        hvn.STR_TO_INT_DIC[he_vrnu])
    return out_ge


def _read_mam_parsed_chapters(chapters, io_book, plus_or_plain):
    # psv_psn: pseudo-verse's pseudo-number (0, 1..N, תתת)
    # psv_contents: pseudo-verse contents: a 3-element list,
    #     with the elements being cells C, D, & E, in parsed form.
    # cvt: c, v, t
    #     c: chapter number (integer)
    #     v: verse number (integer)
    #     t: vtrad (versification tradition)
    #        (t is always VT_MAM in this context)
    for he_chnu, ch_contents in chapters.items():
        for psv_psn, psv_contents in ch_contents.items():
            minirow = _make_mre(psv_contents, plus_or_plain)
            if psv_psn not in ('0', 'תתת'):
                int_vrnu = hvn.STR_TO_INT_DIC[psv_psn]
                int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
                cvt = tbn.mk_cvtmam(int_chnu, int_vrnu)
                my_utils.init(io_book['verses'], cvt, minirow)


def _make_mre(psv_contents, plus_or_plain):
    # Make an extended minirow based on
    # psv_contents (the pseudo-verse's contents).
    #
    # First thing to do is to go from a list of lists to a list of tuples:
    assert isinstance(psv_contents, list)
    for something_p in psv_contents:  # something_p: CP, DP, EP, or next_CP
        assert isinstance(something_p, list)
    the_list = list(map(tuple, psv_contents))
    # Second (and final) thing to do is to actually construct
    # the Minirow or MinirowExt:
    if plus_or_plain == 'plus':
        return MinirowExt(*the_list)
    assert plus_or_plain == 'plain'
    return Minirow(*the_list)


# he_pverse_pnum: Hebrew pseudo-verse pseudo-numeral
# We call it a pseudo-numeral because it is not always a real Hebrew numeral:
#    it can be 0 or תתת (zero or triple-tav)
# We call it a pseudo-verse because it is not always a real verse:
#    it can be
#       chapter-start contents (pnum 0) or
#       chapter-end contents (pnum תתת)

def _read_csv_lightly(section_name, io_light_books, mam_info=None):
    alt_mam_dir = mam_info and mam_info['dir']
    the_csv_path = csv_path(section_name, alt_mam_dir)
    with open(the_csv_path, encoding='utf-8') as csv_in_fp:
        for row in map(_ROW._make, csv.reader(csv_in_fp)):
            skip_hccs = mam_info and mam_info.get('skip_hard_c_cells')
            light_keys, minirow = _process_one_row_lightly(row, skip_hccs)
            he_bn_sbn, he_chnu, he_pverse_pnum = light_keys
            if he_pverse_pnum == '0':
                if he_chnu == 'א':
                    my_utils.init(io_light_books, he_bn_sbn, {})
                my_utils.init(io_light_books[he_bn_sbn], he_chnu, {})
            my_utils.init(
                io_light_books[he_bn_sbn][he_chnu], he_pverse_pnum, minirow)


def _process_one_row_lightly(row, skip_hard_c_cells):
    he_bn_sbn, he_chnu = _he_bn_sbn_chnu(row.A)
    light_keys = he_bn_sbn, he_chnu, row.B
    c_parsed = _parse_cell_c(light_keys, row.C, skip_hard_c_cells)
    d_parsed = ttp.parse(row.D)
    e_parsed = ttp.parse(row.E)
    return light_keys, Minirow(c_parsed, d_parsed, e_parsed)


def _parse_cell_c(light_keys, cell_c, skip_hard_c_cells):
    # If the cell for column C is too hard to parse in this particular row
    if skip_hard_c_cells and light_keys in _LIGHT_KEYS_WITH_HARD_CELL_C:
        return ({'unparseable': True},)
    return ttp.parse(cell_c)


_LIGHT_KEYS_WITH_HARD_CELL_C = set((  # "hard" meaning "too hard to parse"
    # (miqra_book_names.BS_EXODUS, str('טו'), 'תתת'),
    (my_mam_book_names.BS_DEUTER, str('לב'), 'תתת'),
    (my_mam_book_names.BS_JOSHUA, str('יב'), 'תתת'),
    (my_mam_book_names.BS_JUDGES, str('ה'), 'תתת'),
    (my_mam_book_names.BS_SND_SAM, str('כב'), 'תתת'),
    (my_mam_book_names.BS_QOHELET, str('ג'), 'תתת'),
    (my_mam_book_names.BS_ESTHER, str('ט'), 'תתת'),
    (my_mam_book_names.BS_FST_CHR, str('טז'), 'תתת'),
))


# The following 5 book24s are the only ones with sub-books:
#    Samuel, Kings, & Chronicles (2 sub-books each)
#    Ezra-Nehemiah (2 sub-books)
#    The 12 minor prophets (12 sub-books)
# Note that names of the sub-books of Samuel, Kings, & Chronicles
#    are not just 'א' or 'ב'.
# The names of those sub-books also contain their book24 name,
#    in an abbreviated form.
# E.g. the 1st half of Samuel is notated as 'שמ"א', not just 'א'.
# I.e. 'שמ"א' is an abbreviated form of 'שמואל א'.
# Considering cell A as a whole, this gives cell A some redundancy,
#    for such books.
# E.g. cell A might be 'ספר שמואל/שמ"א ג' (sefer shmuel/shm1 3)
#    (some redundancy).
# Or, cell A might simply be 'ספר בראשית/ג' (sefer bereshit/3)
#    (no redundancy).
# Such redundancy is not necessarily a bad thing.
# For one thing, for book24s with sub-books, it means you can
#    just ignore the book24 name, in many contexts, since the
#    sub-book name is unique.

def _he_bn_sbn_chnu(cell_a):
    #
    # An input of 'book24/sub_book chap_num', e.g. 'ספר שמואל/שמ"א ג'
    #    gives an output of book24, sub_book, chap_num
    #    e.g. (str('ספר שמואל'), str('שמ"א')), str('ג')
    # An input of 'book24/chap_num', e.g. 'ספר בראשית/ג'
    #    gives an output of book24, None, chap_num
    #    e.g. str('ספר בראשית'), None, str('ג')
    # Below, he_chap_id is something like 'ג' or 'שמ"א ג'.
    # I.e. it can be a he_cn_str (Hebrew cn string)
    #    where cn means chapter number.
    # Or, it can be a he_sbncn_str (Hebrew sbncn string)
    #    where sbncn means sub-book name and chapter num.
    # If he_chap_id is
    #    'ג', that means chapter 3
    #     of a book without sub-books, like Genesis.
    # If he_chap_id is
    #    'שמ"א ג', that means chapter 3
    #    of the the sub-book 'שמ"א' of the book of Samuel.
    #
    he_book_name, he_chap_id = cell_a.split('/')
    maybe_sbncn = he_chap_id.split()
    if len(maybe_sbncn) == 2:
        sbncn = maybe_sbncn
        return (he_book_name, sbncn[0]), sbncn[1]
    assert len(maybe_sbncn) == 1
    chap_num = he_chap_id
    return (he_book_name, None), chap_num
