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
    # Now we write varies HTML files in a bottom-up (leaves first) fashion
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    #
    dubious_recs = list(filter(_has_fem, records))
    dubious_path = 'dubious.html'
    dubious_title = 'Words with dubious early meteg on their 2nd letter'
    my_amb_early_mtg_summary.write(dubious_recs, dubious_path, dubious_title)
    #
    intro = _intro(records, dubious_recs, dubious_path, dubious_title)
    title = 'Words with early meteg on their 2nd letter'
    my_amb_early_mtg_summary.write(records, 'index.html', title, intro)


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



def _has_fem(record):
    return record.get('false early mtg')


if __name__ == "__main__":
    main()
