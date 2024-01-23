""" Exports handle. """
import my_render_wikitext_helpers as wt_help
import my_render_element as renel
import my_hebrew_points as hpo
import my_hebrew_accents as ha
import my_mam_wiki_tmpl2 as wtp
import my_utils
import my_qamats_qatan


def handle(hctx, tmpl):
    """
    Handle the מ:קמץ template by tagging the dalet variant with the
    appropriate dqq (disputed qamats qatan) tag: stressed or unstressed.
    This not only indicates that qamats variation exists but also
    indicates whether small meteg should be used or not.
    """
    #
    # We tag the dalet variant to record whether the syllable of the
    # disputed qamats already has a stress marker. See note above.
    #
    dalet_seq = _dalet_qamats_variation(hctx, tmpl)
    if wt_help.get_renopt(hctx, 'ro_qamats_var') == 'rv-dalet':
        return dalet_seq
    samekh_seq = _samekh_qamats_variation(hctx, tmpl)
    dalsam = (
        my_utils.first_and_only(dalet_seq),
        my_utils.first_and_only(samekh_seq))
    ad_rec = my_qamats_qatan.analyze_dalsam(dalsam)
    return (
        *ad_rec['undisputed-prefix'],
        *_handle_disputed(*ad_rec['disputed-part']),
        *ad_rec['undisputed-suffix'],
    )


def _handle_disputed(dalsep, _samsep, stress_mark):
    tag = None
    if stress_mark is not None:
        assert stress_mark in {ha.GER_M, hpo.METEG, ha.MER, ha.MUN}
        tag = 'mam-dqq-stressed'
    elif len(dalsep) == 3:
        tag = 'mam-dqq-unstressed'
    if tag:
        return (renel.mk_ren_el_tc(tag, ''.join(dalsep)),)
    assert len(dalsep) == 5
    dal0 = ''.join(dalsep[0:2])
    dal1 = ''.join(dalsep[2:5])
    dal0_renel = renel.mk_ren_el_tc('mam-dqq-unstressed', dal0)
    return dal0_renel, dal1


# I can say "THE syllable of THE disputed qamats" because luckily there is
# never more than one disputed qamats per word.
#
# I define a stress marker as a meteg or an accent indicating stress.
#
# A syllable has an accent indicating stress if one of the
# following is true of that syllable:
#
#    1. It has an impositive accent.
#    2. It has a stress helper accent.
#    3. It has a stressed non-impositive accent.
#
# (A non-impositive accent is stressed if its word neither has nor needs
# a stress helper.)
#
# Note that we consider revia to be the stress helper for geresh muqdam.
#
# It is unclear what to do about deḥi since MAM doesn’t have deḥi stress
# helpers. To determine whether a MAM deḥi indicates stress, we have to
# determine whether the word NEEDS a stress helper, since we know it won't
# HAVE a stress helper! Deḥi never appears on a syllable with qamats qatan,
# but I don't know if qamats qatan ever appears on a syllable that needs
# a deḥi stress helper. I guess it is okay to have small meteg on such
# a syllable though.


def _dalet_qamats_variation(hctx, tmpl):
    """ Return the dalet variant. """
    # {{מ:קמץ|ד=אאא|ס=בבב}}
    #
    # The dalet argument is the "theoretical" variant.
    # The samekh argument is the Sephardic variant.
    #
    assert wtp.template_len(tmpl) == 3
    return wt_help.render_named_tmpl_el(hctx, tmpl, 1, 'ד')


def _samekh_qamats_variation(hctx, tmpl):
    """ Return the sameh variant. """
    assert wtp.template_len(tmpl) == 3
    return wt_help.render_named_tmpl_el(hctx, tmpl, 2, str('ס'))
