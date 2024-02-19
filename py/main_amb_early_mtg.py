""" Exports main. """

import my_amb_early_mtg
import my_amb_early_mtg_full
import my_amb_early_mtg_summary
import my_uxlc_location
# import my_uxlc
import my_uxlc_book_abbreviations as u_bk_abbr

def main():
    """ Writes amb-early-mtg records to HTML files. """
    records = my_amb_early_mtg.RECORDS
    # io_uxlc = {}
    uxlc, pbi = my_uxlc_location.prep()
    for recidx, record in enumerate(records):
        # _print_bcvp(io_uxlc, recidx, record)
        record['original-order'] = recidx + 1
        record['initial-remark'] = 'dummy initial remark'
        record['bcv-str'] = _bcv_str(record)
        record['tanach-dot-us-url'] = _tanach_dot_us_url(record)
        pg_and_gs = _page_and_guesses(uxlc, pbi, _bcvp_quad(record))
        for key, val in pg_and_gs.items():
            record[key] = pg_and_gs[key]
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    my_amb_early_mtg_summary.write(records)


def _page_and_guesses(uxlc, pbi, bcvp_quad):
    page, fline_guess = my_uxlc_location.estimate(uxlc, pbi, bcvp_quad)
    if fline_guess > 54:
        line_guess = fline_guess - 54
        col_guess = 3
    elif fline_guess > 27:
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


def _bcvp_quad(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
    return std_bkid, *bcvp[1:]


def _bcv_str(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    chnu, vrnu = bcvp[1:3]
    return f'{uxlc_bkid}{chnu}:{vrnu}'


def _tanach_dot_us_url(record):
    bcv_str = _bcv_str(record)
    return f'https://tanach.us/Tanach.xml?{bcv_str}'


# def _print_bcvp(io_uxlc, recidx, record):
#     word = record['word']
#     uxlc_bkid = record['UXLC-bkid']
#     ch_vr_ps = _chnu_vrnu_psnu(io_uxlc, word, uxlc_bkid)
#     new_record = dict(record)
#     new_record['ch-vr-ps'] = ch_vr_ps
#     num = 1 + recidx
#     assignment = f'_RECORD_{num:02} = {new_record}'
#     print(assignment)


# def _chnu_vrnu_psnu(io_uxlc, word, uxlc_bkid):
#     if uxlc_bkid not in io_uxlc:
#         std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
#         io_uxlc[uxlc_bkid] = my_uxlc.read(std_bkid)
#     book = io_uxlc[uxlc_bkid]
#     for chidx, chapter in enumerate(book):
#         for vridx, verse in enumerate(chapter):
#             for wdidx, cv_word in enumerate(verse):
#                 if cv_word == word:
#                     return chidx + 1, vridx + 1, wdidx+1



if __name__ == "__main__":
    main()
