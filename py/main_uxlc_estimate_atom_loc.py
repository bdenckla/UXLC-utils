""" Exports main """

import argparse
import my_tanakh_book_names as tbn
import my_uxlc_location


def _get_cite_e_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('book_id', choices=tbn.ALL_BOOK_IDS)
    # e.g. 'Levit'
    parser.add_argument('chapter', type=int)
    parser.add_argument('verse', type=int)
    parser.add_argument('atom', type=int)
    args = parser.parse_args()
    cite_e = args.book_id, args.chapter, args.verse, args.atom
    return cite_e


def main():
    """
    Estimate the concrete location of the given atom.
    """
    cite_e = _get_cite_e_from_args()
    _main2(cite_e)


def example_run():
    """ Do an example run of the program, for main_0_mega.py. """
    cite_e = tbn.BK_GENESIS, 27, 7, 3
    _main2(cite_e)


def _main2(cite_e):
    uxlc, pbi = my_uxlc_location.prep()
    guess_page, guess_fline = my_uxlc_location.estimate(uxlc, pbi, cite_e)
    guess_fline_str = f'{guess_fline:.1f}'
    print(guess_page, guess_fline_str)


if __name__ == "__main__":
    main()
