""" Exports various utilities. """
import os


def init(dic, key, val):
    """ If key is fresh in dic, set its value to val. Other assert. """
    assert key not in dic
    dic[key] = val


def maybe_init(dic, key, val):
    """ If key is fresh in dic, set its value to val. Otherwise whiff. """
    if key not in dic:
        dic[key] = val


def first_and_only(seq):
    """ Assert that this is there is only 1 el of seq, and returns it. """
    assert len(seq) == 1
    return seq[0]


def first_and_only_and_str(seq):
    """ Like first_and_only, but also asserts that result is a string. """
    fao = first_and_only(seq)
    assert isinstance(fao, str)
    return fao


def szip(*seqs):
    """ Strongly zip (zip, asserting equal length) """
    for seq in seqs[1:]:
        assert _len_for_szip(seq) == _len_for_szip(seqs[0])
    return zip(*seqs)


def l_szip(*seqs):
    """ Force output of szip to be a list. """
    return list(szip(*seqs))


def intersperse(sep, seq):
    """ Intersperse a separator between the elements of a sequence. """
    accum = []
    for elem in seq:
        if accum:
            accum.append(sep)
        accum.append(elem)
    type_of_seq = type(seq)  # e.g. list or tuple
    return type_of_seq(accum)


def ll_map(fun, the_list):
    """
    Map the given function over the given list.
    (The "ll" means "list in, list out".)
    """
    assert isinstance(the_list, list)
    return sl_map(fun, the_list)


def tt_map(fun, the_tuple):
    """
    Map the given function over the given tuple.
    (The "tt" means "tuple in, tuple out".)
    """
    assert isinstance(the_tuple, tuple)
    return st_map(fun, the_tuple)


def sl_map(fun, the_sequence):
    """
    Map the given function over the given sequence (e.g. list or tuple).
    (The "sl" means "[any] sequence in, list out".)
    """
    if isinstance(fun, tuple):
        return [fun[0](*fun[1:], elem) for elem in the_sequence]
    return list(map(fun, the_sequence))


def st_map(fun, the_sequence):
    """
    Map the given function over the given sequence (e.g. list or tuple).
    (The "st" means "[any] sequence in, tuple out".)
    """
    if isinstance(fun, tuple):
        return tuple(fun[0](*fun[1:], elem) for elem in the_sequence)
    return tuple(map(fun, the_sequence))


def sum_of_lists(lists):
    """ Return the sum of lists. """
    accum = []
    for the_list in lists:
        accum.extend(the_list)
    return accum


def show_progress_g(uufileuu, *rest):
    """ Show a progress string. Typically called with first arg __file__. """
    # label is usually some sort of book name
    bn_uufileuu = os.path.basename(uufileuu)
    bn_and_rest = ' '.join((bn_uufileuu, *rest))
    print(bn_and_rest)


def _len_for_szip(obj):
    if not isinstance(obj, (tuple, list)):
        return len(tuple(obj))
    return len(obj)
