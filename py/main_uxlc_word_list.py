"""
Exports main

You can download a fresh zip of XML files for all 39 books using the URL
https://tanach.us/Books/Tanach.xml.zip
"""
import unicodedata
import my_uxlc
import my_open
import my_tanakh_book_names as tbn
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_uni_norm_fragile as unf
import my_uni_heb as uh


def _is_uxlc_fragile(string):
    # UXLC has a more lenient definition of fragile than we use for MAM
    #
    # TODO: consider וַיִּקְבְֹּ֥ר (w,_,y,·,i,q,:,v,·,o,:,(me),r) to be robust
    # because (o,:) i.e., (ḥolam,sheva) is actualy UXLC-standard order.
    # I.e., it is extraordinary to have both of these vowels on a single
    # letter, but if we allow this to happen, this is actually the
    # UXLC-standard order for these vowel code points.
    # And, getting to the deeper defintion of robust, I don't think
    # order matters for this code point, for any font & text rendering stack.
    #
    return unf.is_fragile(_lai_to_lia(string))


def _lai_to_lia(string):
    # "a" in lai & lia includes pataḥ & qamats
    # "i" in lai & lia stands for ḥiriq & sheva
    # Not all 4 combinations occur. In particular
    # we don't need to handle qamats sheva, so we don't
    # handle it.
    #
    # Perhaps we should have implemented the code with
    # a regex substitution rather than an iterative
    # literal substitution. But perhaps it is simpler this way.
    #
    work_str = string
    mids = (
        (hpo.PATAX, hpo.XIRIQ),
        (hpo.QAMATS, hpo.XIRIQ),
        (hpo.PATAX, hpo.SHEVA))
    for mid in mids:
        lai = hl.LAMED + mid[0] + mid[1]
        lia = hl.LAMED + mid[1] + mid[0]
        work_str = work_str.replace(lai, lia)
    return work_str


def _annotate_word(fragile_word):
    f_w = fragile_word
    f_w_n = unicodedata.normalize('NFC', f_w)
    fcs0 = unf.get_fragile_comps(fragile_word)
    fcs1 = tuple(map(uh.comma_shunnas, fcs0))
    return {
        'fragile_word_u': f_w,
        'fragile_word_n': f_w_n,
        'fragile_word_u_cs': uh.comma_shunnas(f_w),
        'fragile_word_n_cs': uh.comma_shunnas(f_w_n),
        'fragile_word_u_with_drops': fcs1[0],
        'fragile_word_n_with_drops': fcs1[1]}


def main():
    """ Extracts two word list files (all, fragile) from UXLC sources. """
    words_all = set()
    for book_id in tbn.ALL_BOOK_IDS:
        for chapter in my_uxlc.read(book_id):
            for verse in chapter:
                words_all |= set(verse)
    words_all = sorted(words_all)
    words_fr0 = filter(_is_uxlc_fragile, words_all)
    words_fr1 = sorted(words_fr0)
    words_fr2 = tuple(map(_annotate_word, words_fr1))
    out_path_all = 'out/uxlc-words.json'
    out_path_fra = 'out/uxlc-words-fragile.json'
    my_open.json_dump_to_file_path(words_all, out_path_all)
    my_open.json_dump_to_file_path(words_fr2, out_path_fra)


if __name__ == "__main__":
    main()
