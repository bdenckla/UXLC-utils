""" Exports give_std_mark_order & has_std_mark_order """
import re
import my_hebrew_points as hpo


def give_std_mark_order(string):
    """
        Give the string (our) standard mark order.
        Our standard mark order is not Unicode-normal order,
        but we think it is a more reasonable order than Unicode-normal order.
        Our standard mark order has the following four marks first
        (in the order shown), followed by all other marks:
            shin dot
            sin dot
            dagesh/mapiq/shuruq dot
            rafeh
    """
    # TODO: what about varika?
    # 1. varika should be included in a cluster
    # 2. a standard order (combining class) should be given to varika
    patclu = r'[א-ת][\u0590-\u05cf]*'  # pattern for a cluster
    return re.sub(patclu, _repl_cluster, string)


def has_std_mark_order(string):
    """
        Say whether the string has (our) standard mark order.
    """
    return string == give_std_mark_order(string)


def _repl_cluster(match):
    wmat = match.group()  # the whole match
    lett, marks = wmat[0], wmat[1:]
    return lett + ''.join(sorted(marks, key=_ccs_keyfn))


_NS_COMB_CLASSES = {  # non-standard combining classes
    # Only the order matters, not the specific values. Both the order and
    # specific values below correspond to "SBL2", by which I mean the
    # non-standard combining classes suggested in the appendix to the manual
    # for the SBL Hebrew Font.
    hpo.SHIND: 10,
    hpo.SIND: 11,
    hpo.DAGESH_OM: 21,
    hpo.RAFE: 23,
}


def _ccs_keyfn(char):
    return _NS_COMB_CLASSES.get(char) or 300
