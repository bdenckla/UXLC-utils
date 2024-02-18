""" Exports main. """

import my_amb_early_mtg
import my_amb_early_mtg_full
import my_amb_early_mtg_summary
import my_uxlc
import my_uxlc_book_abbreviations as u_bk_abbr

def main():
    """ Writes amb-early-mtg records to HTML files. """
    records = my_amb_early_mtg.RECORDS
    #
    io_uxlc = {}
    for index, record in enumerate(records):
        record['original-order'] = index + 1
        record['bcv'] = 'gn6:7'
        record['initial-remark'] = 'dummy initial remark'
        _print_bcvp(io_uxlc, record)
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    my_amb_early_mtg_summary.write(records)


def _print_bcvp(io_uxlc, record):
    word = record['word']
    uxlc_bkid = record['uxlc_bkid']
    ch_vr_ps = _chnu_vrnu_psnu(io_uxlc, word, uxlc_bkid)
    print_out = {
        'original-order': record['original-order'],
        'word': word,
        'ch_vr_ps': ch_vr_ps
    }
    print(print_out)


def _chnu_vrnu_psnu(io_uxlc, word, uxlc_bkid):
    if uxlc_bkid not in io_uxlc:
        std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
        io_uxlc[uxlc_bkid] = my_uxlc.read(std_bkid)
    book = io_uxlc[uxlc_bkid]
    for chidx, chapter in enumerate(book):
        for vridx, verse in enumerate(chapter):
            for wdidx, cv_word in enumerate(verse):
                if cv_word == word:
                    return chidx + 1, vridx + 1, wdidx+1



if __name__ == "__main__":
    main()
