""" Exports functions that help create and use templates. """

import my_utils


def template_element(tmpl: dict, idx: int):
    """ Return template element at index. """
    return template_elements(tmpl)[idx]


def template_arguments(tmpl):
    """ Return the second & any further elements. """
    return template_elements(tmpl)[1:]


def template_len(tmpl):
    """ Return the length of the template. """
    return len(template_elements(tmpl))


def is_template(wtel):
    """ Return whether wtel is a template. """
    if isinstance(wtel, str):
        return False
    assert isinstance(wtel, dict)
    return _dic_is_template(wtel)


def template_elements(tmpl):
    """ Return the elements of the given template. """
    return tmpl['tmpl']


def mktmpl(elements):
    """ Construct a template. """
    return {'tmpl': elements}


def mktmpl_from_stmpl(stmpl):
    """ Make a (general/complex) template from a simple template. """
    return mktmpl([[el_str] for el_str in stmpl['stmpl'].split('|')])


def template_00(tmpl):
    """ Return element 0 of element 0 of the given template. """
    return template_i0(tmpl, 0)


def template_i0(tmpl, idx: int):
    """ Return element 0 of element idx of the given template. """
    return my_utils.first_and_only(template_element(tmpl, idx))


def is_doc_template(wtel):
    """ Return whether wtel is a documentation template. """
    return _is_template_with_name(wtel, 'נוסח')


def strip_nameeq_from_el(tmpl, el_idx, name):
    """ Strip "name equals" from element el_idx of template tmpl """
    return _strip_prefix_from_wtseq(
        name + '=',
        template_element(tmpl, el_idx))


def _is_template_with_name(wtel, name):
    """ Return whether wtel is a template with the given name. """
    return is_template(wtel) and template_element(wtel, 0)[0] == name


def _dic_is_template(dic: dict):
    """ Return whether the given dict is a template. """
    return tuple(dic.keys()) == ('tmpl',)


def _strip_prefix_from_wtseq(prefix, in_list):
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
