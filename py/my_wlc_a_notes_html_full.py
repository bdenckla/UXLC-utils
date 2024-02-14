""" Exports write_xml. """

import my_html
import my_convert_citation_from_wlc_to_uxlc
import my_wlc_a_notes_img_html as img


def write(io_records):
    """ Write records out in full format. """
    for io_record in io_records:
        io_record['path-to-full'] = _write_record(io_record)


def _make_key_value_row(key, value, hbo=False):
    cell_for_key = my_html.table_datum(key)
    if hbo:
        attr = {'lang': 'hbo', 'dir': 'rtl'}
    else:
        attr = None
    cell_for_value = my_html.table_datum(value, attr)
    return my_html.table_row([cell_for_key, cell_for_value])


def _write_record(record):
    #
    body_contents = []
    if html_for_i := img.html_for_img_or_imgs(record):
        body_contents.extend(html_for_i)
    #
    rows = _initial_rows(record)
    ucp = record['uxlc-change-proposal']
    if isinstance(ucp, str):
        # XXX make this a real link
        rows.append(_make_key_value_row('existing UCP', ucp))
    #
    if folio_row := _folio_row(record):
        rows.append(folio_row)
    #
    body_contents.append(my_html.table(rows))
    #
    _append_remarks_and_side_notes(body_contents, record)
    #
    wlc_index = record['wlc-index']
    title = f'WLC a-note {wlc_index}'
    path = f'wlc_a_note_{wlc_index:02}.html'
    write_ctx = my_html.WriteCtx(title, f'docs/{path}')
    my_html.write_html_to_file(body_contents, write_ctx)
    return path


def _append_remarks_and_side_notes(io_body_contents, record):
    remarks = record['remarks']
    side_notes = record.get('side-notes') or []
    for remark in remarks:
        assert not remark.endswith(' ')
        io_body_contents.append(my_html.para(remark))
    #
    for side_note in side_notes:
        assert not side_note.endswith(' ')
        io_body_contents.append(my_html.para(side_note))


def _initial_rows(record):
    anchor = _anchor(record)
    mpk = record['MPK']
    qere = record['qere']
    atiss = record['at issue']
    reason = record.get('at issue English')
    return [
        _make_key_value_row('bcv (link to tanach.us)', anchor),
        _make_key_value_row('MPK', mpk, hbo=True),
        _make_key_value_row('qere', qere, hbo=True),
        _make_key_value_row('at issue', atiss, hbo=True),
        _make_key_value_row('at issue English', reason),
    ]


def _anchor(record):
    bcv = record['bcv']
    href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(bcv)
    return my_html.anchor(bcv, {'href': href})


def _line_str(record):
    if 'line' in record:
        return str(record['line'])
    assert 'line-excluding-blanks' in record
    assert 'line-including-blanks' in record
    leb = record['line-excluding-blanks']
    lib = record['line-including-blanks']
    return str(leb) + '/' + str(lib)


def _folio_row(record):
    if 'folio' in record and record['folio'] != 'XXX fill me in folio':
        # XXX make this into a link like:
        # https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F159B.jpg
        #
        prefix = 'Folio_'
        assert record['folio'].startswith(prefix)
        folio_short = record['folio'].removeprefix(prefix)
        focoli_tuple = folio_short, str(record['column']), _line_str(record)
        focoli_str = ' '.join(focoli_tuple)
        return _make_key_value_row('folio col line', focoli_str)
    return None
