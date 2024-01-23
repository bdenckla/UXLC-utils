"""
Exports:
    render_wtseq
    render_tmpl_el
    render_named_tmpl_el
    get_renopt
    strip_brackets_of_some_kind
"""
from dataclasses import dataclass

import my_scrdfftar_to_doc
import my_mam_wiki_tmpl2 as wtp
import my_shrink
import my_unicode_check


@dataclass
class Hctx:
    """ Holds rendering context. """
    handlers: dict
    bcvt: tuple = None
    renopts: dict = None
    def mk_new_with_handler(self, handler):
        """ Make a new Hctx with the given handler. """
        return Hctx(handler, self.bcvt, self.renopts)


def render_wtseq(hctx, wtseq):
    """ Dispatch a sequence of Wikitext elements to their handlers. """
    newseq = wtseq
    if get_renopt(hctx, 'ro_scrdfftar_to_doc'):
        newseq = my_scrdfftar_to_doc.convert(newseq)
    handled_elements = tuple(
        _handle_wikitext_element(hctx, wtel)
        for wtel in newseq)
    het = map(_tuplify, handled_elements)
    out = my_shrink.shrink(sum(het, tuple()))
    my_unicode_check.check(out)
    return out



def render_tmpl_el(hctx, tmpl, index):
    """ Render the template element at the given index. """
    return render_wtseq(hctx, wtp.template_element(tmpl, index))


def render_named_tmpl_el(hctx, tmpl, index, name):
    """ Handle argument with the given name at position el_idx """
    new_wtseq = wtp.named_template_element(tmpl, index, name)
    return render_wtseq(hctx, new_wtseq)


def get_renopt(hctx, opt_name: str):
    """ Return None or render option named opt_name. """
    return hctx.renopts.get(opt_name) if hctx.renopts else None


def strip_brackets_of_some_kind(brackets, string):
    """
    Strip brackets in the general sense of "brackets",
    i.e. including parens, curly braces, and square brackets.
    """
    assert string.startswith(brackets[0]) and string.endswith(brackets[1])
    return string[1:-1]


def _tuplify(tup_or_nontup):
    if isinstance(tup_or_nontup, tuple):
        return tup_or_nontup
    return (tup_or_nontup,)


def _handle_wikitext_element(hctx: Hctx, elem):
    dispatch_key = _dispatch_key(elem)
    handler = hctx.handlers[dispatch_key]
    return handler(hctx, elem)


def _dispatch_key(elem):
    if isinstance(elem, str):
        return elem if elem == '__' else str
    if wtp.is_template(elem):
        return wtp.template_name(elem)
    assert False
