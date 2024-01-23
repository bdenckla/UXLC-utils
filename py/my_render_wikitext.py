"""
Exports:
    render
"""

from dataclasses import dataclass

import my_render_wikitext_handlers as handlers
import my_render_wikitext_helpers as wt_help
import my_tanakh_book_names as tbn
import my_utils

# renopts: options as to what the verse bodies should contain.
#     ro_cantillation:
#         'rv-cant-dual': combined cantillation (the default)
#         'rv-cant-alef': alef strand of cantillation
#         'rv-cant-bet': bet strand of cantillation
#         'rv-cant-all-three': all three of the above
#         There are 3 dualcant texts: Reuben, Ex Dec, & Deut Dec.
#             dualcant: dually (doubly) cantillated
#             Reuben: Gen 35:22
#             Ex Dec: Exodus Decalogue
#             Deut Dec: Deuteronomy Decalogue
#         Each dualcant text has an alef & bet "strand".
#             For Reuben: alef=פשוטה & bet=מדרשית
#             For Decalogues: alef=taxton & bet=elyon


def render(bkid, books, renopts=None):
    """
    bkid: book ID from my_tanakh_book_names
    books: maps a book ID to parsed Wikitext book contents
    renopts: see above

    Given these inputs, this function:

    Returns a dict mapping a cvt to a verse body.
    cvt = chapter and verse qualified by vtrad
    The verse body is a tuple of text elements.
    A text element is a string or a dict with a '_ren_tag' key
        and 0 or more other keys. Those other keys often
        include a 'contents' key, holding a tuple of text elements.
    """
    verses = books[bkid]['verses']
    bbr = bkid, books, renopts
    return {
        cvt: _render_minirow(bbr, cvt, minirow)
        for cvt, minirow in verses.items()
    }

@dataclass
class VerseAndFriends:
    """ Holds verse, maybe a next CP, & maybe a good ending. """
    verse: tuple
    next_cp: tuple
    good_ending: tuple
    def map_over(self, fun):
        """
        Make a new veraf by mapping fun over the fields of this veraf.
        """
        if isinstance(fun, tuple):
            return VerseAndFriends(
                fun[0](*fun[1:], self.verse),
                fun[0](*fun[1:], self.next_cp),
                fun[0](*fun[1:], self.good_ending),
            )
        return VerseAndFriends(
            fun(self.verse),
            fun(self.next_cp),
            fun(self.good_ending),
        )


def map_over_verafs(fun, verafs):
    """ Map fun over verafs. """
    return my_utils.sl_map((_map_over_veraf, fun), verafs)


def _map_over_veraf(fun, veraf: VerseAndFriends):
    """
    Make a new veraf by mapping fun over the fields of the given veraf.
    """
    return veraf.map_over(fun)


def _render_minirow(bbr, cvt, minirow):
    if minirow is None:  # possibly Joshua 21:36 & 21:37
        return VerseAndFriends(('\N{EM DASH}',), tuple(), tuple())
    bkid, books, renopts = bbr
    hctx = handlers.default_hctx(tbn.mk_bcvt(bkid, cvt), renopts)
    ep_renseq = wt_help.render_wtseq(
        hctx,
        minirow.EP)
    ncp_renseq = wt_help.render_wtseq(
        handlers.colc_hctx(hctx),
        minirow.next_CP)
    ge_renseq = wt_help.render_wtseq(
        hctx,
        _good_ending_wtseq(bkid, books, cvt))
    return VerseAndFriends(ep_renseq, ncp_renseq, ge_renseq)


def _good_ending_wtseq(bkid, books, cvt):
    good_ending = books[bkid]['good_ending']
    if good_ending and cvt == good_ending['last_chapnver']:
        wtel = good_ending['wikitext_element']
        return (wtel,)
    return tuple()
