

def parse(strs_and_tmpls):
    return _smt(_parse_str_or_tmpl, strs_and_tmpls)


def _smt(mapfn, mapels):
    return sum(map(mapfn, mapels), tuple())


def _parse_str_or_tmpl(wikitext_element):
    if isinstance(wikitext_element, dict):
        assert tuple(wikitext_element.keys()) == ('tmpl',)
        return (wikitext_element,)
    assert isinstance(wikitext_element, str)
    plainstr = wikitext_element
    if _has_lt_and_then_a_known_tag(plainstr):
        return _parse_tagful_str(plainstr)
    return (wikitext_element,)


_KNOWN_TAGS = (
    'קטע' + ' ',
    'noinclude', '/noinclude',
    'references/',
)


def _has_lt_and_then_a_known_tag(plainstr):
    for known_tag in _KNOWN_TAGS:
        ltkt = '<' + known_tag
        if ltkt in plainstr:
            return True
    return False


def _startswith_a_known_tag(plainstr):
    for known_tag in _KNOWN_TAGS:
        if plainstr.startswith(known_tag):
            return True
    return False


def _parse_tagful_str(in_str):
    pre, *rest = in_str.split('<')
    return _tupify(pre) + _smt(_parse2, rest)


def _parse2(in_str):
    inside, post = in_str.split('>')
    assert _startswith_a_known_tag(inside)
    return {'custom_tag': inside}, *_tupify(post)


def _tupify(in_str):  # tuple, but with empty string to empty tuple
    return tuple() if in_str == '' else (in_str,)
