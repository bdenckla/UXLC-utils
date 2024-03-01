""" Exports find. """

import re
import my_tanakh_book_names as tbn
import my_uxlc
import my_hebrew_points as hpo
import my_str_defs as sd
import my_uxlc_book_abbreviations as u_bk_abbr


def find():
    last_recnum = 66
    for std_bkid in tbn.ALL_BOOK_IDS:
        for chidx, chapter in enumerate(my_uxlc.read(std_bkid)):
            for vridx, verse in enumerate(chapter):
                for atidx, atom in enumerate(verse):
                    if _has_early_mtg(atom):
                        last_recnum += 1
                        uxlc_bkid = u_bk_abbr.BKNA_MAP_STD_TO_UXLC[std_bkid]
                        bcvp = uxlc_bkid, chidx+1, vridx+1, atidx+1
                        recass = _record_assignment(atom, last_recnum, bcvp)
                        print(recass)


_LETT_NLETT_STAR = r'[א-ת][^א-ת]*'
_LETT_NLETT_PLUS = r'[א-ת][^א-ת]+'
_NOT_XIRIQ = f'[^{hpo.XIRIQ}]'

def _has_early_mtg(atom):
    patt = (
        _LETT_NLETT_STAR +
        _LETT_NLETT_PLUS +
        _LETT_NLETT_STAR +
        hpo.METEG + sd.CGJ + _NOT_XIRIQ
    )
    return re.match(patt, atom)

def _record_assignment(atom, recnum, bcvp):
    uxlc_bkid, chnu, vrnu, atnu = bcvp
    recval = {
        'word': atom,
        'uxlc_bcvp': (uxlc_bkid, chnu, vrnu, atnu),
        'img': f'{uxlc_bkid}{chnu}v{vrnu}.png',
    }
    recname = f'_RECORD_{recnum:02}'
    return f'{recname} = {recval}'
