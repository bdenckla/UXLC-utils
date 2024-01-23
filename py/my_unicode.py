""" Exports unicode_names, unicode_name """

import unicodedata
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_hebrew_accents as ha


def names(string, separator=' '):
    """ Expand string to code point names. """
    return separator.join(map(name, string))


def name(string_len_1):
    """ Convert string_len_1 to a name elucidation """
    return _SHORT_NAMES.get(string_len_1) or unicodedata.name(string_len_1)


_SHORT_NAMES = {
    '\N{SPACE}': 'space',  # 0020
    '\N{Combining grapheme joiner}': 'combining-grapheme-joiner',  # 034f
    '\N{Zero width joiner}': 'zero-width-joiner',  # 200d
    ha.ATN: 'etnaḥta',  # 0591
    '\N{HEBREW ACCENT Segol}': 'segol-accent',  # 0592
    '\N{HEBREW ACCENT Shalshelet}': 'shalshelet',  # 0593
    '\N{HEBREW ACCENT Zaqef qatan}': 'zaqef-qatan',  # 0594
    '\N{HEBREW ACCENT Zaqef gadol}': 'zaqef-gadol',  # 0595
    ha.TIP: 'tipeḥa/tarḥa',  # 0596
    ha.REV: 'revia',  # 0597
    '\N{HEBREW ACCENT Zarqa}': 'zarqa-stress-helper/tsinorit',  # 0598
    '\N{HEBREW ACCENT Pashta}': 'pashta',  # 0599
    '\N{HEBREW ACCENT Yetiv}': 'yetiv',  # 059a
    '\N{HEBREW ACCENT Tevir}': 'tevir',  # 059b
    ha.GER: 'geresh',  # 059c
    ha.GER_M: 'geresh-muqdam',  # 059d
    ha.GER_2: 'gershayim',  # 059e
    '\N{HEBREW ACCENT Qarney para}': 'qarney-para',  # 059f
    ha.TEL_G: 'telisha-gedola',  # 05a0
    '\N{HEBREW ACCENT Pazer}': 'pazer',  # 05a1
    ha.ATN_H: 'atnaḥ-hafukh',  # 05a2
    ha.MUN: 'munaḥ',  # 05a3
    '\N{HEBREW ACCENT Mahapakh}': 'mahapakh',  # 05a4
    ha.MER: 'merkha/yored',  # 05a5
    '\N{HEBREW ACCENT Merkha kefula}': 'merkha-kefula',  # 05a6
    '\N{HEBREW ACCENT Darga}': 'darga',  # 05a7
    '\N{HEBREW ACCENT Qadma}': 'qadma',  # 05a8
    '\N{HEBREW ACCENT Telisha qetana}': 'telisha-qetana',  # 05a9
    ha.YBY: 'yeraḥ-ben-yomo',  # 05aa
    ha.OLE: 'ole',  # 05ab
    '\N{HEBREW ACCENT Iluy}': 'iluy',  # 05ac
    '\N{HEBREW ACCENT Dehi}': 'deḥi',  # 05ad
    '\N{HEBREW ACCENT Zinor}': 'tsinor',  # 05ae
    hpo.SHEVA: 'sheva',  # 05b0
    hpo.XSEGOL: 'ḥataf-segol',  # 05b1
    hpo.XPATAX: 'ḥataf-pataḥ',  # 05b2
    hpo.XQAMATS: 'ḥataf-qamats',  # 05b3
    hpo.XIRIQ: 'ḥiriq',  # 05b4
    hpo.TSERE: 'tsere',  # 05b5
    hpo.SEGOL_V: 'segol-vowel',  # 05b6
    hpo.PATAX: 'pataḥ',  # 05b7
    hpo.QAMATS: 'qamats',  # 05b8
    hpo.XOLAM: 'ḥolam',  # 05b9
    hpo.XOLAM_XFV: 'ḥolam-ḥaser-for-vav',  # 05ba
    hpo.QUBUTS: 'qubuts',  # 05bb
    hpo.DAGESH_OM: 'dagesh/mapiq/shuruq-dot',  # 05bc
    hpo.METEG: 'meteg/siluq',  # 05bd
    '\N{HEBREW PUNCTUATION Maqaf}': 'maqaf',  # 05be
    hpo.RAFE: 'rafeh',  # 05bf
    '\N{HEBREW PUNCTUATION Paseq}': 'paseq/legarmeih',  # 05c0
    hpo.SHIND: 'shin-dot',  # 05c1
    hpo.SIND: 'sin-dot',  # 05c2
    '\N{HEBREW PUNCTUATION Sof pasuq}': 'sof-pasuq',  # 05c3
    '\N{HEBREW MARK Upper dot}': 'upper-dot',  # 05c4
    '\N{HEBREW MARK Lower dot}': 'lower-dot',  # 05c5
    '\N{HEBREW PUNCTUATION NUN HAFUKHA}': 'nun-hafukha',  # 05c6
    hpo.QAMATS_Q: 'qamats-qatan',  # 05c7
    hl.ALEF: 'alef',  # 05d0
    hl.BET: 'bet',  # 05d1
    hl.GIMEL: 'gimel',  # 05d2
    hl.DALET: 'dalet',  # 05d3
    hl.HE: 'he',  # 05d4
    hl.VAV: 'vav',  # 05d5
    hl.ZAYIN: 'zayin',  # 05d6
    hl.XET: 'ḥet',  # 05d7
    hl.TET: 'tet',  # 05d8
    hl.YOD: 'yod',  # 05d9
    hl.FKAF: 'final-kaf',  # 05da
    hl.KAF: 'kaf',  # 05db
    hl.LAMED: 'lamed',  # 05dc
    hl.FMEM: 'final-mem',  # 05dd
    hl.MEM: 'mem',  # 05de
    hl.FNUN: 'final-nun',  # 05df
    hl.NUN: 'nun',  # 05e0
    hl.SAMEKH: 'samekh',  # 05e1
    hl.AYIN: 'ayin',  # 05e2
    hl.FPE: 'final-pe',  # 05e3
    hl.PE: 'pe',  # 05e4
    hl.FTSADI: 'final-tsadi',  # 05e5
    hl.TSADI: 'tsadi',  # 05e6
    hl.QOF: 'qof',  # 05e7
    hl.RESH: 'resh',  # 05e8
    hl.SHIN: 'shin',  # 05e9
    hl.TAV: 'tav',  # 05ea
    hpo.JSVARIKA: 'varika',
}
