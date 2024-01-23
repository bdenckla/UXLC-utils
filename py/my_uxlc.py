""" Exports read """

import xml.etree.ElementTree

import my_tanakh_book_names as tbn
import my_sef_cmn


def read(book_id):
    """ Read book with id book_id into a list of chapters. """
    basename = (
        _UXLC_BOOK_FILE_NAMES.get(book_id) or
        my_sef_cmn.SEF_BKNA[book_id])
    xml_path = f'in/UXLC/{basename}.xml'
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    chapters = []
    for chapter in root.iter('c'):
        verses = []
        for verse in chapter.iter('v'):
            words = []
            for verse_child in verse:
                _dispatch_on_tag(words, verse_child, _VERSE_CHILD_FNS)
            verses.append(words)
        chapters.append(verses)
    return chapters


_UXLC_BOOK_FILE_NAMES = {
    tbn.BK_FST_SAM: 'Samuel_1',
    tbn.BK_SND_SAM: 'Samuel_2',
    tbn.BK_FST_KGS: 'Kings_1',
    tbn.BK_SND_KGS: 'Kings_2',
    tbn.BK_SONG: 'Song_of_Songs',
    tbn.BK_FST_CHR: 'Chronicles_1',
    tbn.BK_SND_CHR: 'Chronicles_2',
}

# GOs have 6 types:
#    w, a single word;
#    q, a word representing a qere variant;
#    k, a word representing a ketib variant;
#    pe, an empty tag representing an open paragraph marker;
#    samekh, an empty tag representing a closed paragraph marker,
#    reversednun, an empty tag representing a reversed nun.


def _handle_xc_ignore(_1, _2):  # xc means vc or wc (verse child or word child)
    return


def _handle_wc_s(accum, word_child_s):
    # The <s> element implements small, large, and suspended letters.
    # E.g. <s t="large">וֹ</s>.
    accum[-1] += word_child_s.text.strip()


_WORD_CHILD_FNS = {
    'x': _handle_xc_ignore,
    's': _handle_wc_s,
}


def _handle_vc_wq(accum, verse_child_wq):
    accum.append(verse_child_wq.text.strip())
    for word_child in verse_child_wq:
        _dispatch_on_tag(accum, word_child, _WORD_CHILD_FNS)
        accum[-1] += word_child.tail.strip()


_VERSE_CHILD_FNS = {
    'w':           _handle_vc_wq,
    'q':           _handle_vc_wq,
    'k':           _handle_xc_ignore,
    'x':           _handle_xc_ignore,
    'pe':          _handle_xc_ignore,
    'samekh':      _handle_xc_ignore,
    'reversednun': _handle_xc_ignore,
}


def _dispatch_on_tag(accum, verse_child, fns):
    fn_for_tag = fns[verse_child.tag]
    fn_for_tag(accum, verse_child)
