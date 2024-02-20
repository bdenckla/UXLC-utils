""" Exports main. """

import my_amb_early_mtg
import my_amb_early_mtg_full
import my_amb_early_mtg_summary
import my_amb_early_mtg_extend
import my_html

def main():
    """ Writes amb-early-mtg records to HTML files. """
    records = my_amb_early_mtg.RECORDS
    #
    my_amb_early_mtg_extend.extend_records(records)  # mutates, i.e. modifies in-place
    #
    _set_prev_and_next(records, 'prev', 'next')
    #
    dubious_recs = list(filter(_has_deml2, records))
    #
    _set_prev_and_next(dubious_recs, 'prev-dubious', 'next-dubious')
    #
    # Now we write varies HTML files in a bottom-up (leaves first) fashion
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    #
    dubious_path = 'dubious.html'
    dubious_title = 'Words with dubious early meteg on their 2nd letter'
    my_amb_early_mtg_summary.write(dubious_recs, dubious_path, dubious_title)
    #
    intro = _intro(records, dubious_recs, dubious_path, dubious_title)
    title = 'Words with early meteg on their 2nd letter'
    my_amb_early_mtg_summary.write(records, 'index.html', title, intro)


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


def _intro(records, dubious_recs, dubious_path, dubious_title):
    anch_attr = {'href': dubious_path}
    nrecs = len(records)
    ndrecs = len(dubious_recs)
    para1_contents = f'This page lists all {nrecs} words in UXLC that have an early meteg on their 2nd letter.'
    anch_contents = f'a version of that list filtered down to the {ndrecs} cases that seem dubious'
    para2_contents = ['Here is ', my_html.anchor(anch_contents, anch_attr), '.']
    return [
        my_html.para(para1_contents),
        my_html.para(para2_contents),
    ]



def _has_deml2(record):
    return record.get('dubious early mtg on letter 2')


if __name__ == "__main__":
    main()
