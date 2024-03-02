

def init():
    return {
        'kq_type_count': {'k0q1': 0, 'k1q0': 0, 'k1q1': 0, 'k2q1': 0, 'k1q2': 0, 'k2q2': 0},
        'kq_cases': {'k0q1': [], 'k1q0': [], 'k2q1': [], 'k1q2': [], 'k2q2': []}
    }


def collect_for_verse(fois, bcv, verse):
    state = {'k_stack': [], 'q_stack': []}
    for atidx, atom in enumerate(verse):
        assert isinstance(atom, list)
        assert len(atom) == 2
        assert atom[0] in ('w', 'k', 'q')
        bcvp = *bcv, atidx+1
        _collect_for_atom(state, fois, bcvp, atom)
    _record_and_clear(state, fois, bcvp)


def _quad(state):
    k_stack, q_stack = state['k_stack'], state['q_stack']
    numk, numq = len(k_stack), len(q_stack)
    return k_stack, q_stack, numk, numq


def _stacks_are_equal_len(state):
    _k_stack, _q_stack, numk, numq = _quad(state)
    return numk == numq


def _collect_for_atom(state, fois, bcvp, atom):
    if atom[0] == 'w':
        _record_and_clear(state, fois, bcvp)
        return
    if atom[0] == 'k':
        if _stacks_are_equal_len(state):
            _record_and_clear(state, fois, bcvp)
        state['k_stack'].append(atom[1])
        return
    if atom[0] == 'q':
        state['q_stack'].append(atom[1])
        return
    assert False


def _record_and_clear(state, fois, bcvp):
    k_stack, q_stack, numk, numq = _quad(state)
    if (numk, numq) == (0, 0):
        return
    str_key = _knqm_str(numk, numq)
    fois['kq_type_count'][str_key] += 1
    if (numk, numq) != (1, 1):
        str_for_case = '/'.join((*k_stack, *q_stack))
        fois['kq_cases'][str_key].append((_bcvp_str(bcvp), str_for_case))
    state['k_stack'] = []
    state['q_stack'] = []


def _knqm_str(numk, numq):
    return f'k{numk}q{numq}'


def _bcvp_str(bcvp):
    bkid, chnu, vrnu, atnu = bcvp
    return f'{bkid} {chnu}:{vrnu}.{atnu}'