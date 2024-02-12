""" Exports write_html. """

import my_convert_citation_from_wlc_to_uxlc
import my_utils
import my_html



def write(records):
    """ Writes WLC a-notes records to docs/index.html. """
    rows_for_data = list(map(_rec_to_row, records))
    rows = [_row_for_header(), *rows_for_data]
    table = my_html.table(rows)
    body_contents = [*_INTROS, table]
    write_ctx = my_html.WriteCtx('WLC a-notes', 'docs/index.html')
    my_html.write_html_to_file(body_contents, write_ctx)


_THIS_PAGE = (
    'This page describes the 39 words having bracket-a notes '+
    'in WLC. Here is how bracket-a notes are defined in '+
    '“A Reference Guide to the Westminster Leningrad Codex” (WLCmanual420.pdf):'
)
_DEFINITION_OF_AN_A_NOTE = (
    '[The a-note marks adaptations] to a Qere '+
    'that ל and BHS, by their design, do not indicate. '+
    'Usually this indicates the addition of a Maqqef to our Qere text '+
    'that is not present in the margin of ל, '+
    'or [...] the addition of a Dagesh or Mappiq to our Qere text '+
    'that is not present in the Ketiv consonants in the main text of ל.'
)
_THIS_PAGE_ALSO = (
    'This page also provides links to 37 UXLC change proposals related to these bracket-a notes. '+
    '(There are only 37 not 39 because two of the bracket-a notes '+
    'did not motivate a change proposal.)'
)
_THIS_PAGE_USES = (
    'This page uses the initialism “MPK” to stand for “manuscript’s pointed ketiv.”'
)
_INTROS = [
    my_html.para([_THIS_PAGE, my_html.blockquote(_DEFINITION_OF_AN_A_NOTE)]),
    my_html.para([_THIS_PAGE_ALSO]),
    my_html.para([_THIS_PAGE_USES]),
]


def _row_cell_for_hdr_str(rec, hdr_str):
    rec_key = 'qere' if hdr_str == 'WLC qere' else hdr_str
    val = rec[rec_key]
    if hdr_str == 'remarks':
        assert isinstance(val, list)
        assert len(val) in (0, 1)
        anchors = _get_anchors_to_full_and_ucp(rec)
        if val:
            datum_contents = [*val, ' ', *anchors]
        else:
            datum_contents = anchors
        return my_html.table_datum(datum_contents)
    assert isinstance(val, str)
    if hdr_str in ('WLC qere', 'MPK', 'at issue'):
        return my_html.table_datum(val, {'lang': 'hbo', 'dir': 'rtl'})
    if hdr_str == 'bcv':
        href = my_convert_citation_from_wlc_to_uxlc.get_tanach_dot_us_url(val)
        anchor = my_html.anchor(val, {'href': href})
        return my_html.table_datum(anchor)
    return my_html.table_datum(val)


def _get_anchors_to_full_and_ucp(rec):
    path_to_full = rec['path-to-full']
    anchor_to_full = my_html.anchor('full remarks', {'href': path_to_full})
    path_to_ucp = rec.get('path-to-ucp')
    if path_to_ucp:
        anchor_to_ucp = my_html.anchor('UXLC change proposal', {'href': path_to_ucp})
        return [anchor_to_full, '; ', anchor_to_ucp]
    return [anchor_to_full]


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