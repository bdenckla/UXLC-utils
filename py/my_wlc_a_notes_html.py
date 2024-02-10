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


def _rec_kv_to_row_cell(kv_pair):
    key, val = kv_pair
    if key == 'remarks':
        assert isinstance(val, list)
        br = my_html.line_break()
        rems_with_brs = my_utils.intersperse(br, val)
        return my_html.table_datum(rems_with_brs)
    assert isinstance(val, str)
    if key in ('qere', 'MPK', 'at issue'):
        return my_html.table_datum(val, {'lang': 'hbo', 'dir': 'rtl'})
    if key == 'bcv':
        href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(val)
        anchor = my_html.anchor(val, {'href': href})
        return my_html.table_datum(anchor)
    return my_html.table_datum(val)


def _rec_to_row(rec):
    row_cells = list(map(_rec_kv_to_row_cell, rec.items()))
    return my_html.table_row(row_cells)


def _row_for_header():
    strs_for_cells_for_header = [
        'bcv', 'Dotan', 'WLC qere', 'MPK', 'at issue', 'summary', 'remarks']
    cells_for_header = list(map(my_html.table_datum, strs_for_cells_for_header))
    return my_html.table_row(cells_for_header)


