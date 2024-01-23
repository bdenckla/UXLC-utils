""" Exports analyze_dalsam. """

import re

import my_hebrew_points as hpo
import my_hebrew_accents as ha
import my_hebrew_punctuation as hpu
import my_utils


def analyze_dalsam(dalsam):
    """
    Analyze dalet and samekh.
    Return a dict like this: {
        'undisputed-prefix': tuple,
        'disputed-part': (dalsep, samsep, stress_mark),
        'undisputed-suffix': tuple
    }
    where:
    The dalsep part is dalet separated by its qqs.
    The samsep part is samekh separated at the same indices as dalsep.
    The stress_mark part is the stress mark, if any, on the disputed qq.
    """
    dalet, samekh = dalsam
    out = {
        'undisputed-prefix': tuple(),
        'undisputed-suffix': tuple()
    }
    if dalet.count(hpo.QAMATS_Q) == 1:
        out['disputed-part'] = _analyze_disputed_part(dalet, samekh)
        return out
    dalatoms = _atoms_with_trailing_maqaf(dalet)
    samatoms = _atoms_with_trailing_maqaf(samekh)
    found = False
    for dalatom, samatom in my_utils.szip(dalatoms, samatoms):
        if dalatom != samatom:
            assert not found
            found = True
            out['disputed-part'] = _analyze_disputed_part(dalatom, samatom)
            continue
        key = 'undisputed-suffix' if found else 'undisputed-prefix'
        # Below, we could just as well have used samatom instead of dalatom
        # since at this point in the code, they are equal.
        out[key] += (dalatom,)
    return out


def _full_partition_by_qq(string):
    """
    Separate string into its parts between qqs.
    E.g.:
        Return ('a',)          for a string 'a'.
        Return ('a', 'b')      for a string 'a' + qq + 'b'.
        Return ('a', 'b', 'c') for a string 'a' + qq + 'b' + qq + 'c'.
    """
    pre, qamqat, post = string.partition(hpo.QAMATS_Q)
    if qamqat:
        out = pre, qamqat, *_full_partition_by_qq(post)
        assert ''.join(out) == string
        return out
    return (pre,)


def _atoms_with_trailing_maqaf(string):
    """
    Separate string into its atoms,
    where nonfinal atoms have trailing maqaf marks.
    """
    pre, maq, post = string.partition(hpu.MAQ)
    if maq:
        out = pre + maq, *_atoms_with_trailing_maqaf(post)
        assert ''.join(out) == string
        return out
    return (pre,)


def _analyze_disputed_part(dalet, samekh):
    """ Separate dalet by its qqs, and separate samekh similarly. """
    dalsep = _full_partition_by_qq(dalet)
    assert len(dalsep) in (3, 5)
    samsep = _similarly_separate(dalsep, samekh)
    assert dalsep[0] == samsep[0]
    assert dalsep[1] == hpo.QAMATS_Q and samsep[1] == hpo.QAMATS
    assert dalsep[2:] == samsep[2:]
    cp_a_dqq = dalsep[2][0]  # code point after disputed qamats qatan
    is_a_letter = re.fullmatch('[א-ת]', cp_a_dqq)
    if not is_a_letter:
        assert cp_a_dqq in {ha.GER_M, hpo.METEG, ha.MER, ha.MUN}
        stress_mark = cp_a_dqq
        return dalsep, samsep, stress_mark
    # See note on postpositive below
    letter_is_final = re.fullmatch('[א-ת][^א-ת]*$', ''.join(dalsep[2:]))
    assert not letter_is_final
    stress_mark = None
    return dalsep, samsep, stress_mark


# Note on postpositive
######################
# At this point, we know that the code point after the disputed qamats
# qatan (dqq) is a letter, not a stress mark. But, the syllable
# with the dqq might still be stressed, if:
#
#    This letter closes that syllable.
#    This letter is atom-final.
#    This letter has a postpositive accent.
#    That accent indicates stress, i.e. this atom has no stress helper.
#
# In the code above, we are able to rule out this situation merely using
# the atom-final requirement.  I.e., it just so happens that a letter after
# an unstressed dqq is never final.


def _similarly_separate(dalsep, samekh):
    lengths = map(len, dalsep)
    samsep = tuple()
    start = 0
    for length in lengths:
        stop = start + length
        samsep = (*samsep, samekh[start:stop])
        start = stop
    return samsep
