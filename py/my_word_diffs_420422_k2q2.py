import my_html
import my_html_for_img
from my_html_span_romanized import rmn

def _html_for_pcl(pcl):
    page, column, line = pcl
    return [
        my_html.anchor(
            f'page {page}',
            {'href': f'https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg'}
        ),
        f' col {column} line {line}'
    ]


def _html_for_bcv_str_wlt_tdu(bcv_str):  # wlt_tdu: with link to tanach.us
    return my_html.anchor(
        bcv_str,
        {'href': f'https://tanach.us/Tanach.xml?{bcv_str}'}
    )


_FST_SAM_20_2_UXLC = 'https://tanach.us/Tanach.xml?1Sam20:2'
_FST_SAM_20_2_IMG = 'https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F161B.jpg'
_FST_SAM_20_2_PCL = '161B', 2, 17

_SND_SAM_21_12_KQ = ['שם הפלשתים', my_html.line_break(), 'שָׁ֙מָּה֙ פְּלִשְׁתִּ֔ים']
_SND_SAM_21_12_BCV_STR = '2Sam21:12'
_SND_SAM_21_12_PCL = '181B', 2, 12

_EZEK_42_9_KQ = ['ומתחתה לשכות', my_html.line_break(), 'וּמִתַּ֖חַת הַלְּשָׁכ֣וֹת']
_EZEK_42_9_BCV_STR = 'Ezek42:9'
_EZEK_42_9_PCL = '299B', 3, 22

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
            'that we are primarily dealing with a word boundary issue here. '
            'There is a ',
            rmn('ḥaser/malei'),
            ' issue later in the second word, '
            'but the primary issue is where the word boundary falls within the letters '
            'ושוריאשכל[י]לו. '
            'The table below shows the details.'
        ]
    ),
    my_html.table([
        my_html.table_row([
            my_html.table_header([]),
            my_html.table_header([]),
            my_html.table_header('word boundary'),
        ]),
        my_html.table_row([
            my_html.table_datum(rmn('ketiv')),
            my_html.table_datum('ושורי אשכללו'),
            my_html.table_datum('before the א'),
        ]),
        my_html.table_row([
            my_html.table_datum(rmn('qere')),
            my_html.table_datum('ושוריא שכלילו'),
            my_html.table_datum('after the א'),
        ])
    ]),
    my_html.para(
        [
            'Because we are primarily dealing with a word boundary issue, '
            'it is an understandable impulse to group these 4 words into a single k2q2 construct '
            '(which is what WLC 4.22 now has) '
            'rather than group them into a k1q1×2 (two adjacent k1q1 constructs) '
            '(which is what WLC 4.20 had). '
            'The table below shows what these constructs look like in Michigan-Claremont terms.',
        ]
    ),
    my_html.table([
        my_html.table_row([
            my_html.table_datum('k2q2'),
            my_html.table_datum('*ka'),
            my_html.table_datum('*kb'),
            my_html.table_datum('**qa'),
            my_html.table_datum('**qb'),
        ]),
        my_html.table_row([
            my_html.table_datum('k1q1×2'),
            my_html.table_datum('*ka'),
            my_html.table_datum('**qa'),
            my_html.table_datum('*kb'),
            my_html.table_datum('**qb'),
        ])
    ]),
    my_html.para(
        [
            'Although the impulse is understandable, it is not consistent with the diplomatic spirit of '
            'WLC to allow such an impulse to override what we see in the manuscript. '
            'What we see in the manuscript is the choice to treat these words as k1q1×2: '
            'two adjacent k1q1 constructs. '
            'BHS and BHQ agree with the manuscript, though of course we’d be willing to reject their '
            'reading if it contradicted the manuscript.'
        ]
    ),
    my_html.para(
        [
            'The table below shows two other k2q2 that are instructive to compare, '
            'since they, too, concern word division.'
        ]
    ),
    my_html.table([
        my_html.table_row([
            my_html.table_datum(_html_for_bcv_str_wlt_tdu(_EZEK_42_9_BCV_STR)),
            my_html.table_datum(_EZEK_42_9_KQ, {'class': 'big'}),
        ]),
        my_html.table_row([
            my_html.table_datum(_html_for_bcv_str_wlt_tdu(_SND_SAM_21_12_BCV_STR)),
            my_html.table_datum(_SND_SAM_21_12_KQ, {'class': 'big'}),
        ]),
    ]),
    my_html.para(
        [
            'In the case of Ezekiel 42:9, we find that the manuscript supports the k2q2 grouping '
            '(', *_html_for_pcl(_EZEK_42_9_PCL), '):'
        ]
    ),
    my_html_for_img.html_for_single_img('Ezek42v9.png'),
    my_html.para(
        [
            'But in the case of 2 Samuel 21:12, we find that the manuscript supports a different k2q2 grouping! '
            'This k2q2 reaches back one word earlier than the two words of WLC’s k2q2 '
            '(', *_html_for_pcl(_SND_SAM_21_12_PCL), '):'
        ]
    ),
    my_html_for_img.html_for_single_img('2Sam21c12.png'),
    my_html.para(
        [
            'Using square brackets to set off the k2q2 grouping, here’s how WLC and the manuscript '
            'divide up the ', rmn('qere'), ' letters of these three words:'
        ]
    ),
    my_html.table([
        my_html.table_row([
            my_html.table_datum('WLC'),
            my_html.table_datum('תלאום [שמה פלשתים]', {'dir': 'rtl'}),
        ]),
        my_html.table_row([
            my_html.table_datum('Ms ל'),
            my_html.table_datum('[תלאום שמה] פלשתים', {'dir': 'rtl'}),
        ]),
    ]),
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
            'For example this is what BHS did, and WLC continues to do, with respect to meteg '
            'placement. '
            'In the 50-or-so years since the publication of BHS, scholarship has reached a consensus '
            'that meteg placement was not viewed as meaningful by the Masoretes. '
            'I.e. the consensus is that meteg placment '
            'was left up to scribal discretion. '
            'Still, at the time, perhaps it was the right decision for BHS to err on the safe side by preserving '
            'meteg placement.'
        ]
    ),
]
