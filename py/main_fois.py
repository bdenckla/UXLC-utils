""" Exports main. """

import my_uxlc
import my_open


def _handle_vc_wqk(wqk, accum, verse_child):
    accum.append([wqk, verse_child.text.strip()])
    for word_child in verse_child:
        my_uxlc.dispatch_on_tag(accum, word_child, _WORD_CHILD_HANDLERS)
        accum[-1][1] += word_child.tail.strip()


def _handle_vc_w(accum, verse_child):
    _handle_vc_wqk('w', accum, verse_child)


def _handle_vc_q(accum, verse_child):
    _handle_vc_wqk('q', accum, verse_child)


def _handle_vc_k(accum, verse_child):
    _handle_vc_wqk('k', accum, verse_child)


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    accum[-1][1] += word_child_s.text.strip()


_WORD_CHILD_HANDLERS = {
    'x': my_uxlc.handle_xc_ignore,
    's': _handle_wc_s,
}
_VERSE_CHILD_HANDLERS = {
    'w':           _handle_vc_w,
    'q':           _handle_vc_q,
    'k':           _handle_vc_k,
    'x':           my_uxlc.handle_xc_ignore,
    'pe':          my_uxlc.handle_xc_ignore,
    'samekh':      my_uxlc.handle_xc_ignore,
    'reversednun': my_uxlc.handle_xc_ignore,
}


def _collect_for_atom(state, fois, atom):
    if atom[0] == 'w':
        _record_and_clear(state, fois)
        return
    if atom[0] == 'k':
        k_stack, q_stack = state['k_stack'], state['q_stack']
        numk, numq = len(k_stack), len(q_stack)
        if numk == numq:
            _record_and_clear(state, fois)
        state['k_stack'].append(atom[1])
        return
    if atom[0] == 'q':
        state['q_stack'].append(atom[1])
        return
    assert False


def _record_and_clear(state, fois):
    k_stack, q_stack = state['k_stack'], state['q_stack']
    numk, numq = len(k_stack), len(q_stack)
    if (numk, numq) == (0, 0):
        return
    str_key = _str_key(numk, numq)
    fois['kq_type_count'][str_key] += 1
    if (numk, numq) != (1, 1):
        str_for_case = '/'.join((*k_stack, *q_stack))
        fois['kq_cases'][str_key].append(str_for_case)
    state['k_stack'] = []
    state['q_stack'] = []


def _str_key(numk, numq):
    return f'k{numk}q{numq}'


def _collect_for_verse(fois, verse):
    state = {'k_stack': [], 'q_stack': []}
    for atom in verse:
        assert isinstance(atom, list)
        assert len(atom) == 2
        assert atom[0] in ('w', 'k', 'q')
        _collect_for_atom(state, fois, atom)
    _record_and_clear(state, fois)


def main():
    """ Writes UXLC features of interest to a JSON file. """
    uxlc = my_uxlc.read_all_books(_VERSE_CHILD_HANDLERS)
    fois = {
        'kq_type_count': {'k0q1': 0, 'k1q0': 0, 'k1q1': 0, 'k2q1': 0, 'k1q2': 0, 'k2q2': 0},
        'kq_cases': {'k0q1': [], 'k1q0': [], 'k2q1': [], 'k1q2': [], 'k2q2': []}
    }
    for _bkid, chapters in uxlc.items():
        for chapter in chapters:
            for verse in chapter:
                _collect_for_verse(fois, verse)
    json_output_path = 'out/UXLC-misc/features_of_interest.json'
    my_open.json_dump_to_file_path(fois, json_output_path)


if __name__ == "__main__":
    main()
