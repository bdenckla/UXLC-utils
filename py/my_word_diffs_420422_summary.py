""" Exports write_html. """

import my_word_diffs_420422_utils as wd_utils
import my_url_generator as urlg
import my_utils
import my_html



def write(records, path, title, intro=None):
    """ Writes 420422 records to index.html and other HTML files. """
    if intro is None:
        intro = []
    assert isinstance(intro, list)
    table_of_abbrev = wd_utils.diff_type_abbreviation_table()
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table_of_records = my_html.table(rows)
    body_contents = [*intro, table_of_abbrev, table_of_records]
    write_ctx = my_html.WriteCtx(title, f'docs/420422/{path}')
    my_html.write_html_to_file(body_contents, write_ctx, '../')


def _row_cell_for_hdr_str(record, hdr_str):
    if hdr_str == 'remark':
        anchor = _get_anchor_to_full(record)
        ucps_and_ir = _ucps_and_initial_remark(record)
        datum_contents = [anchor, *ucps_and_ir]
        datum_contents = my_utils.intersperse('; ', datum_contents)
        return my_html.table_datum(datum_contents)
    if hdr_str == 'bcv':
        anchor = urlg.bcv_with_link_to_tdu(record)
        return my_html.table_datum(anchor)
    if hdr_str == '4.20 uword':
        ab_uword = record['ab-uword']
        a_uword, _b_uword = ab_uword.split('\n')
        attr = {'lang': 'hbo', 'dir': 'rtl'}
        return my_html.table_datum(a_uword, attr)
    if hdr_str == 'difftype':
        dity_span = wd_utils.diff_type_span_with_title(record)
        return my_html.table_datum(dity_span)
    assert False


def _ucps_and_initial_remark(record):  # ucp: UXLC-change-proposal
    ucps = wd_utils.uxlc_change_proposals(record)
    ucp_anchors = list(map(urlg.uxlc_change_with_link, ucps))
    if initial_remark_or_none := record.get('initial-remark'):
        initial_remark_or_empty_list = [initial_remark_or_none]
    else:
        initial_remark_or_empty_list = []
    return [*ucp_anchors, *initial_remark_or_empty_list]


def _get_anchor_to_full(record):
    path_to_full = record['path-to-full']
    anchor_to_full = my_html.anchor('full', {'href': path_to_full})
    return anchor_to_full


def _rec_to_row(record):
    row_cells = my_utils.ll_map(
        (_row_cell_for_hdr_str, record),
        _STRS_FOR_CELLS_FOR_HEADER)
    return my_html.table_row(row_cells)


def _row_for_header():
    cells_for_header = list(map(my_html.table_header, _STRS_FOR_CELLS_FOR_HEADER))
    return my_html.table_row(cells_for_header)


_STRS_FOR_CELLS_FOR_HEADER = [
    'bcv', 'difftype', '4.20 uword', 'remark']
