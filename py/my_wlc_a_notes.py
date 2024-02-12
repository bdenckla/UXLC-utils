""" Exports RECORDS. """

_WLC_C_BRACKET_NOTE_DEFINITION = \
    "We read an accent in ל differently from BHS. "+ \
    "(This is similar to the note “]C”, "+ \
    "but the latter refers to accent differences against BHQ.)"
_WLC_1_BRACKET_NOTE_DEFINITION = \
    "BHS has been faithful to ל [...] "+ \
    "where there might be a question of the validity of the form "+ \
    "and we keep the same form as BHS. "+ \
    "(This is similar to the note “]U”, but the latter refers to cases where "+ \
    "BHQ has been published and we keep the same form as both BHS and BHQ.)"

RECORD_01 = {
    'wlc-index': 1,
    'uxlc-change-proposal': 101,
    'bcv': 'gn27:29',
    'Dotan': '∅',
    'qere': 'וְיִֽשְׁתַּחֲו֤וּ',
    'MPK': 'וְיִֽשְׁתַּחֲוֻ֤',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
    'side-notes': [
        'Dotan notes a later version of this word in this verse, וְיִשְׁתַּחֲוּ֥וּ. '+
        'Presumably he notes this later word for the unexpected dagesh in its penultimate vav. '+
        'This later word is a normal (non-qere) word.'
    ]
}
RECORD_02 = {
    'wlc-index': 2,
    'uxlc-change-proposal': 102,
    'bcv': 'gn43:28',
    'Dotan': '∅',
    'qere': 'וַיִּֽשְׁתַּחֲוּֽוּ׃',
    'MPK': 'וַיִּֽשְׁתַּחֲוֻּֽ׃',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
    'side-notes': [
        'In WLC, this word also has a 1-note, '+
        'presumably because of the unexpected dagesh in the qere’s penultimate vav. ',
        #
        'As a reminder, a WLC 1-note (bracket-1 note) is defined as follows: '+
        f'«{_WLC_1_BRACKET_NOTE_DEFINITION}»',
        #
        'Although Dotan notes this word, '+
        'I do not take him to have noted it for the issue at hand: '+
        'the qubuts-to-shuruq issue. '+
        'I take him to have noted this word '+
        'only for its unexpected dagesh in the qere’s penultimate vav. '+
        'Compare to gn27:29 word 4, וְיִֽשְׁתַּחֲו֤וּ, not noted by Dotan, '+
        'which is the qere of a ketiv/qere that is analogous to this one '+
        'except it has the expected undageshed penultimate vav. '+
        'Also compare to gn27:29 word 10, וְיִשְׁתַּחֲוּ֥וּ, noted by Dotan, '+
        'which is a normal (non-qere) word that is analogous to this qere '+
        'including its unexpected dageshed penultimate vav.'
    ],
}
RECORD_03 = {
    'wlc-index': 3,
    'uxlc-change-proposal': 201,
    'bcv': 'ex4:2',
    'Dotan': '∅',
    'qere': 'מַה־זֶּ֣ה',
    'qere-atom': 'מַה־',
    'MPK': 'מַזֶּ֣ה',
    'at issue': '־',
    'summary': '+mqf',
    'remarks': [],
}
RECORD_04 = {
    'wlc-index': 4,
    'uxlc-change-proposal': 301,
    'bcv': 'js22:7',
    'Dotan': '✓',
    'qere': 'בְּעֵ֥בֶר',
    'MPK': 'מְעֵ֥בֶר',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s מ does not carry a dagesh for the qere’s ב, for some reason. '+
        'This is the dual of js24:15. '+
        'Dotan notes that strictly speaking, the implied qere is '+
        'בְעֵ֥בֶר (unexpectedly dagesh-free).'
    ],
}
RECORD_05 = {
    'wlc-index': 5,
    'uxlc-change-proposal': 302,
    'bcv': 'js24:15',
    'Dotan': '✓',
    'qere': 'מֵעֵ֣בֶר',
    'MPK': 'בְּעֵ֥בֶר',
    'at issue': 'מ',
    'summary': '-dgsh',
    'remarks': [
        'The MPK’s בּ seems to carry a dagesh for the qere’s מ but it is rejected. '+
        'This is the dual of js22:7. '+
        'Dotan notes that strictly speaking, the implied qere is מֵּעֵ֣בֶר (unexpectedly dageshed).'
    ],
}
RECORD_06 = {
    'wlc-index': 6,
    'uxlc-change-proposal': 401,
    'bcv': 'ju20:13',
    'Dotan': '∅',
    'qere': 'בְּנֵ֣י',
    'MPK': (
        '\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}'+
        '\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}'
    ),
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב. '+
        'The MPK (points on no letters) is sheva, tsere, and munaḥ.',
    ],
    'side-notes': [
        'Why in the margin does it say not only «בני קר ולא כת» but also «בני ק»?',
        #
        'Dotan notes that the next word unexpectedly starts with בּ not ב, '+
        'i.e. בִנְיָמִ֔ן would be expected.'
    ],
}
RECORD_07 = {
    'wlc-index': 7,
    'uxlc-change-proposal': 103,
    'bcv': 'ju21:20',
    'Dotan': '∅',
    'qere': 'וַיְצַוּ֕וּ',
    'MPK': 'וַיְצַוֻּ֕',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
}
RECORD_08 = {
    'wlc-index': 8,
    'uxlc-change-proposal': 501,
    'bcv': '1s5:6',
    'Dotan': '∅',
    'qere': 'בַּטְּחֹרִ֔ים',
    'MPK': 'בַּעְפֹלִ֔ים',
    'at issue': 'טּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ע does not carry a dagesh for the qere’s ט, '+
        'perhaps because that would be illegal.',
    ],
    'side-notes': [
        'Same issue, indeed same word modulo accent, six verses later, in 5:12. '+
        'See «Dotan page xx» in tab called «Comments.»'
    ],
}
RECORD_09 = {
    'wlc-index': 9,
    'uxlc-change-proposal': 502,
    'bcv': '1s5:12',
    'Dotan': '∅',
    'qere': 'בַּטְּחֹרִ֑ים',
    'MPK': 'בַּעְפֹלִ֑ים',
    'at issue': 'טּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ע does not carry a dagesh for the qere’s ט, '+
        'perhaps because that would be illegal.',
    ],
    'side-notes': [
        'Same issue, indeed same word modulo accent, six verses before, in 5:6. '+
        'See «Dotan page xx» in tab called «Comments.»'
    ],
}
RECORD_10 = {
    'wlc-index': 10,
    'uxlc-change-proposal': '2024.04.01/2024.01.14-1',
    'bcv': '1s9:1',
    'Dotan': '✓',
    'qere': 'מִבִּנְיָמִ֗ין',
    'MPK': 'מִבִּן־יָמִ֗ין',
    'at issue': 'נְיָ',
    'summary': '+shva,-mqf',
    'remarks': [
        'The MPK’s final nun of מבן does not carry a sheva for the qere’s (non-final) נ, '+
        'perhaps because that would be illegal. '+
        'The maqaf disappears when going from the MPK to the qere. '+
        'Dotan notes that strictly speaking, the implied qere is '+
        'מִבִּניָמִ֗ין (no sheva under middle נ).'
    ],
}
RECORD_11 = {
    'wlc-index': 11,
    'uxlc-change-proposal': 104,
    'bcv': '1s12:10',
    'Dotan': '∅',
    'qere': 'וַיֹּאמְר֣וּ',
    'MPK': 'וַיֹּאמְרֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
}
RECORD_12 = {
    'wlc-index': 12,
    'uxlc-change-proposal': 105,
    'bcv': '1s13:19',
    'Dotan': '∅',
    'qere': 'אָמְר֣וּ',
    'MPK': 'אָמְרֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
    'side-notes': [
        'There’s a large, clear dot above the ר; '+
        'I don’t know what it is supposed to mean, if anything. '+
        'Surely not a revia!'
    ],
}
RECORD_13 = {
    'wlc-index': 13,
    'uxlc-change-proposal': 507,
    'bcv': '1s17:23',
    'Dotan': '✓',
    'qere': 'מִמַּעַרְכ֣וֹת',
    'MPK': 'מִמַּעֲרְ֣וֹת',
    'at issue': 'עַ',
    'summary': 'ḥtf ptḥ to ptḥ',
    'remarks': [
        'The MPK’s ע does not carry a pataḥ for the qere’s ע, '+
        'perhaps because that would be illegal. '+
        'It carries a ḥataf pataḥ. '+
        'Dotan notes that strictly speaking, the implied qere is '+
        'מִמַּעֲרְכ֣וֹת (ḥataf pataḥ under ע).'
    ],
}
RECORD_14 = {
    'wlc-index': 14,
    'uxlc-change-proposal': 402,
    'bcv': '2s3:2',
    'Dotan': '∅',
    'qere': 'וַיִּוָּלְד֧וּ',
    'MPK': 'וַיִּ\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}לְד֧וּ',
    'at issue': 'וָּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s vav-qamats.',
    ],
    'side-notes': [
        'Although it cannot carry the vav’s dagesh, '+
        'the ל carries the vav’s qamats as well as its own sheva. '
        'Unlike the manuscript, our MPK shows that qamats on a dotted circle rather than on the ל.'
    ],
}
RECORD_15 = {
    'wlc-index': 15,
    'uxlc-change-proposal': 403,
    'bcv': '2s8:3',
    'Dotan': '∅',
    'qere': 'פְּרָֽת׃',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{HEBREW POINT METEG}׃',
    'at issue': 'פּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s פ. '+
        'The MPK (points on no letters) is sheva, qamats, and siluq.'
    ],
}
RECORD_16 = {
    'wlc-index': 16,
    'uxlc-change-proposal': '2024.04.01/2024.01.18-2',
    'bcv': '2s18:20',
    'Dotan': '✓',
    'qere': 'עַל־כֵּ֥ן',
    'qere-atom': 'עַל־',
    'MPK': 'עַלֵ֥',
    'at issue': '־',
    'summary': '+mqf',
    'remarks': [
        'The MPK lacks a trailing maqaf. '+
        'The MPK (points on no letters) is tsere and merkha. '+
        'Well really those points are under ל not under nothing.',
        #
        'Dotan notes that strictly speaking, the implied qere is עַל כֵ֥ן. '+
        'I think what he finds notable here is the MPK’s lack of a maqaf. '+
        'I do not think he finds the MPK’s lack of dagesh notable because as far as I know, '+
        'such a dagesh is never present.',
    ],
    'side-notes': [
        'Why is this not considered a qere velo ketiv by WLC? '+
        'I have submitted a change proposal to UXLC to make it a qere velo ketiv.'
    ],
}
RECORD_40 = {
    'wlc-index': 16,  # not unique! (two 16s)
    'uxlc-change-proposal': 412,
    'bcv': '2s18:20',
    'Dotan': '✓',
    'qere': 'עַל־כֵּ֥ן',
    'qere-atom': 'כֵּ֥ן',
    'MPK': 'עַלֵ֥',
    'at issue': 'כּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s כ. '+
        'The MPK (points on no letters) is tsere and merkha. '+
        'Well really those points are under ל not under nothing.',
        #
        'Dotan notes that strictly speaking, the implied qere is עַל כֵ֥ן. '+
        'I think what he finds notable here is the MPK’s lack of a maqaf. '+
        'I do not think he finds the MPK’s lack of dagesh notable because as far as I know, '+
        'such a dagesh is never present.'
    ],
}
RECORD_17 = {
    'wlc-index': 17,
    'uxlc-change-proposal': 404,
    'bcv': '2s21:9',
    'Dotan': '∅',
    'qere': 'בִּתְחִלַּ֖ת',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}תְחִלַּ֖ת',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב.',
        #
        'Although it cannot carry ב’s dagesh, the initial ת could carry the ב’s ḥiriq as well as its own sheva. '+
        'Yet, it does not: the spacing is generous, leaving the ḥiriq floating out on its own without a parent letter. '+
        'Unlike the manuscript, our MPK shows that ḥiriq on a dotted circle rather than floating out on its own.'
    ],
}
RECORD_18 = {
    'wlc-index': 18,
    'uxlc-change-proposal': 405,
    'bcv': '2s22:8',
    'Dotan': '∅',
    'qere': 'וַיִּתְגָּעַ֤שׁ',
    'MPK': 'וַ\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}תְגָּעַ֤שׁ',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.',
        #
        'Although it cannot carry the yod’s dagesh, the vav carries its own pataḥ as well as the yod’s ḥiriq. '
        'Unlike the manuscript, our MPK shows that ḥiriq on a dotted circle rather than on the vav.'
    ],
}
RECORD_19 = {
    'wlc-index': 19,
    'uxlc-change-proposal': 503,
    'bcv': '1k7:45',
    'Dotan': '∅',
    'qere': 'הָאֵ֔לֶּה',
    'MPK': 'הָאֵ֔הֶה',
    'at issue': 'לּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ה does not carry a dagesh for the qere’s ל, '+
        'perhaps because that would be illegal.'
    ],
}
RECORD_20 = {
    'wlc-index': 20,
    'uxlc-change-proposal': None,
    'bcv': '1k9:9',
    'Dotan': '∅',
    'qere': 'וַיִּשְׁתַּחֲו֥וּ',
    'MPK': 'וַיִּשְׁתַּחֲוּ֥',
    'at issue': '?',
    'summary': '?',
    'remarks': [
        'The MPK has all the qere’s marks so I don’t see what the issue is. '+
        'The suffix וּ֥ becomes ו֥וּ. '+
        'I would have expected a qubuts in the MPK, but this notation works, too, '+
        'as long as we interpret the MPK’s dot in the vav to be a shuruq dot not a dagesh.'
    ],
}
RECORD_21 = {
    'wlc-index': 21,
    'uxlc-change-proposal': 106,
    'bcv': '1k12:7',
    'Dotan': '∅',
    'qere': 'וַיְדַבְּר֨וּ',
    'MPK': 'וַיְדַבְּרֻ֨',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
    'side-notes': [
        'In WLC, this word also has a c-note, '+
        'presumably because WLC has qadma where BHS (in error) has pashta.',
        #
        'As a reminder, a WLC c-note (bracket-c note) is defined as follows: '+
        f'«{_WLC_C_BRACKET_NOTE_DEFINITION}»'],
}
RECORD_22 = {
    'wlc-index': 22,
    'uxlc-change-proposal': 504,
    'bcv': '2k4:3',
    'Dotan': '∅',
    'qere': 'שְׁכֵנָ֑יִךְ',
    'MPK': 'שְׁכֵנָ֑כִי',
    'at issue': 'ךְ',
    'summary': '+shva',
    'remarks': [
        'The MPK’s yod does not carry a sheva for the qere’s ך, '+
        'perhaps because that would be illegal.'
    ],
}
RECORD_23 = {
    'wlc-index': 23,
    'uxlc-change-proposal': 505,
    'bcv': '2k6:25',
    'Dotan': '∅',
    'qere': 'דִּבְיוֹנִ֖ים',
    'MPK': 'חִרְייֹונִ֖ים',
    'at issue': 'דּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ח does not carry a dagesh for the qere’s ד, '+
        'perhaps because that would be illegal.',
    ],
    'side-notes': [
        'the ḥolam malei dot on the qere’s vav comes from the ḥolam (ḥaser?) dot on the yod of the MPK! '+
        'Instead of being on the yod of the MPK, '+
        'why isn’t this dot on the vav of the MPK?'
    ],
}
RECORD_24 = {
    'wlc-index': 24,
    'uxlc-change-proposal': 470,
    'bcv': '2k19:31',
    'Dotan': '∅',
    'qere': 'צְבָא֖וֹת',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW ACCENT TIPEHA}',
    'at issue': 'וֹ',
    'summary': '+ḥlm dt',
    'remarks': [
        'The MPK has no letter to carry a ḥolam dot on the qere’s vav. '+
        'The MPK (points on no letters) is sheva, qamats, and tipeḥa.'
    ],
}
RECORD_25 = {
    'wlc-index': 25,
    'uxlc-change-proposal': 406,
    'bcv': '2k19:37',
    'Dotan': '∅',
    'qere': 'בָּנָיו֙',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב. '+
        'The MPK (points on no letters) is two qamats marks and (what we intepret as) pashta (not qadma).',
    ],
    'side-notes': [
        'There is also a dot near the pashta, which we ignore. '+
        'I.e. we assume it is not ink, or in any case not intentional.'
    ],
}
RECORD_26 = {
    'wlc-index': 26,
    'uxlc-change-proposal': 107,
    'bcv': '2k20:18',
    'Dotan': '∅',
    'qere': 'יִקָּ֑חוּ',
    'MPK': 'יִקָּ֑חֻ',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
    'side-notes': [
        'The dagesh in the qof is way off center, but still legit IMO.'
    ],
}
RECORD_27 = {
    'wlc-index': 27,
    'uxlc-change-proposal': 303,
    'bcv': '2k23:33',
    'Dotan': '∅',
    'qere': 'מִמְּלֹ֖ךְ',
    'MPK': 'בִּמְּלֹ֖ךְ',
    'at issue': 'מ',
    'summary': '-dgsh',
    'remarks': [
        'The MPK’s בּ seems to carry a dagesh for the qere’s מ but it is rejected. '+
        'See js24:15, which is similar. '+
        'Dotan does not note this case, though he does note js24:15.'
    ],
}
RECORD_28 = {
    'wlc-index': 28,
    'uxlc-change-proposal': 202,
    'bcv': 'is3:15',
    'Dotan': '∅',
    'qere': 'מַה־לָּכֶם֙',
    'qere-atom': 'מַה־',
    'MPK': 'מַלָּכֶם֙',
    'at issue': '־',
    'summary': '+mqf',
    'remarks': [],
}
RECORD_29 = {
    'wlc-index': 29,
    'uxlc-change-proposal': 203,
    'bcv': 'je18:3',
    'Dotan': '∅',
    'qere': 'וְהִנֵּה־ה֛וּא',
    'qere-atom': 'וְהִנֵּה־',
    'MPK': 'וְהִנֵּה֛וּ',
    'at issue': '־',
    'summary': '+mqf',
    'remarks': [],
}
RECORD_30 = {
    'wlc-index': 30,
    'uxlc-change-proposal': 407,
    'bcv': 'je31:38',
    'Dotan': '∅',
    'qere': 'בָּאִ֖ים',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}\N{HEBREW ACCENT TIPEHA}',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב. '+
        'The MPK (points on no letters) is qamats, ḥiriq, and tipeḥa.'
    ],
}
RECORD_31 = {
    'wlc-index': 31,
    'uxlc-change-proposal': 450,
    'bcv': 'je50:29',
    'Dotan': '∅',
    'qere': 'לָהּ֙',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}',
    'at issue': 'הּ',
    'summary': '+mapiq',
    'remarks': [
        'The MPK has no letter to carry a mapiq for the qere’s ה. '+
        'The MPK (points on no letters) is qamats and (what we intepret as) pashta (not qadma).'
    ],
}
RECORD_32 = {
    'wlc-index': 32,
    'uxlc-change-proposal': 408,
    'bcv': 'ek14:14',
    'Dotan': '∅',
    'qere': 'דָּנִיֵּ֣אל',
    'MPK': 'דָּנִאֵ֣ל',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.'
    ],
}
RECORD_33 = {
    'wlc-index': 33,
    'uxlc-change-proposal': 409,
    'bcv': 'ek14:20',
    'Dotan': '∅',
    'qere': 'דָּנִיֵּ֣אל',
    'MPK': 'דָּנִאֵ֣ל',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.'
    ],
}
RECORD_34 = {
    'wlc-index': 34,
    'uxlc-change-proposal': 410,
    'bcv': 'ek28:3',
    'Dotan': '∅',
    'qere': 'מִדָּֽנִיֵּ֑אל',
    'MPK': 'מִדָּֽנִאֵֿ֑ל',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.',
    ],
    'side-notes': [
        'The rafeh on the א makes it clear that the qere’s yod functions as a consonant not a vowel, '+
        'i.e. the qere’s syllables are מִ־דָּֽ־נִ־יֵּ֑אל.'
    ],
}
RECORD_35 = {
    'wlc-index': 35,
    'uxlc-change-proposal': 506,
    'bcv': 'pr23:26',
    'Dotan': '∅/✓',
    'qere': 'תִּצֹּֽרְנָה׃',
    'MPK': 'תִּרֽצְֹנָהֿ׃',
    'at issue': 'צּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ר does not carry a dagesh for the qere’s צ, perhaps because that would be illegal.',
        #
        'See Comments tab for more complete remarks.'
    ],
}
RECORD_36 = {
    'wlc-index': 36,
    'uxlc-change-proposal': 460,
    'bcv': 'lm4:16',
    'Dotan': '∅',
    'qere': 'וּזְקֵנִ֖ים',
    'MPK': 'זְקֵנִ֖ים',
    'at issue': 'וּ…',
    'summary': '+shrq dt',
    'remarks': [
        'The MPK has no letter to carry a shuruq dot for the qere’s vav.'
    ],
}
RECORD_37 = {
    'wlc-index': 37,
    'uxlc-change-proposal': 108,
    'bcv': 'es9:27',
    'Dotan': '∅',
    'qere': 'וְקִבְּל֣וּ',
    'MPK': 'וְקִבְּלֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
}
RECORD_38 = {
    'wlc-index': 38,
    'uxlc-change-proposal': 411,
    'bcv': 'da2:9',
    'Dotan': '∅',
    'qere': 'הִזְדְּמִנְתּוּן֙',
    'MPK': 'הִזְ\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}מִנְתּוּן֙',
    'at issue': 'דּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ד.',
        #
        'Although it cannot carry the ד’s dagesh, the מ carries the ד’s sheva as well as its own ḥiriq. '
        'Unlike the manuscript, our MPK shows that sheva on a dotted circle rather than on the מ.'
    ],
}
RECORD_39 = {
    'wlc-index': 39,
    'uxlc-change-proposal': 109,
    'bcv': 'er3:3',
    'Dotan': '∅',
    'qere': 'וַיַּעֲל֨וּ',
    'MPK': 'וַיַּעֲלֻ֨',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': [],
}
RECORDS = [
    RECORD_01,
    RECORD_02,
    RECORD_03,
    RECORD_04,
    RECORD_05,
    RECORD_06,
    RECORD_07,
    RECORD_08,
    RECORD_09,
    RECORD_10,
    RECORD_11,
    RECORD_12,
    RECORD_13,
    RECORD_14,
    RECORD_15,
    RECORD_16,
    RECORD_17,
    RECORD_18,
    RECORD_19,
    RECORD_20,
    RECORD_21,
    RECORD_22,
    RECORD_23,
    RECORD_24,
    RECORD_25,
    RECORD_26,
    RECORD_27,
    RECORD_28,
    RECORD_29,
    RECORD_30,
    RECORD_31,
    RECORD_32,
    RECORD_33,
    RECORD_34,
    RECORD_35,
    RECORD_36,
    RECORD_37,
    RECORD_38,
    RECORD_39,
    RECORD_40,
]
