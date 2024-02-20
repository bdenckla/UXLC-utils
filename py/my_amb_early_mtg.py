""" Exports RECORDS. """

_MAM_STATUS_CNN_ALREADY_DONE = (
    'Change not needed since change already made on Wikisource.'
)
_MAM_STATUS_CNN_FIXED_LONG_AGO = (
    'Change not needed since MAM already fixed this or never had this problem to begin with.'
)
_MAM_STATUS_CNN_NO_METEG = (
    'Change not needed since MAM has no meteg at all on this word.'
)
_MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE = (
    'Change not needed since MAM’s corresponding word discards UXLC meteg micro-placement, '
    'and the macro-placement is not at issue here. '
    'I.e. MAM does not preseve the earliness of the meteg, '
    'and which letter it belongs to is not at issue here.'
)
_MAM_STATUS_CHANGE_MAY_BE_NEEDED = (
    'Change may be needed since MAM’s corresponding word retains UXLC’s meteg macro-placement. '
    'I.e. MAM does not preseve the earliness of the meteg but it does preserve which letter it belongs to.'
)


_RECORD_01 = {
    'word': 'וּמֽ͏ַעֲשֵׂ֔ה', 'bcvp': ('1Chr', 23, 28, 17), 'img': '1Chr23v28.png',
}
_RECORD_02 = {
    'word': 'וְנֽ͏ֶחֱלֵ֙יתִי֙', 'bcvp': ('Dan', 8, 27, 4), 'img': 'Dan8v27.png',
}
_RECORD_03 = {
    'word': 'הַמּֽ͏ַאֲכִ֨לְךָ֥', 'bcvp': ('Deut', 8, 16, 1), 'img': 'Deut8v16.png',
}
_RECORD_04 = {
    'word': 'מִמּֽ͏ַעֲלֵ֣י', 'bcvp': ('Deut', 14, 7, 6), 'img': 'Deut14v7.png',
}
_RECORD_05 = {
    'word': 'וְהֽ͏ַעֲבַטְתָּ֞', 'bcvp': ('Deut', 15, 6, 8), 'img': 'Deut15v6.png',
}
_RECORD_06 = {
    'word': 'עֲבֽ͏ָדְךָ֖', 'bcvp': ('Deut', 15, 18, 12), 'img': 'Deut15v18.png',
}
_RECORD_07 = {
    'word': 'דְּגֽ͏ָנְךָ֜', 'bcvp': ('Deut', 18, 4, 2), 'img': 'Deut18v4.png',
}
_RECORD_08 = {
    'word': 'וּפֽ͏ָרְשׂוּ֙', 'bcvp': ('Deut', 22, 17, 14), 'img': 'Deut22v17.png',
}
_RECORD_09 = {
    'word': 'וְקֽ͏ָרְבָה֙', 'bcvp': ('Deut', 25, 11, 7), 'img': 'Deut25v11.png',
    'initial-remark': 'Seems more like a ḥiriq than a sheva under the vav.',
    'further-remarks': ['Seems like there was an erasure under the vav.'],
}
_RECORD_10 = {
    'word': 'וְלֽ͏ָאַלְמָנָ֔ה', 'bcvp': ('Deut', 26, 12, 16), 'img': 'Deut26v12.png',
}
_RECORD_11 = {
    'word': 'יְקֽ͏ִימְךָ֨', 'bcvp': ('Deut', 28, 9, 1), 'img': 'Deut28v9.png',
}
_RECORD_12 = {
    'word': 'וְדֽ͏ַאֲב֥וֹן', 'bcvp': ('Deut', 28, 65, 18), 'img': 'Deut28v65.png',
}
_RECORD_13 = {
    'word': 'וַיּֽ͏ַהַרְג֣וּ', 'bcvp': ('Esth', 9, 15, 11), 'img': 'Esth9v15.png',
}
_RECORD_14 = {
    'word': 'וְאֽ͏ַהֲרֹ֔ן', 'bcvp': ('Ex', 7, 7, 5), 'img': 'Ex7v7.png',
}
_RECORD_15 = {
    'word123p': ('וַ', 'יּֽ͏ַ', 'עֲשׂ֖וּ'),
    'word': 'וַיּֽ͏ַעֲשׂ֖וּ', 'bcvp': ('Ex', 12, 50, 1), 'img': 'Ex12v50.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on the first letter',
    'initial-remark': 'Proposed change in email but not yet a UXLC change proposal.',
    'MAM-word': 'וַֽיַּעֲשׂ֖וּ',
    'MAM-status': _MAM_STATUS_CNN_ALREADY_DONE,
    'MAM-diff-URL': 'https://he.wikisource.org/w/index.php?title=%D7%A9%D7%9E%D7%95%D7%AA_%D7%99%D7%91%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=2839217&oldid=2815126',
}
_RECORD_16 = {
    'word123p': ('וַ', 'יּֽ͏ַ', 'עֲשׂוּ־'),
    'word': 'וַיּֽ͏ַעֲשׂוּ־', 'bcvp': ('Ex', 14, 4, 16), 'img': 'Ex14v4.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'MAM-word': 'וַיַּֽעֲשׂוּ־',
    'MAM-status': _MAM_STATUS_CHANGE_MAY_BE_NEEDED,
}
_RECORD_17 = {
    'word123p': ('וַ', 'יּֽ͏ַ', 'עֲמֹ֖ד'),
    'word': 'וַיּֽ͏ַעֲמֹ֖ד', 'bcvp': ('Ex', 14, 19, 14), 'line': 18, 'img': '17-Ex14v19a14.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on the first letter',
    'initial-remark': 'The first two pataḥ marks are shifted “late”.',
    'further-remarks': [
        'Despite this shift, if we assume that the meteg tracks with this shift, '
        'the vav rather than the yod “owns” the meteg.'
    ],
    'MAM-word': 'וַיַּֽעֲמֹ֖ד',
    'MAM-status': _MAM_STATUS_CHANGE_MAY_BE_NEEDED,
}
_RECORD_18 = {
    'word123p': ('וַ', 'יּֽ͏ַ', 'אֲמִ֙ינוּ֙'),
    'word': 'וַיּֽ͏ַאֲמִ֙ינוּ֙', 'bcvp': ('Ex', 14, 31, 14), 'line': 5, 'img': '18-Ex14v31a14.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on the first letter',
    'MAM-word': 'וַיַּֽאֲמִ֙ינוּ֙',
    'MAM-status': _MAM_STATUS_CHANGE_MAY_BE_NEEDED,
}
_RECORD_19 = {
    'word': 'וְהֽ͏ַאֲזַנְתָּ֙', 'bcvp': ('Ex', 15, 26, 11), 'img': 'Ex15v26a11.png',
}
_RECORD_20 = {
    'word': 'הַמּֽ͏ַחֲלָ֞ה', 'bcvp': ('Ex', 15, 26, 17), 'img': 'Ex15v26a17.png',
}
_RECORD_21 = {
    'word': 'וַיּֽ͏ַעַמְד֖וּ', 'bcvp': ('Ex', 20, 18, 17), 'img': 'Ex20v18.png',
}
_RECORD_22 = {
    'word123p': ('וַ', 'יּֽ͏ַ', 'עֲל֖וּ'),
    'word': 'וַיּֽ͏ַעֲל֖וּ', 'bcvp': ('Ex', 24, 5, 6), 'img': 'Ex24v5.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on the first letter',
    'initial-remark': 'See UXLC change proposal 2024.01.29-3.',
    'existing UXLC change proposal': ('2024.04.01', '2024.01.29-3'),
    'MAM-word': 'וַֽיַּעֲל֖וּ',
    'MAM-status': _MAM_STATUS_CNN_ALREADY_DONE,
    'MAM-diff-URL': 'https://he.wikisource.org/w/index.php?title=%D7%A9%D7%9E%D7%95%D7%AA_%D7%9B%D7%93%2F%D7%98%D7%A2%D7%9E%D7%99%D7%9D&diff=2838019&oldid=2837894',
}
_RECORD_23 = {
    'word123p': ('בְּ', 'נֽ͏ֵ', 'י־'),
    'word': 'בְּנֽ͏ֵי־', 'bcvp': ('Ex', 30, 12, 5), 'img': 'Ex30v12.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on letter 2',
    'initial-remark': 'L has a normal meteg on the 2nd letter (nun).',
    'further-remarks': [
        'BHS agrees with L so this seems like purely a WLC transcription error.',
        'An almost identical error appears in @בְּנֽ͏ֵי־# in UXLC Ex 35:20.'
    ],
    'MAM-word': 'בְּנֵֽי־',
    'MAM-status': _MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE,
}
_RECORD_24 = {
    'word123p': ('בְּ', 'נֽ͏ֵ', 'י־'),
    'word': 'בְּנֽ͏ֵי־', 'bcvp': ('Ex', 35, 20, 4), 'img': 'Ex35v20.png',
    'dubious early mtg on letter 2': 'Better transcribed as a normal meteg on letter 2',
    'initial-remark': 'L has a normal meteg on the 2nd letter (nun).',
    'further-remarks': [
        'BHS agrees with L so this seems like purely a WLC transcription error.',
        'An almost identical error appears in @בְּנֽ͏ֵי־# in UXLC Ex 30:12.'
    ],
    'MAM-word': 'בְּנֵֽי־',
    'MAM-status': _MAM_STATUS_CNN_MACRO_NOT_AT_ISSUE,
}
_RECORD_25 = {
    'word123p': ('וְ', 'לֽ͏ָ', 'קַחְתָּ֣'),
    'word': 'וְלֽ͏ָקַחְתָּ֣', 'bcvp': ('Ezek', 5, 2, 9), 'line': 16, 'img': '25-Ezek5v2.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'initial-remark': 'The sheva has an additional dot below it, but we ignore that dot.',
    'MAM-word': 'וְלָקַחְתָּ֣',
    'MAM-status': _MAM_STATUS_CNN_NO_METEG
}
_RECORD_26 = {
    'word': 'וְאֽ͏ֵלַמָּ֔יו', 'bcvp': ('Ezek', 40, 36, 3), 'wq': 'q', 'line': 9, 'img': '26-Ezek40v36.png',
}
_RECORD_27 = {
    'word': 'וַיּֽ͏ַעֲשׂוּ־', 'bcvp': ('Ezra', 10, 16, 1), 'line': 3, 'img': 'Ezra10v16.png',
}
_RECORD_28 = {
    'word': 'לְהֽ͏ַחֲיֽוֹת׃', 'bcvp': ('Gen', 6, 20, 14), 'line': 6, 'img': 'Gen6v20.png',
}
_RECORD_29 = {
    'word': 'בְּעֽ͏ַנְנִ֥י', 'bcvp': ('Gen', 9, 14, 2), 'img': 'Gen9v14.png',
}
_RECORD_30 = {
    'word': 'וְהֽ͏ַכְּנַעֲנִ֖י', 'bcvp': ('Gen', 12, 6, 10), 'img': 'Gen12v6.png',
}
_RECORD_31 = {
    'word': 'וְאֽ͏ֶעֱשֶׂ֨ה', 'bcvp': ('Gen', 27, 9, 12), 'line': 5, 'img': 'Gen27v9.png',
}
_RECORD_32 = {
    'word': 'וַיּֽ͏ַעֲל֨וּ', 'bcvp': ('Gen', 50, 7, 6), 'img': 'Gen50v7.png',
}
_RECORD_33 = {
    'word': 'וְהֽ͏ַחֲזָקָ֗ה', 'bcvp': ('Isa', 27, 1, 8), 'line': 20, 'img': 'Isa27v1.png',
}
_RECORD_34 = {
    'word': 'בְּרֽ͏ָע׃', 'bcvp': ('Isa', 33, 15, 19), 'line': 19, 'img': 'Isa33v15.png',
}
_RECORD_35 = {
    'word123p': ('וְ', 'קֽ͏ָ', 'רָאתָ֩'),
    'word': 'וְקֽ͏ָרָאתָ֩', 'bcvp': ('Jer', 3, 12, 2), 'img': 'Jer3v12.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'initial-remark': 'MAM notes with surprise that Mechon Mamre has meteg on qof.',
    'further-remarks': ['MAM’s note is ממ!=@וְקָֽרָאתָ֩#'],
    'MAM-word': 'וְֽקָרָ֩אתָ֩',
    'MAM-status': _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_36 = {
    'word': 'הַמּֽ͏ַעֲשִׂ֥ים', 'bcvp': ('Jer', 7, 13, 6), 'img': 'Jer7v13.png',
}
_RECORD_37 = {
    'word': 'וְ֝אֽ͏ַחֲוָתִ֗י', 'bcvp': ('Job', 13, 17, 4), 'img': 'Job13v17.png',
}
_RECORD_38 = {
    'word': 'הַקּֽ͏ִיקָי֖וֹן', 'bcvp': ('Jon', 4, 6, 18), 'img': 'Jon4v6.png',
}
_RECORD_39 = {
    'word': 'בֶּחֽ͏ָרָבָ֛ה', 'bcvp': ('Josh', 3, 17, 7), 'img': 'Josh3v17.png',
}
_RECORD_40 = {
    'word': 'וְהֽ͏ַמְאַסֵּ֗ף', 'bcvp': ('Josh', 6, 13, 17), 'img': 'Josh6v13.png',
}
_RECORD_41 = {
    'word': 'הָאֽ͏ָהֳלִ֖י', 'bcvp': ('Josh', 7, 21, 22), 'img': 'Josh7v21.png',
}
_RECORD_42 = {
    'word': 'וְאֽ͏ַחֲרֵי־', 'bcvp': ('Josh', 8, 34, 1), 'line': 6, 'img': 'Josh8v34.png',
}
_RECORD_43 = {
    'word': 'וְנֽ͏ַהֲלָל֙', 'bcvp': ('Josh', 19, 15, 2), 'line': 25, 'img': 'Josh19v15.png',
}
_RECORD_44 = {
    'word': 'וְהֽ͏ַחִתִּי֙', 'bcvp': ('Josh', 24, 11, 14), 'line': 11, 'img': 'Josh24v11.png',
}
_RECORD_45 = {
    'word': 'וַיּֽ͏ַחֲנ֖וּ', 'bcvp': ('Judg', 20, 19, 5), 'img': 'Judg20v19.png',
}
_RECORD_46 = {
    'word': 'וַיּֽ͏ֶחֶרְדוּ֙', 'bcvp': ('1Kings', 1, 49, 1), 'img': '1Kings1v49.png',
}
_RECORD_47 = {
    'word': 'לְהֽ͏ַחֲרִימָ֑ם', 'bcvp': ('1Kings', 9, 21, 11), 'img': '1Kings9v21.png',
}
_RECORD_48 = {
    'word': 'וַיּֽ͏ַאֲבֶל־', 'bcvp': ('Lam', 2, 8, 13), 'img': 'Lam2v8.png',
}
_RECORD_49 = {
    'word': 'וְהֽ͏ַעֲבַרְתָּ֞', 'bcvp': ('Lev', 25, 9, 1), 'img': 'Lev25v9.png',
}
_RECORD_50 = {
    'word': 'וְהֽ͏ֶעֱמִ֥יד', 'bcvp': ('Lev', 27, 11, 11), 'img': 'Lev27v11.png',
}
_RECORD_51 = {
    'word123p': ('וְ', 'הֽ͏ַ', 'עֲמַדְתָּ֣'),
    'word': 'וְהֽ͏ַעֲמַדְתָּ֣', 'bcvp': ('Num', 3, 6, 5), 'img': 'Num3v6.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'initial-remark': 'MAM notes the uncertainty of the ownership of this meteg in L.',
    'MAM-word': 'וְהַעֲמַדְתָּ֣',
    'MAM-status': _MAM_STATUS_CNN_NO_METEG
}
_RECORD_52 = {
    'word': 'לְטֽ͏ַהֲרָ֔ם', 'bcvp': ('Num', 8, 7, 4), 'img': 'Num8v7.png',
}
_RECORD_53 = {
    'word': 'וְהֽ͏ַחֲרַמְתִּ֖י', 'bcvp': ('Num', 21, 2, 13), 'img': 'Num21v2.png',
}
_RECORD_54 = {
    'word': 'וְהֽ͏ֶאֱבִ֥יד', 'bcvp': ('Num', 24, 19, 3), 'img': 'Num24v19.png',
}
_RECORD_55 = {
    'word': 'וְהֽ͏ַעֲמַדְתָּ֣', 'bcvp': ('Num', 27, 19, 1), 'img': 'Num27v19.png',
}
_RECORD_56 = {
    'word': 'תֵדֽ͏ָע׃', 'bcvp': ('Prov', 5, 6, 8), 'img': 'Prov5v6.png',
}
_RECORD_57 = {
    'word': 'אֱוֽ͏ִיל׃', 'bcvp': ('Prov', 7, 22, 11), 'img': 'Prov7v22.png',
}
_RECORD_58 = {
    'word': 'צַדּֽ͏ִיק׃', 'bcvp': ('Prov', 14, 32, 6), 'img': 'Prov14v32.png',
}
_RECORD_59 = {
    'word': 'צָרֽ͏ָה׃', 'bcvp': ('Prov', 25, 19, 8), 'img': 'Prov25v19.png',
}
_RECORD_60 = {
    'word': 'צַדּֽ͏ִיק׃', 'bcvp': ('Ps', 7, 10, 11), 'img': 'Ps7v10.png',
}
_RECORD_61 = {
    'word': 'עָלֽ͏ָי׃', 'bcvp': ('Ps', 16, 6, 8), 'img': 'Ps16v6.png',
}
_RECORD_62 = {
    'word123p': ('וַ֭', 'יּֽ͏ַ', 'עֲבֹר'),
    'word': 'וַ֭יּֽ͏ַעֲבֹר', 'bcvp': ('Ps', 37, 36, 1), 'img': 'Ps37v36.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'MAM-word': 'וַֽ֭יַּעֲבֹר',
    'MAM-status': _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_63 = {
    'word': 'פָּ֤קֽ͏ַדְתָּ', 'bcvp': ('Ps', 65, 10, 1), 'img': 'Ps65v10.png',
}
_RECORD_64 = {
    'word123p': ('וַ֭', 'יּֽ͏ַ', 'דְרִיכֵם'),
    'word': 'וַ֭יּֽ͏ַדְרִיכֵם', 'bcvp': ('Ps', 107, 7, 1), 'img': 'Ps107v7.png',
    'dubious early mtg on letter 2': 'Perhaps better transcribed as a normal meteg on the first letter',
    'MAM-word': 'וַֽ֭יַּדְרִיכֵם',
    'MAM-status': _MAM_STATUS_CNN_FIXED_LONG_AGO,
}
_RECORD_65 = {
    'word': 'עָלֽ͏ָי׃', 'bcvp': ('Ps', 142, 8, 12), 'img': 'Ps142v8.png',
}
_RECORD_66 = {
    'word': 'וַיּֽ͏ִזְכְּרֶ֖הָ', 'bcvp': ('1Sam', 1, 19, 16), 'img': '1Sam1v19.png',
}

RECORDS = [
    _RECORD_01,
    _RECORD_02,
    _RECORD_03,
    _RECORD_04,
    _RECORD_05,
    _RECORD_06,
    _RECORD_07,
    _RECORD_08,
    _RECORD_09,
    _RECORD_10,
    _RECORD_11,
    _RECORD_12,
    _RECORD_13,
    _RECORD_14,
    _RECORD_15,
    _RECORD_16,
    _RECORD_17,
    _RECORD_18,
    _RECORD_19,
    _RECORD_20,
    _RECORD_21,
    _RECORD_22,
    _RECORD_23,
    _RECORD_24,
    _RECORD_25,
    _RECORD_26,
    _RECORD_27,
    _RECORD_28,
    _RECORD_29,
    _RECORD_30,
    _RECORD_31,
    _RECORD_32,
    _RECORD_33,
    _RECORD_34,
    _RECORD_35,
    _RECORD_36,
    _RECORD_37,
    _RECORD_38,
    _RECORD_39,
    _RECORD_40,
    _RECORD_41,
    _RECORD_42,
    _RECORD_43,
    _RECORD_44,
    _RECORD_45,
    _RECORD_46,
    _RECORD_47,
    _RECORD_48,
    _RECORD_49,
    _RECORD_50,
    _RECORD_51,
    _RECORD_52,
    _RECORD_53,
    _RECORD_54,
    _RECORD_55,
    _RECORD_56,
    _RECORD_57,
    _RECORD_58,
    _RECORD_59,
    _RECORD_60,
    _RECORD_61,
    _RECORD_62,
    _RECORD_63,
    _RECORD_64,
    _RECORD_65,
    _RECORD_66,
]
