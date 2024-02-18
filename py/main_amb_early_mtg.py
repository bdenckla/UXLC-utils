""" Exports main. """

import my_amb_early_mtg
import my_amb_early_mtg_full
import my_amb_early_mtg_summary


def main():
    """ Writes amb-early-mtg records to HTML files. """
    records = my_amb_early_mtg.RECORDS
    #
    for index, record in enumerate(records):
        record['original-order'] = index + 1
        record['bcv'] = 'gn6:7'
        record['initial-remark'] = 'dummy initial remark'
    #
    my_amb_early_mtg_full.write(records)  # fills in path-to-full fields
    my_amb_early_mtg_summary.write(records)


if __name__ == "__main__":
    main()
