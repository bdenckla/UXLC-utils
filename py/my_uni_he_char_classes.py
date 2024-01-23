""" Exports SHSI_DOTS, VOWEL_POINTS, LETTERS, ACCENTS, SPECIALS """


import my_str_defs as sd
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_hebrew_accents as ha


SHSI_DOTS = (
    hpo.SHIND,
    hpo.SIND,
)


VOWEL_POINTS = (
    hpo.SHEVA,
    hpo.XSEGOL,
    hpo.XPATAX,
    hpo.XQAMATS,
    hpo.XIRIQ,
    hpo.TSERE,
    hpo.SEGOL_V,
    hpo.PATAX,
    hpo.QAMATS,
    hpo.QAMATS_Q,
    hpo.XOLAM,
    hpo.XOLAM_XFV,
    hpo.QUBUTS,
)


LETTERS = (
    hl.ALEF,
    hl.BET,
    hl.GIMEL,
    hl.DALET,
    hl.HE,
    hl.VAV,
    hl.ZAYIN,
    hl.XET,
    hl.TET,
    hl.YOD,
    hl.FKAF,
    hl.KAF,
    hl.LAMED,
    hl.FMEM,
    hl.MEM,
    hl.FNUN,
    hl.NUN,
    hl.SAMEKH,
    hl.AYIN,
    hl.FPE,
    hl.PE,
    hl.FTSADI,
    hl.TSADI,
    hl.QOF,
    hl.RESH,
    hl.SHIN,
    hl.TAV,
)

ACCENTS = (
    hpo.METEG,
    ha.ATN,
    ha.SEG_A,
    '\N{HEBREW ACCENT SHALSHELET}',
    '\N{HEBREW ACCENT ZAQEF QATAN}',
    '\N{HEBREW ACCENT ZAQEF GADOL}',
    ha.TIP,
    ha.REV,
    ha.ZARQA_SH,
    ha.PASH,
    '\N{HEBREW ACCENT YETIV}',
    '\N{HEBREW ACCENT TEVIR}',
    ha.GER,
    ha.GER_M,
    ha.GER_2,
    '\N{HEBREW ACCENT QARNEY PARA}',
    ha.TEL_G,
    '\N{HEBREW ACCENT PAZER}',
    ha.ATN_H,
    ha.MUN,
    '\N{HEBREW ACCENT MAHAPAKH}',
    ha.MER,
    '\N{HEBREW ACCENT MERKHA KEFULA}',
    '\N{HEBREW ACCENT DARGA}',
    '\N{HEBREW ACCENT QADMA}',
    ha.TEL_Q,
    ha.YBY,
    ha.OLE,
    '\N{HEBREW ACCENT ILUY}',
    '\N{HEBREW ACCENT DEHI}',
    ha.ZARQA,
)

SPECIALS = (
    '\N{HEBREW MARK UPPER DOT}',
    '\N{HEBREW MARK LOWER DOT}',
    hpo.RAFE,
    hpo.JSVARIKA,
    sd.ZWJ,
)
