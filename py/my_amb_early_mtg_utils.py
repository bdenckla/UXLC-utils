import my_html
import my_uxlc_book_abbreviations as u_bk_abbr
import my_tanakh_book_names as tbn

def bcv_with_link_to_tdu(record):
    the_bcv_str = _bcv_str(record)
    href = _tanach_dot_us_url(record)
    return my_html.anchor(the_bcv_str, {'href': href})


def bcv_with_link_to_mwd(record):
    the_bcv_str = _bcv_str(record)
    href = _mam_with_doc_url(record)
    return my_html.anchor(the_bcv_str, {'href': href})


def _bcv_str(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    chnu, vrnu = bcvp[1:3]
    return f'{uxlc_bkid}{chnu}:{vrnu}'


def _tanach_dot_us_url(record):
    the_bcv_str = _bcv_str(record)
    return f'https://tanach.us/Tanach.xml?{the_bcv_str}'


def _mam_with_doc_url(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
    osdf = tbn.ordered_short_dash_full(std_bkid)  # e.g. A2-Exodus
    chnu, vrnu = bcvp[1:3]  # ignoring verse numbering differences
    bcv_part = f'{osdf}.html#c{chnu}v{vrnu}'
    return f'https://bdenckla.github.io/MAM-with-doc/{bcv_part}'
