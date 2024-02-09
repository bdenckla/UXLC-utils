""" Exports check. """

import re
import my_uxlc_book_abbreviations as u_bk_abbr
import my_uxlc_location


def check(uxlc, page_break_info, changes):
    """ Check the LC locations in changes against page break info. """
    pbi = page_break_info
    check_results = tuple(_check_loc(uxlc, pbi, c) for c in changes)
    check_results_f = tuple(map(_flatten_check_result, check_results))
    return check_results_f


def _flatten_check_result(check_result):
    change, flines = check_result
    pgid, column, line = _pgcoli(change)
    flat = {
        'change_release': change['release'],
        'change_cite': change['citation'],
        'change_page': pgid,
        'change_column': _tweak_change_col(pgid, column),
        'change_line': line,
        #
        **flines
    }
    return flat


def _pgcoli(change):
    change_lc_loc = change['lc_gen'] or change['lc']
    pgcoli = expand_lc_loc_to_pgcoli(change_lc_loc)
    return pgcoli


def _tweak_change_col(pgid, column):
    if pgid in ('182A', '182B'):  # On or about 2Sam 22
        # I don't agree with Chris regarding the notion that
        # there are two columns on these pages
        return 1
    return column


def _check_loc(uxlc, pbi, change):
    cite_e = _expand_citation(change['citation'])
    change_fline = _change_fline(change)
    guess_page, guess_fline = my_uxlc_location.estimate(uxlc, pbi, cite_e)
    change_page = _pgcoli(change)[0]
    assert change_page == guess_page
    fline_diff = guess_fline - change_fline
    flines = {
        'change_fline': change_fline,
        'guess_fline': round(guess_fline, 2),
        'fline_diff': round(fline_diff, 2),
    }
    check_result = change, flines
    return check_result


def _change_fline(change):
    pgid, column, line = _pgcoli(change)
    tweaked_col = _tweak_change_col(pgid, column)
    pre_columns = tweaked_col - 1
    return 27 * pre_columns + line


def _expand_lc_loc_to_leabcoli(lc_loc):
    # leabcoli: leaf, ca_or_cb, column, line
    # ca_or_cb: capital A or capital B
    patt = r'Folio_(\d\d\d)([AB]) (\d):(\d\d?)(-.+)?'
    match = re.fullmatch(patt, lc_loc)
    leafnu_str, ca_or_cb, colnu_str, linenu_str, _endpoint = match.groups(0)
    return int(leafnu_str), ca_or_cb, int(colnu_str), int(linenu_str)


def expand_lc_loc_to_pgcoli(lc_loc):
    """ Expand LC location string to a triple of pgid, column, & line. """
    # pgcoli: pgid, column, line
    # ca_or_cb: capital A or capital B
    leaf_int, ca_or_cb, col_int, line_int = _expand_lc_loc_to_leabcoli(lc_loc)
    pgid = f'{leaf_int:03d}{ca_or_cb}'
    return pgid, col_int, line_int


def _expand_citation(citation: str):
    patt = r'([A-z0-9]+) (\d+):(\d+).(\d+)'
    match = re.fullmatch(patt, citation)
    assert match
    book_ua, chnu_s, vrnu_s, wdnu_s = match.groups(0)
    # ua: UXLC abbreviation (for book)
    assert isinstance(book_ua, str)
    bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[book_ua]
    return bkid, int(chnu_s), int(vrnu_s), int(wdnu_s)
