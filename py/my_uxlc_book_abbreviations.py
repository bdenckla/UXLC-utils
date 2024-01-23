""" Exports UXLC_BOOK_ABBREVIATIONS. """

import my_tanakh_book_names as tbn

BKNA_MAP_UXLC_TO_STD = {  # not a two-way map! (E.g. 1Chr & 1 Chr)
    'Gen': tbn.BK_GENESIS,
    'Ex': tbn.BK_EXODUS,
    'Lev': tbn.BK_LEVIT,
    'Num': tbn.BK_NUMBERS,
    'Deut': tbn.BK_DEUTER,
    #
    'Josh': tbn.BK_JOSHUA,
    'Judg': tbn.BK_JUDGES,
    # For the 8 entries below, see "note on inversion"
    '1 Sam': tbn.BK_FST_SAM,  # This name "loses" since it is first.
    '2 Sam': tbn.BK_SND_SAM,  # This name "loses" since it is first.
    '1Sam': tbn.BK_FST_SAM,  # This name "wins" since it is last.
    '2Sam': tbn.BK_SND_SAM,  # This name "wins" since it is last.
    '1 Kings': tbn.BK_FST_KGS,  # This name "loses" since it is first.
    '2 Kings': tbn.BK_SND_KGS,  # This name "loses" since it is first.
    '1Kings': tbn.BK_FST_KGS,  # This name "wins" since it is last.
    '2Kings': tbn.BK_SND_KGS,  # This name "wins" since it is last.
    #
    'Isa': tbn.BK_ISAIAH,
    'Jer': tbn.BK_JEREM,
    'Ezek': tbn.BK_EZEKIEL,
    #
    'Hos': tbn.BK_HOSHEA,
    'Joel': tbn.BK_JOEL,
    'Am': tbn.BK_AMOS,
    'Ob': tbn.BK_OVADIAH,
    'Jon': tbn.BK_JONAH,
    'Mic': tbn.BK_MIKHAH,
    # Naḥum
    # Ḥabaqquq
    'Zeph': tbn.BK_TSEF,
    'Hag': tbn.BK_XAGGAI,
    'Zech': tbn.BK_ZEKHAR,
    'Mal': tbn.BK_MALAKHI,
    #
    'Ps': tbn.BK_PSALMS,
    'Prov': tbn.BK_PROV,
    'Job': tbn.BK_JOB,
    #
    'Song': tbn.BK_SONG,
    'Ruth': tbn.BK_RUTH,
    'Lam': tbn.BK_LAMENT,
    'Eccl': tbn.BK_QOHELET,
    'Esth': tbn.BK_ESTHER,
    #
    'Dan': tbn.BK_DANIEL,
    'Ezra': tbn.BK_EZRA,
    'Neh': tbn.BK_NEXEM,
    # For the 4 entries below, see "note on inversion"
    '1 Chr': tbn.BK_FST_CHR,  # This name "loses" since it is first.
    '2 Chr': tbn.BK_SND_CHR,  # This name "loses" since it is first.
    '1Chr': tbn.BK_FST_CHR,  # This name "wins" since it is last.
    '2Chr': tbn.BK_SND_CHR,  # This name "wins" since it is last.
}
# Note on inversion
#
# Below, when trying to invert the mapping above,
# i.e. when forming STD_BKNA_TO_UXLC_BKNA,
# we let the last UXLC name "win".
#
# I.e., "last one wins" is our strategy for inverting the
# not-strictly-invertible UXLC_BKNA_TO_STD_BKNA.
#
BKNA_MAP_STD_TO_UXLC = {
    std: uxlc for uxlc, std in BKNA_MAP_UXLC_TO_STD.items()
}
