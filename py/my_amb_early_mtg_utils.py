import my_html

def bcv_with_link_to_tdu(record):
    the_bcv_str = _bcv_str(record)
    href = _tanach_dot_us_url(record)
    return my_html.anchor(the_bcv_str, {'href': href})


def _bcv_str(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    chnu, vrnu = bcvp[1:3]
    return f'{uxlc_bkid}{chnu}:{vrnu}'


def _tanach_dot_us_url(record):
    the_bcv_str = _bcv_str(record)
    return f'https://tanach.us/Tanach.xml?{the_bcv_str}'
