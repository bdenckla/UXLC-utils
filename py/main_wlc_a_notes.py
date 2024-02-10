""" Exports main. """

import my_wlc_a_notes
import my_wlc_a_notes_html
import my_wlc_a_notes_xml


def main():
    """ Writes WLC a-notes records to HTML & XML files. """
    my_wlc_a_notes_html.write(my_wlc_a_notes.RECORDS)
    my_wlc_a_notes_xml.write(my_wlc_a_notes.RECORDS)


if __name__ == "__main__":
    main()
