import my_html
import my_html_for_img
from my_html_span_romanized import rmn


def _html_for_pcl(pcl):
    page, column, line = pcl
    return [
        '(',
        my_html.anchor(
            f'page {page}',
            {'href': f'https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg'}
        ),
        f' col {column} line {line}',
        '):'
    ]


def _html_for_bcv_str_wlt_tdu(bcv_str):  # wlt_tdu: with link to tanach.us
    return my_html.anchor(
        bcv_str,
        {'href': f'https://tanach.us/Tanach.xml?{bcv_str}'}
    )


def _html_for_kq(kq):
    return kq[0], my_html.line_break(), kq[1]


def _bkm_table_row_of_headers():  # bkm: bcv, ketiv/qere, manuscript
    return my_html.table_row_of_headers(['', '', 'manuscript'])


def _bkm_table_row(k2q2rec):
    return my_html.table_row_of_data(
        [
            _html_for_bcv_str_wlt_tdu(k2q2rec['bcv-str']),
            _html_for_kq(k2q2rec['kq-strs']),
            k2q2rec['manuscript']
        ],
        [
            None,
            _HBO_RTL_BIG,
            None
        ],
    )


def _intro_and_img(k2q2rec):
    return [
        my_html.para(
            [
                *k2q2rec['intro'], ' ', *_html_for_pcl(k2q2rec['pcl'])
            ]
        ),
        my_html_for_img.html_for_single_img(k2q2rec['img'])
    ]

_HBO_RTL_BIG = {'lang': 'hbo', 'dir': 'rtl', 'class': 'big'}
_GAYA_PAREN_METEG = [rmn('gaʿya'), ' (', rmn('meteg'), ')']
_JOB_38_1_and_40_6_PARAS = [
    my_html.para([
        'In the cases of Job 38:1 and 40:6, '
        'we find that '
        'while the manuscript supports WLC’s grouping of the two ', rmn('qere'), ' words together, '
        'the manuscript does not support WLC’s treatment of the ', rmn('ketiv'), ' letters '
        'as a single word. '
        'In other words, the manuscript supports a k1q2 grouping rather than a k2q2 grouping. '
    ]),
    my_html.para([
        'In both 38:1 and 40:6, '
        'the ', rmn('paseq'), ' after the ', rmn('nun'), ' '
        'should not be interpreted as relevant to the ', rmn('ketiv'), ', i.e. should not be be interpreted '
        'as splitting the ', rmn('ketiv'), ' into two words. '
        'I find it surprising and unfortunate that WLC went to the trouble of devoting a special bracket note, ',
        my_html.code(']M'), ', '
        'to these cases. '
        'A little more scrutiny might have revealed that there is only a mistake in transcription, '
        'not an anomaly in the manuscript. '
        'Here the WLC transcription has a little more work to do than usual because, as with all k/q, WLC is '
        'not just transcribing BHS (or later, ל) '
        'but also converting (in this case incorrectly) '
        'from pointed-ketiv, unpointed-qere representation to the opposite representation. '
    ])
]
_JOB_38_1_and_40_6_INTRO = [
    'Note that, extraordinarily, in Job 38:1 and 40:6, '
    'the scribe has reiterated some of the pointing of the ', rmn('ketiv'), ' '
    'on the ', rmn('qere'), ' letters, '
    'pointing the מן of the ', rmn('qere'), ' with ',
    rmn('ḥiriq'), ', ',
    *_GAYA_PAREN_METEG, ', and ',
    rmn('paseq'), '. '
    '(I’m not sure why this was done, '
    'and I don’t think it is relevant to the issue at hand, '
    'but nonetheless it seemed worth mentioning.) '
    'Here is the manuscript image for Job 38:1'
]
_K2Q2REC_EZEK = {
    'bcv-str': 'Ezek42:9',
    'kq-strs': ('ומתחתה לשכות', 'וּמִתַּ֖חַת הַלְּשָׁכ֣וֹת'),
    'pcl': ('299B', 3, 22),
    'img': 'Ezek42v9.png',
    'manuscript': 'supports WLC’s k2q2',
    'intro': [
        'In the case of Ezekiel 42:9, we find that the manuscript supports WLC’s k2q2 grouping'
    ],
}
_K2Q2REC_SND_SAM_21_12 = {
    'bcv-str': '2Sam21:12',
    'kq-strs': ('שם הפלשתים', 'שָׁ֙מָּה֙ פְּלִשְׁתִּ֔ים'),
    'pcl': ('181B', 2, 12),
    'img': '2Sam21c12.png',
    'manuscript': ['supports k2q2+k1q1', my_html.line_break(), 'rather than WLC’s k1q1+k2q2'],
    'intro': [
        'But in the case of 2 Samuel 21:12, we find that the manuscript does not support WLC’s k2q2 grouping. '
        'Rather, it supports a different k2q2 grouping than that found in WLC! '
        'The manuscript’s k2q2 reaches back one word earlier than WLC’s k2q2'
    ],
}
_K2Q2REC_FST_KGS = {
    'bcv-str': '1Kings17:15',
    'kq-strs': ('הוא־והיא', 'הִיא־וָה֛וּא'),
    'pcl': ('197B', 3, 24),
    'img': '1Kings17v15.png',
    'manuscript': ['supports k1q1×2', my_html.line_break(), 'rather than WLC’s k2q2'],
    'intro': [
        'In the case of 1 Kings 17:15, we find that the manuscript does not support WLC’s k2q2 grouping'
    ],
}
_K2Q2REC_FST_SAM = {
    'bcv-str': '1Sam20:2',
    'kq-strs': ('לו־עשה', 'לֹֽא־יַעֲשֶׂ֨ה'),
    'pcl': ('161B', 2, 17),
    'img': '1Sam20v2.png',
    'manuscript': 'supports WLC’s k2q2',
    'intro': [
        'In the case of 1 Sam 20:2, we find that the manuscript supports WLC’s k2q2 grouping'
    ],
}
_K2Q2REC_ISAIAH = {
    'bcv-str': 'Isaiah52:5',
    'img': 'Isaiah52v5.png',
    'kq-strs': ('מי־לי־', 'מַה־לִּי־'),
    'pcl': ('240B', 3, 3),
    'manuscript': 'supports WLC’s k2q2',
    'intro': [
        'In the case of Isaiah 52:5, we find that the manuscript supports WLC’s k2q2 grouping. '
        'It is slightly surprising that this k/q is framed as a k2q2 at all, since the second word '
        'of both qere and ketiv is לי, i.e. there is no variation in the second word. '
        'Here is the manuscript image'
    ],
}
_K2Q2REC_JOB_38V12 = {
    'bcv-str': 'Job38:12',
    'img': 'Job38v12.png',
    'kq-strs': ('ידעתה שחר', 'יִדַּ֖עְתָּה הַשַּׁ֣חַר'),
    'pcl': ('408A', 2, 17),
    'manuscript': 'supports WLC’s k2q2',
    'intro': [
        'In the case of Job 38:12, we find that the manuscript supports WLC’s k2q2 grouping'
    ],
}
_K2Q2REC_JOB_38V01 = {
    'bcv-str': 'Job38:1',
    'img': 'Job38v1.png',
    'kq-strs': ('מנ הסערה', 'מִ֥ן ׀ הַסְּעָרָ֗ה'),
    'pcl': ('408A', 2, 5),
    'manuscript': ['supports k1q2', my_html.line_break(), 'rather than WLC’s k2q2'],
    'intro': _JOB_38_1_and_40_6_INTRO,
}
_K2Q2REC_JOB_40 = {
    'bcv-str': 'Job40:6',
    'img': 'Job40v6.png',
    'kq-strs': ('מנ סערה', 'מִ֥ן ׀ סְעָרָ֗ה'),
    'pcl': ('408B', 2, 13),
    'manuscript': ['supports k1q2', my_html.line_break(), 'rather than WLC’s k2q2'],
    'intro': ['Here is the manuscript image for Job 40:6'],
}
_BKM_REC_SND_SAM_5_2 = {
    'bcv-str': '2Sam5:2',
    'img': '2Sam5v2.png',
    'kq-strs': ('הייתה מוציא והמבי', 'הָיִ֛יתָ הַמּוֹצִ֥יא וְהַמֵּבִ֖יא'),
    'pcl': ('171A', 1, 20),
    'manuscript': ['supports ∅+k1q1×2', my_html.line_break(), 'rather than WLC’s k1q1×3'],
    'intro': [
        'In WLC, the k/q differences of the first two words are about a word boundary, '
        'but the manuscript does not support that. '
        'Indeed the first k1q1 in WLC, הייתה/היית, '
        'corresponds to a normal word in the manuscript, as the following image shows'
    ]
}
EZRA_4_12 = [
    my_html.para(
        [
            'I think I understand the impulse behind this WLC change, '
            'but nonetheless I find the change inadvisable. '
            'So I not only support UXLC’s rejection of this change '
            'but also advise WLC to revert this change in some future version.',
        ]
    ),
    my_html.para(
        [
            'My guess is that the impulse behind this change is '
            'that we are primarily dealing with a word boundary issue here, '
            'so a single k2q2 seems more appropriate than '
            'two adjacent k1q1 constructs, '
            'a configuration we sometimes abbreviate as k1q1×2. '
            '(There is a ',
            rmn('ḥaser/malei'),
            ' issue later in the second word, '
            'but the primary issue is the word boundary issue.) '
            'The word boundary issue is about a difference between ',
            rmn('qere'), ' and ', rmn('ketiv'),
            ' as to where the word boundary falls within the letters '
            'ושוריאשכל[י]לו.) '
            'The table below shows the details.'
        ]
    ),
    my_html.table([
        my_html.table_row_of_headers(
            ['', '', 'word boundary']
        ),
        my_html.table_row_of_data(
            [rmn('ketiv'), 'ושורי אשכללו', 'before the א'],
            [None, _HBO_RTL_BIG, None]
        ),
        my_html.table_row_of_data(
            [rmn('qere'), 'וְשׁוּרַיָּ֣א שַׁכְלִ֔ילוּ', 'after the א'],
            [None, _HBO_RTL_BIG, None]
        )
    ]),
    my_html.para(
        [
            'Because we are primarily dealing with a word boundary issue, '
            'it is an understandable impulse to group these 4 words into a single k2q2 construct '
            '(which is what WLC 4.22 now has) '
            'rather than group them into two adjacent k1q1 constructs. '
            '(which is what WLC 4.20 had). '
            'The table below shows what these two grouping strategies look like in Michigan-Claremont terms.',
        ]
    ),
    my_html.table([
        my_html.table_row_of_data(['k2q2', '*ka', '*kb', '**qa', '**qb']),
        my_html.table_row_of_data(['k1q1×2', '*ka', '**qa', '*kb', '**qb'])
    ]),
    my_html.para(
        [
            'Although the impulse is understandable, it is not consistent with the diplomatic spirit of '
            'WLC to allow such an impulse to override what we see in the manuscript. '
            'What we see in the manuscript is the choice to group these words into '
            'two adjacent k1q1 constructs. '
            'BHS and BHQ agree with the manuscript, though of course we’d be willing to reject their '
            'reading if it contradicted the manuscript.'
        ]
    ),
    my_html.heading_level_2('Other k2q2 in WLC'),
    my_html.para(
        [
            'The table below shows two other k2q2 in WLC that are instructive to compare with this Ezra 4:12 one, '
            'since they, too, are about a word boundary.'
        ]
    ),
    my_html.table([
        _bkm_table_row_of_headers(),
        _bkm_table_row(_K2Q2REC_EZEK),
        _bkm_table_row(_K2Q2REC_SND_SAM_21_12),
    ]),
    *_intro_and_img(_K2Q2REC_EZEK),
    *_intro_and_img(_K2Q2REC_SND_SAM_21_12),
    my_html.para(
        [
            'Using square brackets to set off the k2q2 grouping, here’s how WLC and the manuscript '
            'divide up the ', rmn('qere'), ' letters of these three words:'
        ]
    ),
    my_html.table([
        my_html.table_row_of_data(['WLC', 'תלאום [שמה פלשתים]'], [None, {'dir': 'rtl'}]),
        my_html.table_row_of_data(['Ms ל', '[תלאום שמה] פלשתים'], [None, {'dir': 'rtl'}])
    ]),
    my_html.para(
        [
            'Let’s look at the six other k2q2 cases in WLC. '
            'None of these cases are about a word boundary, '
            'but it will still be interesting to see '
            'whether, in each case, the manuscript does or does not support WLC’s k2q2 grouping.'
        ]
    ),
    my_html.table([
        _bkm_table_row_of_headers(),
        _bkm_table_row(_K2Q2REC_FST_KGS),
        _bkm_table_row(_K2Q2REC_FST_SAM),
        _bkm_table_row(_K2Q2REC_ISAIAH),
        _bkm_table_row(_K2Q2REC_JOB_38V12),
        _bkm_table_row(_K2Q2REC_JOB_38V01),
        _bkm_table_row(_K2Q2REC_JOB_40),
    ]),
    *_intro_and_img(_K2Q2REC_FST_KGS),
    *_intro_and_img(_K2Q2REC_FST_SAM),
    *_intro_and_img(_K2Q2REC_ISAIAH),
    *_intro_and_img(_K2Q2REC_JOB_38V12),
    *_JOB_38_1_and_40_6_PARAS,
    *_intro_and_img(_K2Q2REC_JOB_38V01),
    *_intro_and_img(_K2Q2REC_JOB_40),
    my_html.para(
        [
            'Having completed our review of k2q2 in WLC, we can say that some are '
            'supported by the manuscript, and some are not. '
            'I would urge WLC, in future versions, to use k2q2 only when supported by the manuscript.'
        ]
    ),
    my_html.heading_level_2('k1q1×2, k1q1×3, etc. in WLC'),
    my_html.para(
        [
            'It would be nice to also review all cases of multiple adjacent k1q1 in WLC to see if all of them '
            'are supported by the manuscript. '
            'I wonder whether, for example, some instances of k1q1×2 in WLC should in fact be represented as k2q2. '
            'I do not propose to do this (possibly rather large) survey at the moment, but one problematic case has, '
            'almost accidentally, come to my attention, and I will discuss it here. ',
            my_html.span(
                'That problematic case is the following k1q1×3 in 2 Samuel 5:2:',
                {'id': 'SndSam5v2'}
            )
        ]
    ),
    my_html.table([
        _bkm_table_row_of_headers(),
        _bkm_table_row(_BKM_REC_SND_SAM_5_2),
        #_bkm_table_row(_BKM_REC_PROV_21_29),
    ]),
    *_intro_and_img(_BKM_REC_SND_SAM_5_2),
    my_html.para([
        'In other words the manuscript considers the ה of the ', rmn('qere'), ' המוציא ',
        'to come from nowhere, not from the end of הייתה. '
        'Note that in ל, the ', rmn('pataḥ'), ' intended for this ה is an orphan, floating out in '
        'a lonely fashion before the ', rmn('ketiv'), ' letters מוציא.'
    ]),
    my_html.para([
        'The Aleppo Codex (Ms א) is rarely relevant to WLC, but here it is perhaps useful to look at it. '
        'Ms א treats these words quite differently than ל does. '
        'Unlike ל, Ms א does consider the ה of the ', rmn('qere'), ' המוציא ',
        'to come from the end of הייתה, as indicated by the following: '
    ]),
    my_html.unordered_list([
        'היית rather than הייתה are the qere letters',
        'the final ה of הייתה is pointed with pataḥ, i.e. הייתהַ',
        ['the ', rmn('qere'), ' words היית המוציא are grouped together']
    ]),
    my_html.para([
        'Also unlike ל, Ms א considers והמבי to be a normal word, not a ', rmn('ketiv'), ' '
        'needing a final א to form a ', rmn('qere'), '. '
        'Ms א does note the lack of a final א, with “חס א” with a splotch above that may have been a numeral, '
        'perhaps a ', rmn('vav'), ' meaning “6 times lacking [a final] א”. '
        'All this can be seen in the following image: ',
        my_html_for_img.html_for_single_img('2Sam5v2-Aleppo.png')
    ]),
    my_html.para([
        'So we could say that WLC represents the k/q of Samuel 5:2 as an uncomfortable mix '
        'of the traditions we see in ל and א, whereas, '
        'according to its charter, WLC should hew to ל. '
        '(I very much doubt that א actually influenced BHS but I suspect that the tradition captured in א appears '
        'in the Second Rabbinic Bible (Second Venice Miqraot Gedolot) and it is through that influential edition '
        'that BHS (and hence WLC) ended up with this content not supported by ל.)'
    ]),
    my_html.heading_level_2('Conclusion'),
    my_html.para(
        [
            'Finally, we should admit that ', rmn('qere'), ' grouping '
            'may have been left up to individual scribal discretion. '
            'In other words, ', rmn('qere'), ' grouping '
            'may not have been viewed as meaningful by the Masoretes. '
            'Just as we do not distinguish a normal ', rmn('lamed'),
            ' letter from the occasional elongated one, ',
            'perhaps we should not be concerned to preserve ', rmn('qere'), ' grouping, '
            'particularly when we don’t like the  manuscript’s grouping.'
        ]
    ),
    my_html.para(
        [
            'That having been said, it seems more consistent with the diplomatic spirit '
            'of WLC to err on the safe side by preserving ', rmn('qere'), ' grouping. '
            'For example this is what BHS did, and WLC continues to do, with respect to ', *_GAYA_PAREN_METEG, ' '
            'placement. '
            'In the 50-or-so years since the publication of BHS, scholarship has reached a consensus '
            'that ', rmn('gaʿya'), ' placement was not viewed as meaningful by the Masoretes. '
            'I.e. the consensus is that ', rmn('gaʿya'), ' placment '
            'was left up to scribal discretion. '
            'Still, at the time, perhaps it was the right decision for BHS to err on the safe side by preserving '
            '', rmn('gaʿya'), ' placement. '
            'I urge WLC to follow this example and '
            'err on the safe side by preserving ', rmn('qere'), ' grouping. '
        ]
    ),
]
