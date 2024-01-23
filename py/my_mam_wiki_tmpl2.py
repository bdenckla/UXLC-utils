""" Exports functions that help create and use templates. """

import my_utils
import my_mam_wiki_tmpl as wtp1


def template_element(tmpl: dict, idx: int):
    """ Return template element at index. """
    if idx == 0:
        return [tmpl['tmpl_name']]
    return template_arguments(tmpl)[idx-1]


def named_template_element(tmpl: dict, idx: int, name: str):
    """
    For element ['foo=bar', 'baz'] at index, return ['bar', 'baz'].
    """
    return _strip_prefix(name + '=', template_element(tmpl, idx))


def template_elements(tmpl):
    """ Return all elements. """
    return [[tmpl['tmpl_name']], *template_arguments(tmpl)]


def template_arguments(tmpl):
    """ Return the second & any further elements. """
    return _restore_singletons(tmpl.get('tmpl_args', []))


def template_len(tmpl):
    """ Return the length of the template. """
    return 1 + len(template_arguments(tmpl))


def is_template(wtel):
    """ Return whether wtel is a template. """
    if isinstance(wtel, str):
        return False
    assert isinstance(wtel, dict)
    return dic_is_template(wtel)


def is_custom_tag(wtel):
    """ Return whether wtel is a custom tag. """
    return isinstance(wtel, dict) and tuple(wtel.keys()) == ('custom_tag',)


def is_template_with_name(wtel, name):
    """ Return whether wtel is a template with the given name. """
    return is_template(wtel) and wtel['tmpl_name'] == name


def is_template_with_name_in(wtel, names):
    """ Return whether wtel is a template with on eof the given names. """
    return is_template(wtel) and wtel['tmpl_name'] in names


def dic_is_template(dic: dict):
    """ Return whether the given dict is a template. """
    return tuple(dic.keys()) in (
        ('tmpl_name',),
        ('tmpl_name', 'tmpl_args'))


def mktmpl(elements):
    """ Construct a template. """
    name = my_utils.first_and_only(elements[0])
    args = elements[1:]
    if len(args) == 0:
        return {'tmpl_name': name}
    if name == 'נוסח' and len(args[0]) == 0:
        # Various code expects the 1st arg to נוסח to be [''] not []
        # ([] often results from calling "shrink")
        # XXX tweak that code to allow [''] or []
        return mktmpl([['נוסח'], [''], *args[1:]])
    return {'tmpl_name': name, 'tmpl_args': _simplify_singletons(args)}


def map_args(fun, tmpl2):
    """ Map a function over the args of a template. """
    tmpl_args = template_arguments(tmpl2)
    return mktmpl([
        [template_name(tmpl2)],
        *my_utils.ll_map(fun, tmpl_args)])


def mktmpl2_fr_tmpl1_els(tmpl1_els):
    """ Construct a tmpl2 from the elements of a tmpl1. """
    return mktmpl(_use_tmpl2_in_tmpl1_els(tmpl1_els))


def use_tmpl2(wtel):
    """ Use tmpl2 format for this wtel & below """
    if wtp1.is_template(wtel):
        return mktmpl2_fr_tmpl1_els(wtp1.template_elements(wtel))
    return wtel


def use_tmpl2_in_wtseq(wtseq):
    """ Use tmpl2 format in the given wtseq. """
    assert isinstance(wtseq, (list, tuple))
    type_of_wtseq = type(wtseq)
    return type_of_wtseq(map(use_tmpl2, wtseq))


def template_name(tmpl):
    """ Return element 0 of element 0 of the given template. """
    return tmpl['tmpl_name']


def template_i0(tmpl, idx: int):
    """ Return element 0 of element idx of the given template. """
    return my_utils.first_and_only(template_element(tmpl, idx))


def tmpl_arg_i0(tmpl, idx: int):
    """ Return element 0 of arg idx of the given template. """
    return my_utils.first_and_only(template_arguments(tmpl)[idx])


def template_i0_maybe(tmpl, idx, default=None):
    """
    Acts like template_i0 if element i exists and is nonempty.
    Otherwise returns default.
    At the time of this writing, only used in _handle_yerushalax.
    """
    if template_len(tmpl) <= idx:
        return default
    eli = template_element(tmpl, idx)
    return default if len(eli) == 0 else my_utils.first_and_only(eli)


def is_doc_template(wtel):
    """ Return whether wtel is a documentation template. """
    return is_template_with_name(wtel, 'נוסח')


def is_scrdff_template(wtel):
    """ Return whether wtel is a scrdff template. """
    return is_template_with_name(wtel, 'מ:הערה')


def _strip_prefix(prefix, in_list):
    """ Strip prefix off first element of in_list """
    # Example in_list/output table, assuming prefix='pre'
    #
    # in_list          | output
    # ---------------- | ------------
    # ['pre=foo']      | ['foo']
    # ['pre=foo', bar] | ['foo', bar]
    # ['pre=', bar]    | [bar]
    #
    assert isinstance(in_list, list)
    assert isinstance(in_list[0], str)
    assert in_list[0].startswith(prefix)
    new_el0 = in_list[0][len(prefix):]
    return [new_el0] + in_list[1:] if new_el0 else in_list[1:]


SDT_ARG_IDX_FOR_TARG = 1
SDT_ARG_IDX_FOR_NOTE = 2
SDT_ARG_IDX_FOR_STARPOS = 3
#
SLHW_ARG_IDX_FOR_TARG = 1
SLHW_ARG_IDX_FOR_DESC0 = 2
SLHW_ARG_IDX_FOR_DESC1 = 3
SLHW_ARG_IDX_FOR_DESC2 = 4
SLHW_ARG_IDX_FOR_DESC3 = 5


def _simplify_singletons(tmpl2_args):
    assert isinstance(tmpl2_args, list)
    return list(map(_simplify_singleton, tmpl2_args))


def _simplify_singleton(tmpl2_arg):
    assert isinstance(tmpl2_arg, list)
    if len(tmpl2_arg) == 1:
        return tmpl2_arg[0]
    return tmpl2_arg


def _restore_singletons(tmpl2_args):
    assert isinstance(tmpl2_args, list)
    return list(map(_restore_singleton, tmpl2_args))


def _restore_singleton(tmpl2_arg):
    if isinstance(tmpl2_arg, (dict, str)):
        return [tmpl2_arg]
    assert isinstance(tmpl2_arg, list)
    return tmpl2_arg


def _use_tmpl2_in_tmpl1_els(tmpl1_els):
    assert isinstance(tmpl1_els, list)
    return list(map(use_tmpl2_in_wtseq, tmpl1_els))
