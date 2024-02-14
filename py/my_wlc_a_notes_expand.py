""" Exports expand. """


def expand(io_records):
    """
    Add fields including uxlc-change-proposal-sequential.
    """
    ucp_count = 0
    ucp_dic = {}
    for record in io_records:
        _add_reason(record)
        ucp = record['uxlc-change-proposal']
        if isinstance(ucp, int):
            assert ucp not in ucp_dic
            ucp_dic[ucp] = True
            ucp_count += 1
            record['uxlc-change-proposal-sequential'] = ucp_count


def _add_reason(io_record):
    summ_in = io_record['summary']
    atiss_in = io_record['at issue']
    summ_out = _SUMMARY_MAP[summ_in]
    atiss_key = summ_in, atiss_in
    atiss_out = _AT_ISSUE_MAP[atiss_key]
    io_record['at issue English'] = f'{summ_out}{atiss_out}'


_AT_ISSUE_MAP = {
    ('אֻ to אוּ', 'וּ'): '',
    ('+mqf', '־'): '',
    ('הּ', 'הּ'): '',
    ('?', '?'): 'unclear',
    #
    ('+dgsh', 'בּ'): ' to bet',
    ('+dgsh', 'וָּ'): ' to vav-qamats',
    ('+dgsh', 'פּ'): ' to pe',
    ('+dgsh', 'יּ'): ' to yod',
    ('+dgsh', 'דּ'): ' to dalet',
    ('+dgsh', 'כּ'): ' to kaf',
    ('+dgsh', 'טּ'): ' to tet',
    ('+dgsh', 'לּ'): ' to lamed',
    ('+dgsh', 'צּ'): ' to tsadi',
    ('+shrq dt', 'וּ'): ' to the initial vav',
    #
    ('+ḥlm dt', 'וֹ'): ' to vav',
    ('+shva', 'ךְ'): ' to kaf sofit',
    ('+shva', 'נְ'): ' to nun',
    #
    ('עֲ to עַ', 'עַ'): ' under ayin',
    #
    ('-dgsh', 'מ'): ' from mem',
}


_SUMMARY_MAP = {
    'אֻ to אוּ': 'changed a qubuts to a shuruq',
    '+mqf': 'added a maqaf',
    '+dgsh': 'added a dagesh',
    '-dgsh': 'removed a dagesh',
    'הּ': 'added a mapiq to he',
    '+shrq dt': 'added a shuruq dot',
    '+ḥlm dt': 'added a ḥolam malei dot',
    '+shva': 'added a sheva',
    'עֲ to עַ': 'changed a ḥataf pataḥ to a pataḥ',
    '?': '',
}
