""" Exports unparse """
import my_mam_wiki_tmpl as wtp1
import my_utils


def unparse(wikitext_sequence):
    """ Return a string containing the unparsed the Wikitext sequence.
    I use "unparse" to mean "reverse the parsing process".
    """
    return ''.join(map(_unparse_wtel, wikitext_sequence))


def _unparse_wikitext_str(wtel_str):
    return wtel_str


def _unparse_wikitext_tmpl(wtel_tmpl):
    tmpl_els = wtp1.template_elements(wtel_tmpl)
    bar_separated_els = '|'.join(map(unparse, tmpl_els))
    return '{{' + bar_separated_els + '}}'


def _unparse_wikitext_custom_tag(wtel_cuta):
    return '<' + wtel_cuta['custom_tag'] + '>'


_WIKITEXT_HANDLERS = {
    (str, None): _unparse_wikitext_str,
    (dict, 'tmpl'): _unparse_wikitext_tmpl,
    (dict, 'custom_tag'): _unparse_wikitext_custom_tag,
}


def _single_key(obj):
    if not isinstance(obj, dict):
        assert isinstance(obj, str)
        return None
    keys = tuple(obj.keys())
    return my_utils.first_and_only(keys)


def _unparse_wtel(wikitext_el):
    elem = wikitext_el
    handler = _WIKITEXT_HANDLERS[type(elem), _single_key(elem)]
    return handler(elem)
