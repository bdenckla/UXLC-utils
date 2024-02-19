def bcv_str(record):
    bcvp = record['bcvp']
    uxlc_bkid = bcvp[0]
    chnu, vrnu = bcvp[1:3]
    return f'{uxlc_bkid}{chnu}:{vrnu}'


def tanach_dot_us_url(record):
    bcv_str = bcv_str(record)
    return f'https://tanach.us/Tanach.xml?{bcv_str}'
