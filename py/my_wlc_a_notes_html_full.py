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


def _write_record(record):
    body_contents = []
    wlc_index = record['wlc-index']
    bcv = record['bcv']
    qere = record['qere']
    mpk = record['MPK']
    atiss = record['at issue']
    remarks = record['remarks']
    side_notes = record.get('side-notes') or []
    #
    body_contents.append(my_html.para(qere, {'lang': 'hbo', 'dir': 'rtl'}))
    body_contents.append(my_html.para(mpk, {'lang': 'hbo', 'dir': 'rtl'}))
    body_contents.append(my_html.para(atiss, {'lang': 'hbo', 'dir': 'rtl'}))
    #
    href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(bcv)
    anchor = my_html.anchor(bcv, {'href': href})
    body_contents.append(my_html.para(anchor))
    #
    for remark in remarks:
        body_contents.append(my_html.para(remark))
    #
    for side_note in side_notes:
        body_contents.append(my_html.para(side_note))
    #
    wlc_index_str = _wlc_index_str(wlc_index)
    title = f'WLC a-note {wlc_index_str}'
    path = f'docs/wlc_a_note_{wlc_index_str}.html'
    write_ctx = my_html.WriteCtx(title, path)
    my_html.write_html_to_file(body_contents, write_ctx)
