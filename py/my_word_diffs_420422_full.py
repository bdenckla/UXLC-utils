""" Exports write_xml. """

import my_html
import my_word_diffs_420422_utils as wd_utils
import my_html_for_img as img
import my_url_generator as urlg


def write(io_records):
    """ Write records out in full format. """
    for io_record in io_records:
        io_record['path-to-full'] = _write_record(io_record)


_HBO_RTL = {'lang': 'hbo', 'dir': 'rtl', 'class': 'big'}


def _make_key_value_row(key, value, big_hbo=False):
    cell_for_key = my_html.table_datum(key)
    attr = _HBO_RTL if big_hbo else None
    cell_for_value = my_html.table_datum(value, attr)
    return my_html.table_row([cell_for_key, cell_for_value])


def _write_record(record):
    #
    body_contents = []
    #
    body_contents.append(my_html.para(_navs(record)))
    #
    if html_for_i := img.html_for_img_or_imgs(record):
        body_contents.extend(html_for_i)
    #
    rows = _initial_rows(record)
    #
    if folio_row := _folio_row(record):
        rows.append(folio_row)
    #
    body_contents.append(my_html.table(rows, {'class': 'limited-width'}))
    #
    _append_remarks_and_side_notes(body_contents, record)
    #
    orord = record['original-order']
    title = f'WLC 4.20 to 4.22 diff {orord}'
    filename = _filename(orord)
    path = f'full-record/{filename}'
    write_ctx = my_html.WriteCtx(title, f'docs/420422/{path}')
    my_html.write_html_to_file(body_contents, write_ctx, '../../')
    return path


def _navs(record):
    navs = []
    _maybe_append_nav(navs, record, 'prev', 'Prev')
    _maybe_append_nav(navs, record, 'next', 'Next')
    return navs


def _maybe_append_nav(io_navs, record, key, human_readable):
    if pn_rec := record.get(key):  # previous or next rec
        if io_navs:
            io_navs.append(' ')
        io_navs.append(_anchor_for_nav(human_readable, pn_rec))


def _anchor_for_nav(pn_str, record):
    orord = record['original-order']
    return my_html.anchor(pn_str, {'href': _filename(orord)})


def _filename(orord):
    return f'420422-{orord:02}.html'


def _append_remarks_and_side_notes(io_body_contents, record):
    if initial_remark := record.get('initial-remark'):
        assert not initial_remark.endswith(' ')
        io_body_contents.append(my_html.para(initial_remark))
    #
    if further_remarks := record.get('further-remarks'):
        for fur_remark in further_remarks:
            assert not fur_remark.endswith(' ')
            hesp_fur = _hebrew_spanify(fur_remark)
            io_body_contents.append(my_html.para(hesp_fur))


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
    bcv_with_link_to_tdu = urlg.bcv_with_link_to_tdu(record)
    bcv_with_link_to_mwd = urlg.bcv_with_link_to_mwd(record)
    ab_uword_br = _newline_to_br(record['ab-uword'])
    ab_word_br = _newline_to_br(record['ab-word'])
    rows = []
    rows.append(_make_key_value_row('bcv (link to tanach.us)', bcv_with_link_to_tdu))
    rows.append(_make_key_value_row('bcv (link to Mwd)', bcv_with_link_to_mwd))
    # rows.append(_make_key_value_row('img file name', record['img']))
    rows.append(_make_key_value_row('ab-uword', ab_uword_br, big_hbo=True))
    rows.append(_make_key_value_row('ab-word', ab_word_br))
    _append_uxlc_change_proposals(rows, record)
    rows.append(_make_key_value_row('diff type', wd_utils.diff_type_long(record)))
    rows.append(_make_key_value_row('diff desc', record['diff-desc']))
    rows.append(_make_key_value_row('page', _page_with_link_to_img(record)))
    rows.append(_make_key_value_row(*_colx_and_linex(record)))
    return rows


def _append_uxlc_change_proposals(rows, record):
    ucps = wd_utils.uxlc_change_proposals(record)
    for ucp_idx, ucp in enumerate(ucps):
        qualifier = f' {ucp_idx+1}' if len(ucps) > 1 else ''
        anchor = urlg.uxlc_change_with_link(ucp)
        rows.append(_make_key_value_row(f'UXLC change proposal{qualifier}', anchor))


def _newline_to_br(nssp):  # nssp newline-separated string-pair
    elem1of2, elem2of2 = nssp.split('\n')
    return [elem1of2, my_html.line_break(), elem2of2]


def _colx_and_linex(record):
    if record.get('line'):
        return 'col-and-line', _cole_and_linee(record)
    return 'col-guess-and-line-guess', _colg_and_lineg(record)


def _cole_and_linee(record):
    # cole: column, exact
    # linee: line, exact
    # If line is given, and column is not given, we assume column guess was right.
    column = record.get('column') or record['column-guess']
    line = record['line']
    return f'{column} {line}'


def _colg_and_lineg(record):
    columng = record['column-guess']
    lineg = record['line-guess']
    return f'{columng} {lineg}'


def _page_with_link_to_img(record):
    page = record['page']
    href = f'https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F{page}.jpg'
    return my_html.anchor(page, {'href': href})


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
