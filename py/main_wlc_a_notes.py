""" Exports main. """

import my_wlc_a_notes
import my_wlc_a_notes_expand
import my_wlc_a_notes_html_summary
import my_wlc_a_notes_html_full
import my_wlc_a_notes_xml


def main():
    """ Writes WLC a-notes records to HTML & XML files. """
    records_s = sorted(my_wlc_a_notes.RECORDS, key=_sort_key_for_rec)
    my_wlc_a_notes_expand.expand(records_s)
    #
    my_wlc_a_notes_html_full.write(records_s)  # fills in path-to-full fields
    my_wlc_a_notes_xml.write(records_s)  # fills in path-to-ucp fields
    my_wlc_a_notes_html_summary.write(records_s)


def _sort_key_for_rec(rec):
    ucp = rec['uxlc-change-proposal']
    if isinstance(ucp, int):
        return 1, ucp
    if isinstance(ucp, str):
        return 2, ucp
    if ucp is None:
        return 3, None
    assert False


if __name__ == "__main__":
    main()
