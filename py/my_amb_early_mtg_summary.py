""" Exports write_html. """

import my_amb_early_mtg_utils as  aem_utils
import my_utils
import my_html



def write(records):
    """ Writes amb-early-mtg records to index.html and other HTML files. """
    intro = [
    ]
    _write2(records, intro, 'Ambiguous early metegs', 'index.html')


def _write2(records, intro, title, path):
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table = my_html.table(rows)
    body_contents = [*intro, table]
    write_ctx = my_html.WriteCtx(title, f'docs/amb-early-mtg/{path}')
    my_html.write_html_to_file(body_contents, write_ctx)


def _row_cell_for_hdr_str(record, hdr_str):
    if hdr_str == 'initial-remark':
        val = record['initial-remark']
        assert isinstance(val, str)
        anchors = _get_anchors_to_full_and_ucp(record)
        if val:
            datum_contents = [*anchors, '; ', *val]
        else:
            datum_contents = anchors
        return my_html.table_datum(datum_contents)
    if hdr_str == 'bcv':
        val = aem_utils.bcv_str(record)
        href = aem_utils.tanach_dot_us_url(record)
        anchor = my_html.anchor(val, {'href': href})
        return my_html.table_datum(anchor)
    val = record[hdr_str]
    assert isinstance(val, str)
    if hdr_str in ('word',):
        attr = {'lang': 'hbo', 'dir': 'rtl'}
    else:
        assert False
    return my_html.table_datum(val, attr)


def _get_anchors_to_full_and_ucp(record):
    path_to_full = record['path-to-full']
    anchor_to_full = my_html.anchor('full', {'href': path_to_full})
    path_to_ucp = record.get('path-to-ucp')
    if path_to_ucp:
        something_for_ucp = my_html.anchor('UCP', {'href': path_to_ucp})
    else:
        something_for_ucp = '(no UCP)'
    return [anchor_to_full, '; ', something_for_ucp]


def _rec_to_row(record):
    row_cells = my_utils.ll_map(
        (_row_cell_for_hdr_str, record),
        _STRS_FOR_CELLS_FOR_HEADER)
    return my_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(map(my_html.table_header, _STRS_FOR_CELLS_FOR_HEADER))
    return my_html.table_row(cells_for_header)


_STRS_FOR_CELLS_FOR_HEADER = [
    'bcv', 'word', 'initial remark']
