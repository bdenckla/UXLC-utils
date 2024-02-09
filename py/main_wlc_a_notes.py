""" Exports main. """

import my_wlc_a_notes
import my_html
import my_utils


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
    return my_html.table_datum(val)


def _rec_to_row(rec):
    row_cells = list(map(_rec_kv_to_row_cell, rec.items()))
    return my_html.table_row(row_cells)


def main():
    """ Writes docs/index.html. """
    rows = list(map(_rec_to_row, my_wlc_a_notes.RECORDS))
    table = my_html.table(rows)
    body_contents = [table]
    write_ctx = my_html.WriteCtx('WLC a-notes', 'docs/index.html')
    my_html.write_html_to_file(body_contents, write_ctx)


if __name__ == "__main__":
    main()
