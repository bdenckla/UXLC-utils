import my_html
import my_tanakh_book_names as tbn


def bcv_with_link_to_tdu(record):
    the_bcv_str = _bcv_str(record)
    href = _tanach_dot_us_url(record)
    return my_html.anchor(the_bcv_str, {'href': href})


def bcv_with_link_to_mwd(record):
    the_bcv_str = _bcv_str(record)
    href = _mam_with_doc_url(record)
    return my_html.anchor(the_bcv_str, {'href': href})


def uxlc_change_with_link(release_and_id):
    _release_date, change_id = release_and_id
    return my_html.anchor(change_id, {'href': _url_for_uxlc_change(release_and_id)})


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
    std_bkid = bcvp[0]
    osdf = tbn.ordered_short_dash_full(std_bkid)  # e.g. A2-Exodus
    chnu, vrnu = bcvp[1:3]  # ignoring verse numbering differences
    bcv_part = f'{osdf}.html#c{chnu}v{vrnu}'
    return f'https://bdenckla.github.io/MAM-with-doc/{bcv_part}'


def _url_for_uxlc_change(release_and_id):
    release_date, change_id = release_and_id
    # a change ID consists of
    #     a changeset date
    #     a dash
    #     a number that identifies which change within that changeset
    release_str = f'{release_date}%20-%20Changes'
    return f'https://hcanat.us/Changes/{release_str}/{release_str}.xml?{change_id}'
