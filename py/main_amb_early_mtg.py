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
        paf = _page_and_flg(uxlc, pbi, _bcvp_quad(record))
        record['page'] = paf[0]
        record['fline-guess'] = paf[1]
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    my_amb_early_mtg_summary.write(records)


def _page_and_flg(uxlc, pbi, bcvp_quad):
    page, guess_fline = my_uxlc_location.estimate(uxlc, pbi, bcvp_quad)
    guess_fline_str = f'{guess_fline:.1f}'
    return page, guess_fline_str


def _bcvp_quad(record):
    uxlc_bkid = record['UXLC-bkid']
    std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
    return std_bkid, *record['ch-vr-ps']


def _bcv_str(record):
    uxlc_bkid = record['UXLC-bkid']
    chnu, vrnu, _psnu = record['ch-vr-ps']
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
