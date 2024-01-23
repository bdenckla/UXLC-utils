"""
This module provides maps (dicts) in both directions between:

    a standard book name like '1Samuel'
    and
    a MAM book name pair like (str('ספר שמואל'), str('שמ"א'))

Note that MAM book names are pairs!
I.e., MAM book names are tuples of length 2.
"""
import my_mam_book_names
import my_tanakh_book_names as tbn


def _flip(pair):
    return pair[1], pair[0]


_PAIRS = (
    (my_mam_book_names.BS_GENESIS, tbn.BK_GENESIS),
    (my_mam_book_names.BS_EXODUS, tbn.BK_EXODUS),
    (my_mam_book_names.BS_LEVIT, tbn.BK_LEVIT),
    (my_mam_book_names.BS_NUMBERS, tbn.BK_NUMBERS),
    (my_mam_book_names.BS_DEUTER, tbn.BK_DEUTER),
    (my_mam_book_names.BS_JOSHUA, tbn.BK_JOSHUA),
    (my_mam_book_names.BS_JUDGES, tbn.BK_JUDGES),
    (my_mam_book_names.BS_FST_SAM, tbn.BK_FST_SAM),
    (my_mam_book_names.BS_SND_SAM, tbn.BK_SND_SAM),
    (my_mam_book_names.BS_FST_KGS, tbn.BK_FST_KGS),
    (my_mam_book_names.BS_SND_KGS, tbn.BK_SND_KGS),
    (my_mam_book_names.BS_ISAIAH, tbn.BK_ISAIAH),
    (my_mam_book_names.BS_JEREM, tbn.BK_JEREM),
    (my_mam_book_names.BS_EZEKIEL, tbn.BK_EZEKIEL),
    (my_mam_book_names.BS_HOSEA, tbn.BK_HOSHEA),
    (my_mam_book_names.BS_JOEL, tbn.BK_JOEL),
    (my_mam_book_names.BS_AMOS, tbn.BK_AMOS),
    (my_mam_book_names.BS_OBADIAH, tbn.BK_OVADIAH),
    (my_mam_book_names.BS_JONAH, tbn.BK_JONAH),
    (my_mam_book_names.BS_MICAH, tbn.BK_MIKHAH),
    (my_mam_book_names.BS_NAXUM, tbn.BK_NAXUM),
    (my_mam_book_names.BS_XABA, tbn.BK_XABA),
    (my_mam_book_names.BS_TSEF, tbn.BK_TSEF),
    (my_mam_book_names.BS_XAGGAI, tbn.BK_XAGGAI),
    (my_mam_book_names.BS_ZEKHAR, tbn.BK_ZEKHAR),
    (my_mam_book_names.BS_MALAKHI, tbn.BK_MALAKHI),
    (my_mam_book_names.BS_PSALMS, tbn.BK_PSALMS),
    (my_mam_book_names.BS_PROV, tbn.BK_PROV),
    (my_mam_book_names.BS_JOB, tbn.BK_JOB),
    (my_mam_book_names.BS_SONG, tbn.BK_SONG),
    (my_mam_book_names.BS_RUTH, tbn.BK_RUTH),
    (my_mam_book_names.BS_LAMENT, tbn.BK_LAMENT),
    (my_mam_book_names.BS_QOHELET, tbn.BK_QOHELET),
    (my_mam_book_names.BS_ESTHER, tbn.BK_ESTHER),
    (my_mam_book_names.BS_DANIEL, tbn.BK_DANIEL),
    (my_mam_book_names.BS_EZRA, tbn.BK_EZRA),
    (my_mam_book_names.BS_NEXEM, tbn.BK_NEXEM),
    (my_mam_book_names.BS_FST_CHR, tbn.BK_FST_CHR),
    (my_mam_book_names.BS_SND_CHR, tbn.BK_SND_CHR),
)

BKID_TO_MAM_BNP = dict(map(_flip, _PAIRS))
MAM_BNP_TO_BKID = dict(_PAIRS)
