""" Exports parse & debold """
import my_utils
import my_mam_wiki_tmpl as wtp1


def parse(string):
    """ Parse the wikitext in string """
    return _argsep(_dcs_to_tuples(debold(string)))


def debold(string):
    """ Remove triple apostrophes from the string """
    # https://github.com/bdenckla/trope/issues/62
    # (deal with triple apostrophes (bold))
    return string.replace("'''", '')


def _dcs_to_tuples(string):
    # dcs: double-curlies, i.e. templates set off by
    # double opening curly brackets &
    # double closing curly brackets.
    doc = string.find('{{')  # doc: double opening curlies
    if doc == -1:
        return tuple() if string == '' else (string,)
    dcc = _find_closing(string, doc+2)  # dcc: double closing curlies
    pre = _dcs_to_tuples(string[:doc])
    mid = _dcs_to_tuples(string[doc+2:dcc])
    post = _dcs_to_tuples(string[dcc+2:])
    return *pre, mid, *post


def _find_closing(string, idx):
    doc = string.find('{{', idx)  # doc: double opening curlies
    dcc = string.find('}}', idx)  # dcc: double closing curlies
    assert dcc != -1
    if doc != -1 and doc < dcc:
        dcc2 = _find_closing(string, doc+2)
        return _find_closing(string, dcc2+2)
    return dcc


def _argsep(els):
    none_sep = _bars_to_none(els)
    gathered = _gather_elements_btwn_nones(none_sep)
    return my_utils.first_and_only(gathered)


def _bars_to_none(els):
    return sum(map(_bars_to_none_one_el, els), tuple())


def _bars_to_none_one_el(element):
    if isinstance(element, str):
        args = element.split('|')
        isp = my_utils.intersperse(None, args)
        if isp[-1] == '':
            return isp[:-1]
        if isp[0] == '':
            return isp[1:]
        return isp
    assert isinstance(element, tuple)
    return (wtp1.mktmpl(_bars_to_none(element)),)


def _gather_elements_btwn_nones(els):
    out = [[]]
    for element in els:
        if element is None:
            out.append([])
            continue
        out[-1].append(_none_helper(element))
    return out


def _none_helper(element):
    if isinstance(element, str):
        return element
    return wtp1.mktmpl(
        _gather_elements_btwn_nones(
            wtp1.template_elements(element)))


# Note regarding the {{{טעמים|}}} arg to the מ:כפול template:
#
# This argument is removed in "MAM parsed plus" so this discussion
# is only relevant to things like "MAM parsed plain",
# the Google Sheet sources, and the Wikisource sources.
#
# We don't need the 1st arg, so we ignore it.
# The 1st arg is expected to be {{{טעמים|}}}.
# It is good that we don't need it because we parse it wrongly.
# It parses to a list of two Wikitext elements: a template "call" and a string.
# In more detail, these two elements are (in JSON):
#
#    {"tmpl": [["{טעמים"], []]},
#    "}"
#
# I.e. it parses to a list of the following two elements:
#
#    a template "call" with:
#       a singleton list of elements as its "0th" argument: ["{טעמים"]
#           i.e. a singleton list of elements as its "name" argument
#           where that single element is the string '{טעמים'
#           (an open curly brace then טעמים)
#       an empty list of elements as its 1st argument: []
#    a string, "}" (a closing curly brace)


_TEST_CASES_1 = (
    ('b', ('b',)),
    ('{{c}}', (('c',),)),
    ('b{{c}}', ('b', ('c',))),
    ('{{c}}d', (('c',), 'd')),
    ('b{{c}}d', ('b', ('c',), 'd')),
    ('a{{b{{c}}d}}e', ('a', ('b', ('c',), 'd'), 'e')),
    ('a{{b}}{{c}}{{d}}e', ('a', ('b',), ('c',), ('d',), 'e')),
)
_TEST_CASE_2_2_INP = 'A{{f|C{{g|c|d}}D|b}}B'
_TEST_CASE_2_2_OUT = [
    'A',
    {'tmpl': [
        ['f'],
        [
            'C',
            {'tmpl': [['g'], ['c'], ['d']]},
            'D'
        ],
        ['b']]},
    'B'
]
_TEST_CASES_2 = (
    ('{{f|a|b}}', [{'tmpl': [['f'], ['a'], ['b']]}]),
    (_TEST_CASE_2_2_INP, _TEST_CASE_2_2_OUT),
    (
        '{{C{{g}}|b}}',
        [{'tmpl': [['C', {'tmpl': [['g']]}], ['b']]}]),
    (
        '{{a|b|{{c|d}}}}',
        [{'tmpl': [['a'], ['b'], [{'tmpl': [['c'], ['d']]}]]}]),
)


def _do_quick_test():
    for test_case in _TEST_CASES_1:
        inp = test_case[0]
        act_out = _dcs_to_tuples(inp)
        print(f'input: {inp} output: {act_out}')
        exp_out = test_case[1]
        assert act_out == exp_out
    for test_case in _TEST_CASES_2:
        inp = test_case[0]
        act_out = parse(inp)
        print(f'input: {inp} output: {act_out}')
        exp_out = test_case[1]
        assert act_out == exp_out


if __name__ == "__main__":
    _do_quick_test()
