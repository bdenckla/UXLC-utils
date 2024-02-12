""" Exports write_xml. """

import my_html
import my_convert_citation_from_wlc_to_uxlc


def write(records):
    """ Write records out in full format. """
    for record in records:
        _write_record(record)


def _wlc_index_str(wlc_index):
    if isinstance(wlc_index, int):
        return f'{wlc_index:02}'
    assert isinstance(wlc_index, list)
    assert len(wlc_index) == 2
    assert isinstance(wlc_index[0], int)
    assert isinstance(wlc_index[1], int)
    main = wlc_index[0]
    sub = wlc_index[1]
    return f'{main:02}sub{sub}'


def _make_key_value_row(key, value, hbo=False):
    cell_for_key = my_html.table_datum(key)
    if hbo:
        attr = {'lang': 'hbo', 'dir': 'rtl'}
    else:
        attr = None
    cell_for_value = my_html.table_datum(value, attr)
    return my_html.table_row([cell_for_key, cell_for_value])


def _write_record(record):
    body_contents = []
    wlc_index = record['wlc-index']
    bcv = record['bcv']
    mpk = record['MPK']
    qere = record['qere']
    atiss = record['at issue']
    reason = record.get('at issue English')
    remarks = record['remarks']
    side_notes = record.get('side-notes') or []
    #
    href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(bcv)
    anchor = my_html.anchor(bcv, {'href': href})
    #
    rows = [
        _make_key_value_row('bcv (link to tanach.us)', anchor),
        _make_key_value_row('MPK', mpk, hbo=True),
        _make_key_value_row('qere', qere, hbo=True),
        _make_key_value_row('at issue', atiss, hbo=True),
        _make_key_value_row('at issue English', reason),
    ]
    #
    body_contents.append(my_html.table(rows))
    #
    for remark in remarks:
        assert not remark.endswith(' ')
        body_contents.append(my_html.para(remark))
    #
    for side_note in side_notes:
        assert not side_note.endswith(' ')
        body_contents.append(my_html.para(side_note))
    #
    wlc_index_str = _wlc_index_str(wlc_index)
    title = f'WLC a-note {wlc_index_str}'
    path = f'docs/wlc_a_note_{wlc_index_str}.html'
    write_ctx = my_html.WriteCtx(title, path)
    my_html.write_html_to_file(body_contents, write_ctx)
