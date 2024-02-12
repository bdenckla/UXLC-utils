""" Exports expand. """


def expand(io_records):
    """
    Add fields including uxlc-change-proposal-sequential.
    """
    ucp_count = 0
    for record in io_records:
        ucp = record['uxlc-change-proposal']
        if isinstance(ucp, int):
            ucp_count += 1
            record['uxlc-change-proposal-sequential'] = ucp_count
            _add_description(record)


def _add_description(io_record):
    summ_in = io_record['summary']
    atiss_in = io_record['at issue']
    summ_out = _SUMMARY_MAP[summ_in]
    atiss_key = summ_in, atiss_in
    atiss_out = _AT_ISSUE_MAP.get(atiss_key) or ''
    #
    desc = f'Note {summ_out}{atiss_out}'
    io_record['uxlc-change-proposal-description'] = desc


_AT_ISSUE_MAP = {
    ('+dgsh', 'בּ'): ' to bet',
    ('+dgsh', 'וָּ'): ' to vav-qamats',
    ('+dgsh', 'פּ'): ' to pe',
    ('+dgsh', 'יּ'): ' to yod',
    ('+dgsh', 'דּ'): ' to dalet',
    ('+dgsh', 'כּ'): ' to kaf',
    ('+mapiq', 'הּ'): ' to he',
    ('+dgsh', 'טּ'): ' to tet',
    ('+dgsh', 'לּ'): ' to lamed',
    ('+dgsh', 'צּ'): ' to tsadi',
    #
    ('+shrq dt', 'וּ…'): ' to initial vav',
    ('+ḥlm dt', 'וֹ'): ' to vav',
    ('+shva', 'ךְ'): ' to final form of kaf',
    ('ḥtf ptḥ to ptḥ', 'עַ'): ' under ayin',
    #
    ('-dgsh', 'מ'): ' from mem',
}


_SUMMARY_MAP = {
    'qbts to shrq': 'qubuts to shuruq',
    '+mqf': 'added maqaf',
    '+dgsh': 'added dagesh',
    '-dgsh': 'removed dagesh',
    '+mapiq': 'added mapiq',
    '+shrq dt': 'added shuruq dot',
    '+ḥlm dt': 'added ḥolam malei dot',
    '+shva': 'added sheva',
    'ḥtf ptḥ to ptḥ': 'ḥataf pataḥ to pataḥ'
}
