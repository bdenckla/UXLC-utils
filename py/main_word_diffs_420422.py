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
    _set_prev_and_next(records, 'prev', 'next')
    #
    # Now we write various HTML files in a bottom-up (leaves first) fashion
    #
    my_word_diffs_420422_full.write(records)  # fills in path-to-full fields
    #
    #
    intro = _intro(records)
    title = 'Words that differ btwn WLC 4.20 and 4.22'
    my_word_diffs_420422_summary.write(records, 'index.html', title, intro)


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
    para1_contents = f'This page lists differences between WLC 4.20 and 4.22.'
    return [
        my_html.para(para1_contents),
    ]



if __name__ == "__main__":
    main()
