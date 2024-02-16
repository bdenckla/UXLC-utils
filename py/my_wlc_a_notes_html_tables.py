""" Exports write_html. """

import my_convert_citation_from_wlc_to_uxlc
import my_wlc_a_notes_intro
import my_utils
import my_html



def write(records):
    """ Writes WLC a-notes records to docs/index.html. """
    _write2(records, my_wlc_a_notes_intro.INTRO, 'WLC a-notes', 'docs/wlc-a-notes/index.html')
    records_in_wlc_order = sorted(records, key=_get_wlc_index)
    _write2(records, [], 'WLC a-notes in WLC order', 'docs/wlc-a-notes/table-in-wlc-order.html')



def _write2(records, intro, title, path):
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table = my_html.table(rows)
    body_contents = [*intro, table]
    write_ctx = my_html.WriteCtx(title, path)
    my_html.write_html_to_file(body_contents, write_ctx)


def _get_wlc_index(rec):
    return rec['wlc-index']


_REC_KEY_FROM_HDR_STR = {
    'WLC qere': 'qere',
    'AI': 'at issue',
    'AIC': 'summary',
}
_HBO_VALS = {
    'אֻ/אוּ': True,
    'הּ': True,
    'עֲ/עַ': True,
}


def _row_cell_for_hdr_str(rec, hdr_str):
    rec_key = _REC_KEY_FROM_HDR_STR.get(hdr_str) or hdr_str
    val = rec[rec_key]
    if rec_key == 'remarks':
        assert isinstance(val, list)
        assert len(val) in (0, 1)
        anchors = _get_anchors_to_full_and_ucp(rec)
        if val:
            datum_contents = [*anchors, '; ', *val]
        else:
            datum_contents = anchors
        return my_html.table_datum(datum_contents)
    assert isinstance(val, str)
    if rec_key in ('qere', 'MPK', 'at issue') or _HBO_VALS.get(val):
        return my_html.table_datum(val, {'lang': 'hbo', 'dir': 'rtl'})
    if rec_key == 'bcv':
        href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(val)
        anchor = my_html.anchor(val, {'href': href})
        return my_html.table_datum(anchor)
    return my_html.table_datum(val)


def _get_anchors_to_full_and_ucp(rec):
    path_to_full = rec['path-to-full']
    anchor_to_full = my_html.anchor('full', {'href': path_to_full})
    path_to_ucp = rec.get('path-to-ucp')
    if path_to_ucp:
        something_for_ucp = my_html.anchor('UCP', {'href': path_to_ucp})
    else:
        something_for_ucp = '(no UCP)'
    return [anchor_to_full, '; ', something_for_ucp]


def _rec_to_row(rec):
    row_cells = my_utils.ll_map(
        (_row_cell_for_hdr_str, rec),
        strs_for_cells_for_header)
    return my_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(map(my_html.table_header, strs_for_cells_for_header))
    return my_html.table_row(cells_for_header)


strs_for_cells_for_header = [
    'bcv', 'MPK', 'WLC qere', 'AI', 'AIC', 'remarks']
