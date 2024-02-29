import my_html
import my_tanakh_book_names as tbn
import my_hebrew_points as hpo
import my_hebrew_punctuation as hpu
import my_hebrew_accents as ha

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
    std_bkid = bcvp[0]
    osdf = tbn.ordered_short_dash_full(std_bkid)  # e.g. A2-Exodus
    chnu, vrnu = bcvp[1:3]  # ignoring verse numbering differences
    bcv_part = f'{osdf}.html#c{chnu}v{vrnu}'
    return f'https://bdenckla.github.io/MAM-with-doc/{bcv_part}'


def diff_type_span_with_title(record):
    diff_type = record['diff-type']
    return my_html.span(diff_type, {'title': diff_type_long(record)})


def diff_type_long(record):
    diff_type = record['diff-type']
    return _DIFF_TYPES[diff_type]


def diff_type_abbreviation_table():
    rows = list(map(_diff_type_abbreviation_row, _DIFF_TYPES.items()))
    return my_html.table(rows)


def _diff_type_abbreviation_row(ad_pair):
    abbrev, definition = ad_pair 
    datum_for_abbrev = my_html.table_datum(abbrev)
    datum_for_defn = my_html.table_datum(definition)
    return my_html.table_row([datum_for_abbrev, datum_for_defn])


def _example(english, mark1, mark2):
    return f'{english}: א{mark1} to א{mark2}'


def _remove_sheva():
    mark = hpo.SHEVA



def _example_quad(english, mq1, mq2):
    x_to_y = f'א{mq1[0]}א{mq1[1]}א{mq1[2]}א{mq1[3]} to א{mq2[0]}א{mq2[1]}א{mq2[2]}א{mq2[3]}'
    return f'{english}: {x_to_y}'


MQ1 = hpo.SHEVA, hpo.XPATAX, hpo.XQAMATS, hpo.XSEGOL
MQ2 = '', hpo.PATAX, hpo.QAMATS, hpo.SEGOL_V
_DMS_EXAMPLE_1 = 'וּלְרׇחְבָּ֑הּ'
_DMS_EXAMPLE_2 = 'וּלְרׇחְבָּ֑הּ'.replace(hpo.DAGESH_OM, '')
_DMS = 'dagesh, mapiq, or shuruq dot'
_DIFF_TYPES = {
    '-dms': f'remove {_DMS}: {_DMS_EXAMPLE_1} to {_DMS_EXAMPLE_2}',
    '+dms': f'add {_DMS}: {_DMS_EXAMPLE_2} to {_DMS_EXAMPLE_1}',
    '-rfh': _example('remove rafeh', hpo.RAFE, ''),
    '-pashta': _example('remove pashta accent', ha.PASH, ''),
    '+rev': _example('add revia accent', '', ha.REV),
    '+psq': _example('add paseq', '', hpu.PAS),
    '+mqf': _example('add maqaf', '', hpu.MAQ),
    '-shoḥ': _example_quad('remove sheva or change ḥataf vowel to plain vowel', MQ1, MQ2),
    '+shoḥ': _example_quad('add sheva or change ḥataf vowel to plain vowel', MQ2, MQ1),
    'vow-chng': 'vowel change',
    'acc-chng': 'accent change',
    'misc': 'miscellaneous'
}
