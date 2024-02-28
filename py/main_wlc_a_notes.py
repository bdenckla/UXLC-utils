""" Exports main. """

import my_wlc_a_notes
import my_wlc_a_notes_expand
import my_wlc_a_notes_summary
import my_wlc_a_notes_full
import my_wlc_a_notes_xml


def main():
    """ Writes WLC a-notes records to HTML & XML files. """
    records = sorted(my_wlc_a_notes.RECORDS, key=_sort_key_for_rec)
    my_wlc_a_notes_expand.expand(records)
    _set_prev_and_next(records, 'prev', 'next')
    #
    my_wlc_a_notes_full.write(records)  # fills in path-to-full fields
    xml_out_path = my_wlc_a_notes_xml.write(records)  # fills in path-to-ucp fields
    my_wlc_a_notes_summary.write(records, xml_out_path)
    my_wlc_a_notes_summary.write(records, xml_out_path, no_ucp=True)


def _sort_key_for_rec(record):
    ucp = record['uxlc-change-proposal']
    if isinstance(ucp, int):
        return 1, ucp
    if isinstance(ucp, str):
        return 2, ucp
    if ucp is None:
        return 3, None
    assert False


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


if __name__ == "__main__":
    main()
