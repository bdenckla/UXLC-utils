""" Exports write_xml. """

import my_html
import my_convert_citation_from_wlc_to_uxlc
import my_wlc_a_notes_img as img


def write(io_records):
    """ Write records out in full format. """
    for io_record in io_records:
        io_record['path-to-full'] = _write_record(io_record)


_HBO_RTL = {'lang': 'hbo', 'dir': 'rtl'}


def _make_key_value_row(key, value, hbo=False):
    cell_for_key = my_html.table_datum(key)
    attr = _HBO_RTL if hbo else None
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
    path = f'full-record/wlc_a_note_{wlc_index:02}.html'
    write_ctx = my_html.WriteCtx(title, f'docs/wlc-a-notes/{path}')
    my_html.write_html_to_file(body_contents, write_ctx, '../')
    return path


def _append_remarks_and_side_notes(io_body_contents, record):
    remarks = record['remarks']
    for remark in remarks:
        assert not remark.endswith(' ')
        io_body_contents.append(my_html.para(remark))
    #
    side_notes = record.get('side-notes') or []
    for side_note in side_notes:
        assert not side_note.endswith(' ')
        hesp = _hebrew_spanify(side_note)
        io_body_contents.append(my_html.para(hesp))


def _hebrew_spanify(string: str):
    pre, sep, post = string.partition('@')
    pre_list = [pre] if pre else []
    if not sep:
        assert not post
        assert pre == string
        return pre_list
    return pre_list + _hebrew_spanify2(post)


def _hebrew_spanify2(string: str):
    pre, sep, post = string.partition('#')
    assert sep
    assert sep == '#'
    return [my_html.span(pre, {'lang': 'hbo'}), *_hebrew_spanify(post)]


def _initial_rows(record):
    anchor = _anchor(record)
    mpk = record['MPK']
    qere = record['qere']
    atiss = record['at issue']
    reason = record.get('at issue English')
    rows = []
    rows.append(_make_key_value_row('bcv (link to tanach.us)', anchor))
    rows.append(_make_key_value_row('MPK', mpk, hbo=True))
    if qere_c := record.get('qere-context'):
        rows.append(_make_key_value_row('qere-context', qere_c, hbo=True))
    rows.append(_make_key_value_row('qere', qere, hbo=True))
    if qere_a := record.get('qere-atom-at-issue'):
        rows.append(_make_key_value_row('qere-atom-at-issue', qere_a, hbo=True))
    rows.append(_make_key_value_row('at issue', atiss, hbo=True))
    rows.append(_make_key_value_row('at issue English', reason))
    return rows


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
    if 'folio' in record:
        # XXX make this into a link like:
        # https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F159B.jpg
        #
        prefix = 'Folio_'
        assert record['folio'].startswith(prefix)
        folio_short = record['folio'].removeprefix(prefix)
        assert folio_short
        focoli_tuple = folio_short, str(record['column']), _line_str(record)
        focoli_str = ' '.join(focoli_tuple)
        return _make_key_value_row('folio col line', focoli_str)
    return None