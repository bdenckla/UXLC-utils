import my_uxlc_location
import my_convert_citation_from_wlc
import my_word_diffs_420422
import my_diffs

def add(io_records):
    uxlc, pbi = my_uxlc_location.prep()
    for recidx, io_record in enumerate(io_records):
        io_record['original-order'] = recidx + 1
        io_record['bcvp'] = _bcvp_quad(io_record['bcv'], io_record['ab_word'])
        io_record['diff_type'] = _diff_type(io_record)
        pg_and_gs = _page_and_guesses(uxlc, pbi, io_record['bcvp'])
        for key, val in pg_and_gs.items():
            io_record[key] = val


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
    pair = record['ab_word'].split('\n')
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
