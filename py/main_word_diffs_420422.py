""" Exports main. """

import my_word_diffs_420422
import my_word_diffs_420422_add_fields
import my_word_diffs_420422_full
import my_word_diffs_420422_summary
import my_html

def main():
    """ Writes 420-to-422 word diff survey to HTML files. """
    records = my_word_diffs_420422.RECORDS
    #
    my_word_diffs_420422_add_fields.add(records)  # mutates, i.e. modifies in-place
    #
    records = sorted(records, key=_sort_key_for_rec)
    #
    _set_prev_and_next(records, 'prev', 'next')
    #
    # Now we write various HTML files in a bottom-up (leaves first) fashion
    #
    my_word_diffs_420422_full.write(records)  # fills in path-to-full fields
    #
    #
    intro = _intro(records)
    title = 'WLC 4.22 Changes'
    my_word_diffs_420422_summary.write(records, 'index.html', title, intro)


def _sort_key_for_rec(record):
    dity = record['diff_type']
    return (1, 'misc') if dity == 'misc' else (0, dity)



def _set_prev_and_next(io_records, prevkey, nextkey):
    prev_record = None
    for io_record in io_records:
        if prev_record:
            io_record[prevkey] = prev_record
        prev_record = io_record
    next_record = None
    for io_record in reversed(io_records):
        if next_record:
            io_record[nextkey] = next_record
        next_record = io_record


def _intro(records):
    nrecs = len(records)
    para1_contents = f'This page lists the {nrecs} words that differ between WLC 4.20 and 4.22.'
    return [
        my_html.para(para1_contents),
    ]



if __name__ == "__main__":
    main()
