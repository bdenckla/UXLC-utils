import py.my_html as my_html
import py.my_tanakh_book_names as tbn
import py.my_uxlc_book_abbreviations as u_bk_abbr


def bcv_with_link_to_tdu(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    href = _tanach_dot_us_url(record)
    return my_html.anchor(uxlc_bcv_str, {"href": href})


def bcv_with_link_to_mwd(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    href = _mam_with_doc_url(record)
    return my_html.anchor(uxlc_bcv_str, {"href": href})


def uxlc_change_with_link(release_and_id):
    _release_date, change_id = release_and_id
    return my_html.anchor(change_id, {"href": _url_for_uxlc_change(release_and_id)})


def _uxlc_bcv_str(record):
    std_bcv_triple = record["std-bcv-triple"]
    std_bkid = std_bcv_triple[0]
    uxlc_bkid = u_bk_abbr.BKNA_MAP_STD_TO_UXLC[std_bkid]
    chnu, vrnu = std_bcv_triple[1], std_bcv_triple[2]
    return f"{uxlc_bkid}{chnu}:{vrnu}"


def _tanach_dot_us_url(record):
    uxlc_bcv_str = _uxlc_bcv_str(record)
    return f"https://tanach.us/Tanach.xml?{uxlc_bcv_str}"


def _mam_with_doc_url(record):
    std_bcv_triple = record["std-bcv-triple"]
    std_bkid = std_bcv_triple[0]
    osdf = tbn.ordered_short_dash_full(std_bkid)  # e.g. A2-Exodus
    chnu, vrnu = std_bcv_triple[1], std_bcv_triple[2]
    # Above, we're ignoring verse numbering differences
    bcv_part = f"{osdf}.html#c{chnu}v{vrnu}"
    return f"https://bdenckla.github.io/MAM-with-doc/{bcv_part}"


def _url_for_uxlc_change(release_and_id):
    release_date, change_id = release_and_id
    # a change ID consists of
    #     a changeset date
    #     a dash
    #     a number that identifies which change within that changeset
    release_str = f"{release_date}%20-%20Changes"
    return f"https://hcanat.us/Changes/{release_str}/{release_str}.xml?{change_id}"
