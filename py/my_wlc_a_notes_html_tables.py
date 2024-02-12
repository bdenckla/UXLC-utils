""" Exports write_html. """

import my_convert_citation_from_wlc_to_uxlc
import my_utils
import my_html



def write(records):
    """ Writes WLC a-notes records to docs/index.html. """
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table = my_html.table(rows)
    body_contents = [table]
    write_ctx = my_html.WriteCtx('WLC a-notes', 'docs/index.html')
    my_html.write_html_to_file(body_contents, write_ctx)



def _row_cell_for_hdr_str(rec, hdr_str):
    rec_key = 'qere' if hdr_str == 'WLC qere' else hdr_str
    val = rec[rec_key]
    if hdr_str == 'remarks':
        assert isinstance(val, list)
        assert len(val) in (0, 1)
        path = rec['path-to-full']
        anchor = my_html.anchor('full', {'href': path})
        datum_contents = my_utils.intersperse(' ',[*val, anchor])
        return my_html.table_datum(datum_contents)
    assert isinstance(val, str)
    if hdr_str in ('WLC qere', 'MPK', 'at issue'):
        return my_html.table_datum(val, {'lang': 'hbo', 'dir': 'rtl'})
    if hdr_str == 'bcv':
        href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(val)
        anchor = my_html.anchor(val, {'href': href})
        return my_html.table_datum(anchor)
    return my_html.table_datum(val)


def _rec_to_row(rec):
    row_cells = my_utils.ll_map(
        (_row_cell_for_hdr_str, rec),
        strs_for_cells_for_header)
    return my_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(map(my_html.table_header, strs_for_cells_for_header))
    return my_html.table_row(cells_for_header)


strs_for_cells_for_header = [
    'bcv', 'MPK', 'WLC qere', 'at issue', 'summary', 'remarks']
