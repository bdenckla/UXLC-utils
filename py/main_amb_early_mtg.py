""" Exports main. """

import my_amb_early_mtg
import my_amb_early_mtg_full
import my_amb_early_mtg_summary
import my_amb_early_mtg_extend

def main():
    """ Writes amb-early-mtg records to HTML files. """
    records = my_amb_early_mtg.RECORDS
    #
    my_amb_early_mtg_extend.extend_records(records)  # mutates, i.e. modifies in-place
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    my_amb_early_mtg_summary.write(records)


if __name__ == "__main__":
    main()
