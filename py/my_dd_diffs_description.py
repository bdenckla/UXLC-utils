""" Exports get1 """
import my_unicode
import my_diffs
import my_dd_simplify_simple_diffs as ssd
import my_dd_lett_words


def get1(str1, str2):
    """
    If possible, get a human-friendly description of the diffs
    between str1 & str2.
    Returns a pair with the following contents:
    Element 1 of the pair is a string describing the diff in detail.
    Element 2 of the pair is a string describing the category, i.e. the kind of diff.
    """
    qc1 = ssd.qualify_code_points(str1)
    qc2 = ssd.qualify_code_points(str2)
    diffs = my_diffs.get(qc1, qc2)
    named_diffs = tuple(map(_get_unicode_names_for_diff, diffs))
    if _letters_differ(str1, str2):
        return _get_dide_incl_letter_changes(str1, str2, named_diffs)
    return ssd.simplify_simple_diffs(named_diffs)


def _letters_differ(str1, str2):
    lm1 = my_dd_lett_words.letters_and_maqafs(str1)
    lm2 = my_dd_lett_words.letters_and_maqafs(str2)
    return lm1 != lm2


def _get_dide_incl_letter_changes(_str1, _str2, named_diffs):
    return str(named_diffs), 'deep diff'


def _get_unicode_names_for_diff(diff):
    assert len(diff) == 2  # an "A" side and a "B" side
    return tuple(map(_get_unicode_names_for_side, diff))


def _get_unicode_names_for_side(side):
    return side and tuple(map(_get_unicode_names_for_side_el, side))


def _get_unicode_names_for_side_el(side):
    letter = ssd.qcp_get(side, 'letter')
    return ssd.qcp_make(
        my_unicode.name(ssd.qcp_get(side, 'code_point')),
        letter and my_unicode.name(letter),
        ssd.qcp_get(side, 'count')
    )
