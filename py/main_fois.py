""" Exports main. """

import my_uxlc


def _handle_vc_wqk(wqk, accum, verse_child):
    accum.append([wqk, verse_child.text.strip()])
    for word_child in verse_child:
        my_uxlc.dispatch_on_tag(accum, word_child, my_uxlc._WORD_CHILD_HANDLERS)
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


def main():
    """ Writes UXLC features of interest to a JSON file. """
    uxlc = my_uxlc.read_all_books(_VERSE_CHILD_HANDLERS)
    pass


if __name__ == "__main__":
    main()
