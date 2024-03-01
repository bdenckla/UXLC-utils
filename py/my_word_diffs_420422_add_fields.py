""" Exports add. """

import json
import my_uxlc_location
import my_convert_citation_from_wlc
import my_word_diffs_420422
import my_diffs
import my_dd_diffs_description as diffs_desc
import my_word_diffs_420422_utils as wd_utils
import my_utils

def add(io_records):
    uxlc, pbi = my_uxlc_location.prep()
    all_ucps = _read_in_all_ucps()
    for recidx, io_record in enumerate(io_records):
        _add1(uxlc, pbi, all_ucps, recidx, io_record)


def _add1(uxlc, pbi, all_ucps, recidx, io_record):
    io_record['original-order'] = recidx + 1
    io_record['bcvp'] = _bcvp_quad(io_record['bcv'], io_record['ab-word'])
    io_record['diff-type'] = _diff_type(io_record)
    io_record['diff-desc'] = _diff_detail(io_record)
    io_record['descs-for-ucps'] = _descs_for_ucps(all_ucps, io_record)
    _add_page_and_guesses(io_record, uxlc, pbi)


def _descs_for_ucps(all_ucps, record):
    ucps_for_this_record = wd_utils.uxlc_change_proposals(record)
    return my_utils.sl_map((_desc_from_ucp, all_ucps), ucps_for_this_record)


def _desc_from_ucp(all_ucps, release_and_id):
    if raw_ucp := all_ucps.get(release_and_id):
        return raw_ucp['description']
    return None


def _add_page_and_guesses(io_record, uxlc, pbi):
    pg_and_gs = _page_and_guesses(uxlc, pbi, io_record['bcvp'])
    for key, val in pg_and_gs.items():
        io_record[key] = val


def _diff_detail(record):
    diff_detail, _category = diffs_desc.get1(*_ab_uwords_pair(record))
    return diff_detail


def _read_in_all_ucps():
    """ Read in lci_recs.json, raw """
    path = 'out/UXLC-misc/all_changes.json'
    with open(path, encoding='utf-8') as in_fp:
        raw_ucps = json.load(in_fp)
    return {_release_and_id(raw_ucp): raw_ucp for raw_ucp in raw_ucps}


def _release_and_id(raw_ucp):
    release_date = raw_ucp['release']
    changeset_date = raw_ucp['changeset']
    number_within_changest = raw_ucp['n']
    change_id = changeset_date + '-' + str(number_within_changest)
    return release_date, change_id


def _ab_uwords_pair(record):
    return record['ab-uword'].split('\n')


_CUSTOM = {
    (('.', None),): '-dms',
    ((None, '.'),): '+dms',
    ((',', None),): '-rfh',
    (('03', None),): '-pashta',
    ((None, '81'),): '+rev',
    ((None, '05'),): '+psq',
    ((None, '-'),): '+mqf',
    ((':', None),): '-shoḥ',
    ((None, ':'),): '+shoḥ',
    (('A', 'E'),): 'vow-chng',
    (('F', 'A'),): 'vow-chng',
    (('I', ':'),): 'vow-chng',
    (('0', '1'),): 'acc-chng',
    (('1', '0'),): 'acc-chng',
    (('1', '3'),): 'acc-chng',
    (('3', '1'),): 'acc-chng',
    (('3', '6'),): 'acc-chng',
    (('7', '9'),): 'acc-chng',
    (('63', '81'),): 'acc-chng',
    (('92', '70'),): 'acc-chng',
}


def _diff_type(record):
    pair = record['ab-word'].split('\n')
    generic_diffs = my_diffs.get(*pair)
    if custom := _CUSTOM.get(tuple(generic_diffs)):
        return custom
    return 'misc'


def _page_and_guesses(uxlc, pbi, bcvp_quad):
    page, fline_guess = my_uxlc_location.estimate(uxlc, pbi, bcvp_quad)
    if fline_guess > 55:
        line_guess = fline_guess - 54
        col_guess = 3
    elif fline_guess >= 28:
        line_guess = fline_guess - 27
        col_guess = 2
    else:
        line_guess = fline_guess
        col_guess = 1
    line_guess_str = f'{line_guess:.1f}'
    fline_guess_str = f'{fline_guess:.1f}'
    return {
        'page': page,
        'fline-guess': fline_guess_str,
        'line-guess': line_guess_str,
        'column-guess': col_guess
    }


def _bcvp_quad(wlc_bcv_str, ab_word):
    std_bcv_triple = my_convert_citation_from_wlc.get_std_bcv_triple(wlc_bcv_str)
    a_word, _b_word = ab_word.split('\n')
    poskey = wlc_bcv_str + '!' + a_word
    pos = my_word_diffs_420422.WORD_POSITIONS[poskey]
    return *std_bcv_triple, pos
