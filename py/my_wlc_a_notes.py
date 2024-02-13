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
_DOTAN_PAGE_XX = (
    'Dotan remarks, in his Foreword to BHL (page xx):',
    #
    'Another example [of a point CEN] is '+
    'an ʿayin of the ketiv that cannot carry a dagesh that is due in the qere, '+
    'as in the manuscript in Deut. 28:27 '+
    'in the [body] text וּבַעְפֹלִים and '+
    'in the margin ק̇ ובטחרים; '+
    'in the printed edition a dagesh was added[, yielding] וּבַטְּחֹרִים.',
    #
    '[The terminology CEN (created ex nihilo) is mine, not Dotan’s.]',
    #
    '[In this quote, Dotan omits the accent (zaqef qatan) on '+
    'the ל of וּבַעְפֹלִים and on '+
    'the ר of וּבַטְּחֹרִים, '+
    'perhaps because it is not germane to the topic at hand.]',
    #
    '[Note that dt28:27 is not a-noted in WLC! (*W/B/(PLYM **W./BA/+.:XORI80YM)]'
)

RECORD_01 = {
    'wlc-index': 1,
    'uxlc-change-proposal': 101,
    'bcv': 'gn27:29',
    'qere': 'וְיִֽשְׁתַּחֲו֤וּ',
    'MPK': 'וְיִֽשְׁתַּחֲוֻ֤',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
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
    'qere': 'וַיִּֽשְׁתַּחֲוּֽוּ׃',
    'MPK': 'וַיִּֽשְׁתַּחֲוֻּֽ׃',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
    'side-notes': [
        'In WLC, this word also has a 1-note, '+
        'presumably because of the unexpected dagesh in the qere’s penultimate vav.',
        #
        'As a reminder, a WLC 1-note (bracket-1 note) is defined as follows: '+
        f'«{_WLC_1_BRACKET_NOTE_DEFINITION}»',
        #
        'Although Dotan has a note on his body-text word וַיִּֽשְׁתַּחֲוּֽוּ׃, '+
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
        'This is the dual of js24:15.'
    ],
    'side-notes': [
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
        'This is the dual of js22:7.'
    ],
    'side-notes': [
        'Dotan notes that strictly speaking, the implied qere is מֵּעֵ֣בֶר (unexpectedly dageshed).'
    ],
}
RECORD_06 = {
    'wlc-index': 6,
    'uxlc-change-proposal': 401,
    'bcv': 'ju20:13',
    'qere': 'בְּנֵ֣י',
    'MPK': (
        '\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}'+
        '\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}'
    ),
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב. '+
        'The MPK (points on no letters) is sheva, tsere, and munaḥ.'
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
    'qere': 'וַיְצַוּ֕וּ',
    'MPK': 'וַיְצַוֻּ֕',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
}
RECORD_08 = {
    'wlc-index': 8,
    'uxlc-change-proposal': 501,
    'bcv': '1s5:6',
    'qere': 'בַּטְּחֹרִ֔ים',
    'MPK': 'בַּעְפֹלִ֔ים',
    'at issue': 'טּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ע does not carry a dagesh for the qere’s ט, '+
        'perhaps because that would be illegal.'
    ],
    'side-notes': [
        'Same issue, indeed same word modulo accent, six verses later, in 5:12.',
        #
        *_DOTAN_PAGE_XX
    ],
}
RECORD_09 = {
    'wlc-index': 9,
    'uxlc-change-proposal': 502,
    'bcv': '1s5:12',
    'qere': 'בַּטְּחֹרִ֑ים',
    'MPK': 'בַּעְפֹלִ֑ים',
    'at issue': 'טּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ע does not carry a dagesh for the qere’s ט, '+
        'perhaps because that would be illegal.'
    ],
    'side-notes': [
        'Same issue, indeed same word modulo accent, six verses before, in 5:6.',
        #
        *_DOTAN_PAGE_XX
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
        'The MPK’s ן in מבן does not carry a sheva for the qere’s נ, '+
        'perhaps because that would be illegal.'
    ],
    'side-notes': [
        'The maqaf disappears from the MPK. '+
        'It is unclear why the maqaf is supplied in the first place. '+
        'Perhaps it is supplied because without it, מִבִּן would be illegal: '+
        'a word without an accent.',
        #
        'Dotan notes that strictly speaking, the implied qere is '+
        'מִבִּניָמִ֗ין (no sheva under middle נ).'
    ],
}
RECORD_11 = {
    'wlc-index': 11,
    'uxlc-change-proposal': 104,
    'bcv': '1s12:10',
    'qere': 'וַיֹּאמְר֣וּ',
    'MPK': 'וַיֹּאמְרֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
}
RECORD_12 = {
    'wlc-index': 12,
    'uxlc-change-proposal': 105,
    'bcv': '1s13:19',
    'qere': 'אָמְר֣וּ',
    'MPK': 'אָמְרֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
    'side-notes': [
        'There’s a large, clear dot above the ר; '+
        'I don’t know what it is supposed to mean, if anything. '+
        'Surely not a revia!'
    ],
}
RECORD_13 = {
    'wlc-index': 13,
    'uxlc-change-proposal': 600,
    'bcv': '1s17:23',
    'img': '13-1s17v23.png',
    'folio': 'Folio_159B',
    'column': 2,
    'line': 11,
    'Dotan': '✓',
    'qere': 'מִמַּעַרְכ֣וֹת',
    'MPK': 'מִמַּעֲרְ֣וֹת',
    'at issue': 'עַ',
    'summary': 'ḥtf ptḥ to ptḥ',
    'remarks': [
        'The MPK’s ע has a ḥataf pataḥ where the qere has a pataḥ.'
    ],
    'side-notes': [
        'Unexpected ḥataf vowels are a known feature (bug?) of ל. '+
        'I.e. this is rare but hardly unique. '+
        'This unexpected ḥataf may well be unrelated '+
        'to the ketiv/qere differences in this word. '
        'If it is unrelated, '
        'this should be a bracket-1 or bracket-U note in WLC, not a bracket-a note.',
        #
        'Breuer notes that א and ק have the expected pataḥ. '+
        '(א is the Aleppo Codex and ק is the Cairo Codex of The Prophets.)',
        #
        'Dotan notes that strictly speaking, the implied qere is '+
        'מִמַּעֲרְכ֣וֹת (ḥataf pataḥ under ע).'
    ],
}
RECORD_14 = {
    'wlc-index': 14,
    'uxlc-change-proposal': 452,
    'bcv': '2s3:2',
    'qere': 'וַיִּוָּלְד֧וּ',
    'MPK': 'וַיִּ\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}לְד֧וּ',
    'at issue': 'וָּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s vav-qamats.'
    ],
    'side-notes': [
        'Although it cannot carry the vav’s dagesh, '+
        'the ל carries the vav’s qamats as well as its own sheva. '+
        'Unlike the manuscript, our MPK shows that qamats on a dotted circle rather than on the ל.'
    ],
}
RECORD_15 = {
    'wlc-index': 15,
    'uxlc-change-proposal': 403,
    'bcv': '2s8:3',
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
    'uxlc-change-proposal': 412,
    'bcv': '2s18:20',
    'qere': 'עַל־כֵּ֥ן',
    'qere-atom': 'כֵּ֥ן',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT TSERE}\N{HEBREW ACCENT MUNAH}\N{DOTTED CIRCLE}',
    'at issue': 'כּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s כ. '+
        'The MPK (points on no letters) is tsere and merkha.'
    ],
    'side-notes': [
        'The points of the MPK are under the ל of the preceding word (עַל), '+
        'but we don’t consider them to be carried by that ל.',
        #
        'Although Dotan has a note on his body-text compound עַל־כֵּ֥ן, '+
        'I do not take him to have noted it for the issue at hand: '+
        'the added dagesh. '+
        '(Dotan notes that strictly speaking, the implied qere is עַל כֵ֥ן.) '+
        'I take him to have noted this compound '+
        'only because the manuscript lacks the expected trailing maqaf on עַל. '+
        #
        'The lack of a trailing maqaf on the preceding word (עַל) '+
        'is the subject of a currently-pending '+
        'change proposal, 2024.04.01/2024.01.18-2.'
    ],
}
RECORD_17 = {
    'wlc-index': 17,
    'uxlc-change-proposal': 454,
    'bcv': '2s21:9',
    'qere': 'בִּתְחִלַּ֖ת',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}תְחִלַּ֖ת',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב.'
    ],
    'side-notes': [
        'Although it cannot carry ב’s dagesh, the initial ת could carry the ב’s ḥiriq as well as its own sheva. '+
        'Yet, it does not: the spacing is generous, leaving the ḥiriq floating out on its own without a parent letter. '+
        'Unlike the manuscript, our MPK shows that ḥiriq on a dotted circle rather than floating out on its own.'
    ],
}
RECORD_18 = {
    'wlc-index': 18,
    'uxlc-change-proposal': 455,
    'bcv': '2s22:8',
    'qere': 'וַיִּתְגָּעַ֤שׁ',
    'MPK': 'וַ\N{DOTTED CIRCLE}\N{HEBREW POINT HIRIQ}תְגָּעַ֤שׁ',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.'
    ],
    'side-notes': [
        'Although it cannot carry the yod’s dagesh, the vav carries its own pataḥ as well as the yod’s ḥiriq. '+
        'Unlike the manuscript, our MPK shows that ḥiriq on a dotted circle rather than on the vav.'
    ],
}
RECORD_19 = {
    'wlc-index': 19,
    'uxlc-change-proposal': 503,
    'bcv': '1k7:45',
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
    'qere': 'וַיִּשְׁתַּחֲו֥וּ',
    'MPK': 'וַיִּשְׁתַּחֲוּ֥',
    'at issue': '?',
    'summary': '?',
    'remarks': [
        'The MPK has all the qere’s marks so I don’t see what the issue is.'
    ],
    'side-notes': [
        'The suffix וּ֥ becomes ו֥וּ. '+
        'I would have expected a qubuts in the MPK, but this notation works, too, '+
        'as long as we interpret the MPK’s dot in the vav to be a shuruq dot not a dagesh.'
    ],
}
RECORD_21 = {
    'wlc-index': 21,
    'uxlc-change-proposal': 106,
    'bcv': '1k12:7',
    'qere': 'וַיְדַבְּר֨וּ',
    'MPK': 'וַיְדַבְּרֻ֨',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
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
    'qere': 'דִּבְיוֹנִ֖ים',
    'MPK': 'חִרְייֹונִ֖ים',
    'at issue': 'דּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ח does not carry a dagesh for the qere’s ד, '+
        'perhaps because that would be illegal.'
    ],
    'side-notes': [
        'the ḥolam malei dot on the qere’s vav comes from the ḥolam (ḥaser?) dot on the yod of the MPK! '+
        'Instead of being on the yod of the MPK, '+
        'why isn’t this dot on the vav of the MPK?'
    ],
}
RECORD_24 = {
    'wlc-index': 24,
    'uxlc-change-proposal': 430,
    'bcv': '2k19:31',
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
    'qere': 'בָּנָיו֙',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}',
    'at issue': 'בּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ב. '+
        'The MPK (points on no letters) is two qamats marks and pashta.'
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
    'qere': 'יִקָּ֑חוּ',
    'MPK': 'יִקָּ֑חֻ',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
    'side-notes': [
        'The dagesh in the qof is way off center, but still legit IMO.'
    ],
}
RECORD_27 = {
    'wlc-index': 27,
    'uxlc-change-proposal': 303,
    'bcv': '2k23:33',
    'qere': 'מִמְּלֹ֖ךְ',
    'MPK': 'בִּמְּלֹ֖ךְ',
    'at issue': 'מ',
    'summary': '-dgsh',
    'remarks': [
        'The MPK’s בּ seems to carry a dagesh for the qere’s מ but it is rejected. '+
        'See js24:15, which is similar.'
    ],
    'side-notes': [
        'Dotan does not note this case, though he does note js24:15.'
    ],
}
RECORD_28 = {
    'wlc-index': 28,
    'uxlc-change-proposal': 202,
    'bcv': 'is3:15',
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
    'qere': 'לָהּ֙',
    'MPK': '\N{DOTTED CIRCLE}\N{HEBREW POINT QAMATS}\N{DOTTED CIRCLE}\N{HEBREW ACCENT PASHTA}',
    'at issue': 'הּ',
    'summary': '+mapiq',
    'remarks': [
        'The MPK has no letter to carry a mapiq for the qere’s ה. '+
        'The MPK (points on no letters) is qamats and pashta.'
    ],
}
RECORD_32 = {
    'wlc-index': 32,
    'uxlc-change-proposal': 458,
    'bcv': 'ek14:14',
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
    'uxlc-change-proposal': 459,
    'bcv': 'ek14:20',
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
    'uxlc-change-proposal': 460,
    'bcv': 'ek28:3',
    'qere': 'מִדָּֽנִיֵּ֑אל',
    'MPK': 'מִדָּֽנִאֵֿ֑ל',
    'at issue': 'יּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s yod.'
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
    'qere': 'תִּצֹּֽרְנָה׃',
    'MPK': 'תִּרֽצְֹנָהֿ׃',
    'at issue': 'צּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK’s ר does not carry a dagesh for the qere’s צ, perhaps because that would be illegal.'
    ],
    'side-notes': [
        'Nor does the MPK’s צ carry a dagesh for the qere’s צ.',
        #
        'More generally, the MPK is a mess, both in terms of neatness '+
        'and in terms of what marks ended up on what letters.',
        #
        'The below-marks make sense, though one has to sort of squint to see what one expects to see. '+
        'I.e. the below marks follow the expected order, i.e. the qere order: ḥiriq, siluq, sheva, qamats.',
        #
        'The above-marks is where it gets weird, since the qere צ’s ḥolam ḥaser dot '+
        'is already present on the צ of the MPK. '+
        'I would expect the ḥolam ḥaser dot to be on the ר of the MPK, i.e. I would expect it to be '+
        'in its qere POSITION, not on its qere LETTER. I.e. I would expect תִּרֹֽצְנָה׃.',
        #
        'Avi, in the MAM documentation, reports that the MPK of א follows this pattern more completely: '+
        'for the two letters at issue in this ketiv/qere, i.e. for the two transposed letters, '+
        'the pointing is already present on the LETTER it will “land on” in the qere, '+
        'not in the POSITION it will land on in the qere. '+
        'That is to say, א-כתיב=תִּרְצֹּֽנָה׃. '+
        'I.e. to form the pointed qere from the pointed ketiv, all that needs to be done is to '+
        'transpose the ר and the צ ALONG with their marks!',
        #
        'Dotan’s Appendix A notes, as I have noted above, that the ḥolam ḥaser dot would be expected '+
        'on (the left side of) the ר of the MPK, whereas it is on (the left side of) the צ. '+
        'Dotan does not note anything about the creation ex nihilo of the dagesh on the qere’s צ.',
        #
        'A final, unimportant remark is that I’ve put a rafeh above the ה of the MPK '+
        'but I’m not sure about this; it might belong above the נ.'
    ],
}
RECORD_36 = {
    'wlc-index': 36,
    'uxlc-change-proposal': 461,
    'bcv': 'lm4:16',
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
    'qere': 'וְקִבְּל֣וּ',
    'MPK': 'וְקִבְּלֻ֣',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
}
RECORD_38 = {
    'wlc-index': 38,
    'uxlc-change-proposal': 462,
    'bcv': 'da2:9',
    'qere': 'הִזְדְּמִנְתּוּן֙',
    'MPK': 'הִזְ\N{DOTTED CIRCLE}\N{HEBREW POINT SHEVA}מִנְתּוּן֙',
    'at issue': 'דּ',
    'summary': '+dgsh',
    'remarks': [
        'The MPK has no letter to carry a dagesh for the qere’s ד.'
    ],
    'side-notes': [
        'Although it cannot carry the ד’s dagesh, the מ carries the ד’s sheva as well as its own ḥiriq. '+
        'Unlike the manuscript, our MPK shows that sheva on a dotted circle rather than on the מ.'
    ],
}
RECORD_39 = {
    'wlc-index': 39,
    'uxlc-change-proposal': 109,
    'bcv': 'er3:3',
    'qere': 'וַיַּעֲל֨וּ',
    'MPK': 'וַיַּעֲלֻ֨',
    'at issue': 'וּ',
    'summary': 'qbts to shrq',
    'remarks': ['The qubuts in the MPK becomes a shuruq dot in the qere.'],
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
]
