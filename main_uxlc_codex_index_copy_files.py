"""Exports main"""

import shutil
import os
import py.my_open as my_open


def _trees(files):
    return tuple(set(map(os.path.dirname, files)))


def main():
    """
    Copy files to the codex-index repo.
    """
    if os.path.exists(_CI_L):
        shutil.rmtree(_CI_L)
        print(f"did shutil.rmtree of {_CI_L}")
    trees_to_mkdir = _TREES_TO_COPY + _trees(_FILES_TO_COPY)
    for tree in trees_to_mkdir:
        fulltree = f"{_CI_L}/{tree}"
        if tree == ".":
            print(f"not did os.makedirs of {fulltree}")
            continue
        os.makedirs(fulltree)
        print(f"yes did os.makedirs of {fulltree}")
    for tree in _TREES_TO_COPY:
        dst = f"{_CI_L}/{tree}"
        shutil.copytree(tree, dst, dirs_exist_ok=True)
        print(f"to {_CI_L}, did shutil.copytree of {tree}")
    for file in _FILES_TO_COPY:
        dst = f"{_CI_L}/{file}"
        shutil.copy(file, dst)
        print(f"to {_CI_L}, did shutil.copy of {file}")
    wpath = f"{_CI_L}/warning-do-not-edit-these-files.txt"
    my_open.with_tmp_openw(wpath, {}, _wcallback)
    print(f"wrote {wpath}")


def _wcallback(out_fp):
    out_fp.write("\n".join(_WARNING_LINES) + "\n")


_WARNING_LINES = [
    "Do not edit these files here in the codex-index public repo.",
    "These files are copied from the UXLC-utils private repo.",
    "If needed, edit them their in the UXLC-utils private repo.",
]
_TREES_TO_COPY = ("in/UXLC",)
_FILES_TO_COPY = (
    "in/UXLC-misc/lci_recs.json",
    "out/UXLC-misc/lci_recs.xml",
    "out/UXLC-misc/lci_augrecs.json",
    "./main_uxlc_estimate_atom_loc.py",
    "py/my_tanakh_book_names.py",
    "py/my_uxlc.py",
    "py/my_uxlc_bibdist.py",
    "py/my_uxlc_cvp.py",
    "py/my_uxlc_location.py",
    "py/my_uxlc_lci_augrec.py",
    "py/my_uxlc_lci_rec.py",
    "py/my_uxlc_lci_rec_flatten.py",
    "py/my_uxlc_page_break_info.py",
)
_CI_L = "../codex-index/leningrad"


if __name__ == "__main__":
    main()
