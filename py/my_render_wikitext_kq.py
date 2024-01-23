""" Exports various handle_.* routines related to ketiv/qere """

import my_hebrew_punctuation as hpu
import my_render_element as renel
import my_shrink
import my_render_wikitext_helpers as wt_help
import my_mam_wiki_tmpl2 as wtp
import my_wdk_ketiv_qere
import my_utils


def handle_kq_ketiv_qere(hctx, tmpl):
    """ Handle a normal ketiv/qere. """
    return _ht_kq(hctx, tmpl, 'k1q1-kq')


def handle_kq_qere_ketiv(hctx, tmpl):
    """
    Handle a ketiv/qere where template arguments are in kq order
    but they should appear in reverse order (qk order).
    """
    return _ht_kq(hctx, tmpl, 'k1q1-qk')


def handle_k1q1_mcom(hctx, tmpl):  # I26:20
    """ Handle a ketiv/qere that is mid-compound, i.e. b in a-b-c. """
    return _ht_kq(hctx, tmpl, 'k1q1-mcom')


def handle_k1q2_sr_kqq(hctx, tmpl):  # 13 cases
    """
    Handle a k1q2 that is sr (strongly-related), where the atoms should
    be presented in kqq order
    """
    return _ht_kq(hctx, tmpl, 'k1q2-sr-kqq')


def handle_k1q2_sr_qqk(hctx, tmpl):  # Ne2:13
    """
    Handle a k1q2 that is sr (strongly-related), where the atoms should
    be presentd in qqk order
    """
    return _ht_kq(hctx, tmpl, 'k1q2-sr-qqk')


def handle_k1q2_sr_bcom(hctx, tmpl):  # 1C9:4
    """
    Handle a k1q2 that is sr (strongly-related), where the atoms are
    between two compounds, i.e. c in a-b c d-e
    read as a-b d-e
    appears in scroll as a c e
    i.e. ketiv c maps to qere "b d"
    """
    return _ht_kq(hctx, tmpl, 'k1q2-sr-bcom')


def handle_k1q2_wr_kqq(hctx, tmpl):  # Ezekiel 9:11
    """ Handle a k1q2 that is wr (weakly-related). """
    return _ht_kq(hctx, tmpl, 'k1q2-wr-kqq')


def handle_k1q2_ur_qkk(hctx, tmpl):  # 2K 18:27 & I 36:12.
    """ Handle a k1q2 that is ur (unrelated): meimei ragleihem. """
    return _ht_kq(hctx, tmpl, 'k1q2-ur-qqk')


def handle_k2q1(hctx, tmpl):
    """ Handle a k2q1. """
    return _ht_kq(hctx, tmpl, 'k2q1')


def handle_k2q2(hctx, tmpl):
    """ Handle a k2q2. """
    return _ht_kq(hctx, tmpl, 'k2q2')


def _style_is_abstract(hctx):
    ro_kq_style = wt_help.get_renopt(hctx, 'ro_kq_style')
    return ro_kq_style == 'rv-kq-abstract'


def _maybe_kq_separator(hctx, kq_type):
    ketiv_maqaf = set(('k1q1-mcom', 'k1q2-sr-bcom'))
    sep_is_maq = kq_type in ketiv_maqaf
    dic = {
        True: (hpu.MAQ, 'mam-kq-sep-maqaf'),
        False: (' ', 'mam-kq-sep-space'),
    }
    sep_char, abstract_tag = dic[sep_is_maq]
    if _style_is_abstract(hctx):
        return tuple(), abstract_tag
    return (sep_char,), 'mam-kq'


def _ht_kq(hctx, tmpl, kq_type):
    k_wtseq, q_wtseq = _ht_kq_unpack_args(tmpl)
    k_renseq = wt_help.render_wtseq(hctx, k_wtseq)
    q_renseq = wt_help.render_wtseq(hctx, q_wtseq)
    k_in_parens = _maybe_paren_kq_ketiv(hctx, k_renseq)
    q_in_sqbracs = _maybe_sqbrac_kq_qere(hctx, q_renseq)
    kq_separator, kq_tag = _maybe_kq_separator(hctx, kq_type)
    kq_contents = (
        renel.mk_ren_el_tc('mam-kq-k', k_in_parens),
        *kq_separator,
        renel.mk_ren_el_tc('mam-kq-q', q_in_sqbracs))
    if not my_wdk_ketiv_qere.PUT_KETIV_1ST[kq_type]:
        kq_contents = tuple(reversed(kq_contents))
    return renel.mk_ren_el_tc(kq_tag, kq_contents)


def _ht_kq_unpack_args(tmpl):
    # We can assert that the length is 3 because the רווח=כן
    # case present in the Google Sheet is absent from "MAM parsed plus".
    assert wtp.template_len(tmpl) == 3
    ketiv = wtp.template_element(tmpl, 1)
    qere = wtp.template_element(tmpl, 2)
    return ketiv, qere


def _paren(seq):
    return my_shrink.shrink(('(', *seq, ')',))


def _sqbrac(seq):
    return my_shrink.shrink(('[', *seq, ']',))


def _maybe_sqbrac_kq_qere(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _sqbrac(wtseq)


def _maybe_paren_kq_ketiv(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _paren(wtseq)


def handle_kq_ketiv_velo_qere(hctx, tmpl):
    """ Handle a ketiv velo qere. """
    assert wtp.template_len(tmpl) == 2
    # letters already parenthesized in source; maqaf outside parens
    ketiv_r = wt_help.render_tmpl_el(hctx, tmpl, 1)  # ketiv, rendered
    ketiv_r_npnm, ask_for_maq = _maybe_rm_punc_fr_k_velo_q(hctx, ketiv_r)
    tag = 'mam-kq-k-velo-q-maq' if ask_for_maq else 'mam-kq-k-velo-q'
    return (renel.mk_ren_el_tc(tag, ketiv_r_npnm),)


def _maybe_rm_punc_fr_k_velo_q(hctx, wtseq):
    wtel = my_utils.first_and_only_and_str(wtseq)
    ro_k_velo_q_style = wt_help.get_renopt(hctx, 'ro_k_velo_q_style')
    npnm = ro_k_velo_q_style == 'rv-no-paren-no-maqaf'
    ask_for_maq = wtel[-1] == hpu.MAQ and npnm
    ht1_nm = wtel[:-1] if ask_for_maq else wtel
    out_str = _strip_paren(ht1_nm) if npnm else ht1_nm
    return (out_str,), ask_for_maq


def _strip_paren(string):
    return wt_help.strip_brackets_of_some_kind('()', string)
