PUT_KETIV_1ST = {
    'k1q1-kq': True,
    'k1q1-mcom': True,
    'k1q2-sr-kqq': True,
    'k1q2-sr-bcom': True,
    'k1q2-wr-kqq': True,
    'k1q2-ur-kqq': True,  # not "naturally occurring"
    'k2q1': True,
    'k2q2': True,
    #
    'k1q1-qk': False,
    'k1q2-sr-qqk': False,
    'k1q2-ur-qqk': False,
}
# Above, k1q2-ur-kqq is not "naturally occurring";
# it is the "k 1st" counterpart to k1q2-ur-qqk.
# It is used only for JPS.
RIRQ_INITIAL_ONLY = ('initial',)
RIRQ_FINAL_ONLY = ('final',)
RIRQ_INITIAL_AND_FINAL = RIRQ_INITIAL_ONLY + RIRQ_FINAL_ONLY
EIEF_TO_ROLES_IN_RANGE = {
    (True, True): RIRQ_INITIAL_AND_FINAL,
    (True, False): RIRQ_INITIAL_ONLY,
    (False, True): RIRQ_FINAL_ONLY
    # medial does not exist (max is 2 words)
}


def put_k_1st(ketiv_rec):
    return PUT_KETIV_1ST[ketiv_rec['ketiv_type']]


def is_initial_only(rirq):
    return rirq == RIRQ_INITIAL_ONLY


def is_final_only(rirq):
    return rirq == RIRQ_FINAL_ONLY


def is_final_only_w(word):
    if ki_rirq := word.get('ki_rirq'):
        return is_final_only(ki_rirq[1])
    return False


def is_initial_only_w(word):
    if ki_rirq := word.get('ki_rirq'):
        return is_initial_only(ki_rirq[1])
    return False


def is_initial_and_final(rirq):
    return rirq == RIRQ_INITIAL_AND_FINAL


def is_initial(rirq):
    return is_initial_only(rirq) or is_initial_and_final(rirq)


def is_final(rirq):
    return is_final_only(rirq) or is_initial_and_final(rirq)
