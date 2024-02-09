""" Exports get_it. """

import my_tanakh_book_names as tbn
import my_uxlc_book_abbreviations as u_bk_abbr

_WLC_BKID_TO_STD_BKID = {
    'gn': tbn.BK_GENESIS,
    'ex': tbn.BK_EXODUS,
    'js': tbn.BK_JOSHUA,
    'ju': tbn.BK_JUDGES,
    '1s': tbn.BK_FST_SAM,
    '2s': tbn.BK_SND_SAM,
    '1k': tbn.BK_FST_KGS,
    '2k': tbn.BK_SND_KGS,
    'is': tbn.BK_ISAIAH,
    'je': tbn.BK_JEREM,
    'ek': tbn.BK_EZEKIEL,
    'pr': tbn.BK_PROV,
    'lm': tbn.BK_LAMENT,
    'es': tbn.BK_ESTHER,
    'da': tbn.BK_DANIEL,
    'er': tbn.BK_EZRA,
}


def get_it(wlc_bcv_str):
    """ Return tanach.us URL for WLC bcv string (bcv: book, chapter, & verse) """
    wlc_bkid = wlc_bcv_str[:2]
    std_bkid = _WLC_BKID_TO_STD_BKID[wlc_bkid]
    uxlc_bkid = u_bk_abbr.BKNA_MAP_STD_TO_UXLC[std_bkid]
    wlc_cv_str = wlc_bcv_str[2:]
    uxlc_bcv_str = uxlc_bkid + wlc_cv_str
    return f'https://tanach.us/Tanach.xml?{uxlc_bcv_str}'
