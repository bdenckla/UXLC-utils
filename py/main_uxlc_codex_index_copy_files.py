""" Exports main """

import shutil
import os


def _trees(files):
    return tuple(set(map(os.path.dirname, files)))


def main():
    """
    Copy files to the codex-index repo.
    """
    trees_to_copy = (
        'in/UXLC',
    )
    files_to_copy = (
        'in/UXLC-misc/lci_recs.json',
        'out/UXLC-misc/lci_recs.xml',
        'py/main_uxlc_estimate_atom_loc.py',
        'py/my_sef_cmn.py',
        'py/my_tanakh_book_names.py',
        'py/my_uxlc.py',
        'py/my_uxlc_bibdist.py',
        'py/my_uxlc_cvp.py',
        'py/my_uxlc_location.py',
        'py/my_uxlc_lci_augrec.py',
        'py/my_uxlc_lci_rec.py',
        'py/my_uxlc_lci_rec_flatten.py',
        'py/my_uxlc_page_break_info.py',
    )
    codex_index = '../codex-index'
    trees_to_rmtree = trees_to_copy + _trees(files_to_copy)
    for tree in trees_to_rmtree:
        dst = f'{codex_index}/{tree}'
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(dst)
    for tree in trees_to_copy:
        dst = f'{codex_index}/{tree}'
        shutil.copytree(tree, dst, dirs_exist_ok=True)
    for file in files_to_copy:
        dst = f'{codex_index}/{file}'
        shutil.copy(file, dst)


if __name__ == "__main__":
    main()
