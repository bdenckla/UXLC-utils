"""
Exports:
    default_hctx(bcvt=None, renopts=None)
    colc_hctx(hctx: wt_help.Hctx)
"""
import my_render_wikitext_dispatch as dispatch
import my_use_true_gershayim
import my_versification
import my_utils
import my_mam_doc_utils as doc_utils
import my_str_defs as sd
import my_hebrew_punctuation as hpu
import my_mam_wiki_tmpl2 as wtp
import my_render_wikitext_kq as kq
import my_template_names as tmpln
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_render_wikitext_spacing_concerns as spacing
import my_render_wikitext_handlers_for_qamats as qamats_variation
import my_render_wikitext_helpers as wt_help
import my_render_element as renel


def default_hctx(bcvt=None, renopts=None):
    """ Return the default Hctx. """
    return wt_help.Hctx(_GEN_WT_HANDLERS, bcvt, renopts)


def colc_hctx(hctx: wt_help.Hctx):
    """ Return a new version of hctx with column C handlers active. """
    return hctx.mk_new_with_handler(_COL_C_HANDLERS)


def _handle_doc(hctx, tmpl):
    assert wtp.template_len(tmpl) >= 3
    doc_target_wtseq = wtp.template_arguments(tmpl)[0]
    doc_target_renseq = wt_help.render_wtseq(hctx, doc_target_wtseq)
    if wt_help.get_renopt(hctx, 'ro_no_doc'):
        return doc_target_renseq
    tr_space, doc_target_stripped = spacing.isolate_trailing(doc_target_renseq)
    doc_parts_wtseqs = wtp.template_arguments(tmpl)[1:]
    main_out = renel.mk_ren_el_tcd(
        'mam-doc', doc_target_stripped,
        _doc_lemma_subhandler(hctx, doc_target_wtseq),
        _doc_parts_subhandler(hctx, doc_parts_wtseqs))
    return main_out, tr_space


def _ignore(_hctx, _tmpl):
    return ''


def _handle_scrdfftar(hctx, tmpl):
    """
    This is displayed on Wikisource as a footnote.
    Don't confuse this template with the much more common
    documentation template (נוסח).
    """
    assert wtp.template_len(tmpl) == 4
    targ_ren_el = _mrel_fr_tel(
        'sdt-target', hctx, tmpl, wtp.SDT_ARG_IDX_FOR_TARG)
    note_renseq = wt_help.render_tmpl_el(hctx, tmpl, wtp.SDT_ARG_IDX_FOR_NOTE)
    starpos_in = wtp.template_i0(tmpl, wtp.SDT_ARG_IDX_FOR_STARPOS)
    #
    note_renseq = my_use_true_gershayim.in_seq(note_renseq)
    #
    note_ren_el = renel.mk_ren_el_tc('sdt-note', note_renseq)
    contents = targ_ren_el, note_ren_el
    attr = {'sdt-starpos': _ATTR_VAL_FROM_ALEFS[starpos_in]}
    return renel.mk_ren_el_tca('scrdfftar', contents, attr)


_ATTR_VAL_FROM_ALEFS = {
    '*אאא': 'before-word',
    'אאא*': 'after-word',
}


def _mrel_fr_tel(tag, hctx, tmpl, index):
    # Make ren_el from tmpl_el
    return renel.mk_ren_el_tc(tag, wt_help.render_tmpl_el(hctx, tmpl, index))


def _ren_to_str(hctx, tmpl, index):
    ren_el = wt_help.render_tmpl_el(hctx, tmpl, index)
    return my_utils.first_and_only_and_str(ren_el)


def _handle_slh_word(hctx, tmpl):
    assert wtp.template_len(tmpl) == 6
    targ_renseq = wt_help.render_tmpl_el(hctx, tmpl, wtp.SLHW_ARG_IDX_FOR_TARG)
    if wt_help.get_renopt(hctx, 'ro_no_slh_word'):
        return targ_renseq
    kais = (  # kai: key and index
        ('slhw-desc-0', wtp.SLHW_ARG_IDX_FOR_DESC0),
        ('slhw-desc-1', wtp.SLHW_ARG_IDX_FOR_DESC1),
        ('slhw-desc-2', wtp.SLHW_ARG_IDX_FOR_DESC2),
        ('slhw-desc-3', wtp.SLHW_ARG_IDX_FOR_DESC3)
    )
    attr = {kai[0]: _ren_to_str(hctx, tmpl, kai[1]) for kai in kais}
    return renel.mk_ren_el_tca('slh-word', targ_renseq, attr)


_THSP = renel.mk_ren_el_t('ren-tag-thin-space')
_NBSP = renel.mk_ren_el_t('ren-tag-no-break-space')


def _handle_paseq(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    nbsp_dvl_sp = _NBSP, sd.DOUB_VERT_LINE + ' '
    return _abstract_default(
        hctx, 'ro_legpas_style', renel.mk_ren_el_t('lp-paseq'), nbsp_dvl_sp)


def _handle_legarmeih_2(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _legarmeih_core(hctx)


def _legarmeih_core(hctx):
    ren_el_abst = renel.mk_ren_el_t('lp-legarmeih')
    thin_pas = _THSP, hpu.PAS
    return _abstract_default(
        hctx, 'ro_legpas_style', (ren_el_abst,), thin_pas)


def _handle_gray_maqaf(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _abstract_default(
        hctx, 'ro_implicit_maqaf_style',
        renel.mk_ren_el_t('implicit-maqaf'),
        renel.mk_ren_el_tc('mam-implicit-maqaf', hpu.MAQ))


def _handle_dualcant(hctx, tmpl):
    assert wtp.template_len(tmpl) == 4
    # {{מ:כפול|כפול=גגג|א=דדד|ב=ההה}}
    rv_cant = wt_help.get_renopt(hctx, 'ro_cantillation') or 'rv-cant-dual'
    all_3_cant_dab_values = 'rv-cant-dual', 'rv-cant-alef', 'rv-cant-bet'
    if rv_cant == 'rv-cant-all-three':
        cant_ren_els = tuple(
            _ren_el_for_cant(hctx, tmpl, cant_dab)
            for cant_dab in all_3_cant_dab_values)
        cant_ren_els_cont = _contents(cant_ren_els)
        if _equal(cant_ren_els_cont):
            return cant_ren_els_cont[0]
        return renel.mk_ren_el_tc('cant-all-three', cant_ren_els)
    assert rv_cant in all_3_cant_dab_values
    ren_el = _ren_el_for_cant(hctx, tmpl, rv_cant)
    return ren_el['contents']


def _contents(ren_els):
    return tuple(map(renel.get_ren_el_contents, ren_els))


def _equal(seq):
    if seq[0] != seq[1]:
        return False
    if len(seq) > 2:
        return _equal(seq[1:])
    return True


def _ren_el_for_cant(hctx, tmpl, cant_dab):
    el_idx, argname, cant_tag = _DUALCANT_ARG_HELPER_DIC[cant_dab]
    rendered_cant = wt_help.render_named_tmpl_el(hctx, tmpl, el_idx, argname)
    return renel.mk_ren_el_tc(cant_tag, rendered_cant)


def _doc_lemma_subhandler(hctx: wt_help.Hctx, doc_target_wtseq):
    # XXX Above, would it be better to return something like '{רווח}'?
    # See https://github.com/bdenckla/MAM-for-Acc/issues/33.
    if doc_lemma := _map_doc_target_to_doc_lemma(doc_target_wtseq):
        return doc_lemma
    tmp_hctx = hctx.mk_new_with_handler(_DOC_LEMMA_HANDLERS)
    doc_lemma = wt_help.render_wtseq(tmp_hctx, doc_target_wtseq)
    assert doc_lemma and doc_lemma != (' ',)
    assert not spacing.general_endswith(doc_lemma[-1], ' ')
    return doc_lemma


def _map_doc_target_to_doc_lemma(doc_target_wtseq):
    if len(doc_target_wtseq) != 1:
        return None
    if wtp.is_template(doc_target_wtseq[0]):
        el1_00 = wtp.template_i0(doc_target_wtseq[0], 0)
        if remap := doc_utils.LEMMA_FROM_TMPL.get(el1_00):
            return remap
    elif isinstance(doc_target_wtseq[0], str):
        if remap := doc_utils.LEMMA_FROM_STR.get(doc_target_wtseq[0]):
            return remap
    return None


def _handle_kq_trivial_qere(hctx, tmpl):
    """ Handle a ketiv/qere that is trivial (contains only qere). """
    assert wtp.template_len(tmpl) in (2, 3)
    # XXX For now we ignore the 2nd arg (3rd el), if it exists.
    # (It exists in all but 5 cases.)
    qere = wt_help.render_tmpl_el(hctx, tmpl, 1)
    return renel.mk_ren_el_tc('mam-kq-trivial', qere)


def _handle_kq_qere_velo_ketiv(hctx, tmpl):
    """ Handle a qere velo ketiv. """
    assert wtp.template_len(tmpl) == 2
    # letters already square-bracketed in source; maqaf outside brackets
    qere = wt_help.render_tmpl_el(hctx, tmpl, 1)
    qere_nsb = _maybe_rm_punc_fr_q_velo_k(hctx, qere)
    return (renel.mk_ren_el_tc('mam-kq-q-velo-k', qere_nsb),)


def _maybe_rm_punc_fr_q_velo_k(hctx, wtseq):
    wtel = my_utils.first_and_only(wtseq)
    isinstance(wtel, str)
    nsb = wt_help.get_renopt(hctx, 'ro_q_velo_k_style') == 'rv-no-sqbrac'
    out_str = _strip_sqbrac(wtel) if nsb else wtel
    return (out_str,)


def _strip_sqbrac(string):
    return wt_help.strip_brackets_of_some_kind('[]', string)


def _doc_parts_subhandler(hctx: wt_help.Hctx, doc_parts_wtseqs):
    tmp_hctx = hctx.mk_new_with_handler(_DOC_PARTS_HANDLERS)
    return my_utils.st_map((wt_help.render_wtseq, tmp_hctx), doc_parts_wtseqs)


def _handle_samekh2_in_c(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'samekh2', in_c=True)


def _handle_samekh2_in_e(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'samekh2')


def _is_nu10_35_or_36(hctx: wt_help.Hctx):
    return my_versification.is_nu10_35_or_36(hctx.bcvt)


def _handle_samekh3_in_c(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'samekh3', in_c=True)


def _handle_samekh3_in_e(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    if _is_nu10_35_or_36(hctx):
        return _abstract_default(
            hctx, 'ro_samekh3_nu10_invnun_neighbor_style',
            renel.mk_ren_el_t('spi-samekh3-nu10-invnun-neighbor'),
            _NBSP)
    return _render_sampe(hctx, 'samekh3')


def _handle_pe2_in_c(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'pe2', in_c=True)


def _handle_pe2_in_e(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'pe2')


def _handle_pe3_in_c(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'pe3', in_c=True)


def _handle_pe3_in_e(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _render_sampe(hctx, 'pe3')


def _render_sampe(hctx, sampe, in_c=False):
    tag_abst = {
        'samekh2': 'spi-samekh2',
        'samekh3': 'spi-samekh3',
        'pe2': 'spi-pe2',
        'pe3': 'spi-pe3',
    }
    return _abstract_default(
        hctx, 'ro_sampe_style',
        renel.mk_ren_el_t(tag_abst[sampe]),
        _render_sampe_default(sampe, in_c))


def _sampe_dic2_el(sp1val):
    he_sam_or_he_pe, tag_defa, postwh = sp1val
    core = '{' + he_sam_or_he_pe + '}'
    ren_el_defa = renel.mk_ren_el_tc(tag_defa, core)
    return ren_el_defa, postwh

_REN_EL_BR_AFTER_PE = renel.mk_ren_el_t('mam-br-after-pe')
_REN_EL_OCTO_SPACE = renel.mk_ren_el_t('ren-tag-octo-space')
_SAMPE_DIC = {
    'samekh2': (hl.SAMEKH, 'mam-spi-samekh', _REN_EL_OCTO_SPACE),
    'samekh3': (hl.SAMEKH, 'mam-spi-samekh', _REN_EL_OCTO_SPACE),
    'pe2': (hl.PE, 'mam-spi-pe', _REN_EL_BR_AFTER_PE),
    'pe3': (hl.PE, 'mam-spi-pe', _REN_EL_BR_AFTER_PE)
}
_SAMPE_DIC2 = {
    sampe: _sampe_dic2_el(sp1val)
    for sampe, sp1val in _SAMPE_DIC.items()}


def _render_sampe_default(sampe, in_c):
    ren_el_defa, whitespace = _SAMPE_DIC2[sampe]
    if in_c:
        return ren_el_defa
    return ' ', ren_el_defa, whitespace


def _handle_large_letter(hctx, tmpl):
    return _slh_letter_subhandler('large', hctx, tmpl)


def _handle_small_letter(hctx, tmpl):
    return _slh_letter_subhandler('small', hctx, tmpl)


def _handle_hung_letter(hctx, tmpl):  # aka raised or suspended
    return _slh_letter_subhandler('hung', hctx, tmpl)


def _slh_letter_subhandler(slh_type, hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)  # e.g. ('בְּ',)
    if wt_help.get_renopt(hctx, 'ro_no_formatting_for_slh'):
        return inner_handled
    type_to_tag = {
        'small': 'mam-letter-small',
        'large': 'mam-letter-large',
        'hung': 'mam-letter-hung'
    }
    return renel.mk_ren_el_tc(type_to_tag[slh_type], inner_handled)


def _handle_poetic_space_resh0123(_hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return ' '


def _handle_shirah_space(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _abstract_default(
        hctx,
        'ro_shirah_space_style',
        renel.mk_ren_el_t('shirah-space'),
        sd.OCTO_NBSP)


def _handle_inverted_nun(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    t10 = wtp.template_i0(tmpl, 1)
    add_tr_space = t10 == hpu.NUN_HAF + '__'
    assert add_tr_space or t10 == hpu.NUN_HAF
    if not add_tr_space:
        assert _is_nu10_35_or_36(hctx)
    maybe_nbsp = _NBSP if add_tr_space else ''
    ren_el_defa = renel.mk_ren_el_tc('mam-spi-invnun', hpu.NUN_HAF)
    defa_maybe_nbsp = ren_el_defa, maybe_nbsp
    return _abstract_default(
        hctx, 'ro_nun_haf_style',
        _ren_el_abst_for_inverted_nun(add_tr_space),
        defa_maybe_nbsp)


def _abstract_default(hctx, ro_key, abst, defa):
    style = wt_help.get_renopt(hctx, ro_key)
    dic = {'abstract': abst, None: defa}
    return dic[style]


def _ren_el_abst_for_inverted_nun(add_tr_space):
    tagmap = {
        True: 'spi-invnun-including-trailing-space',
        False: 'spi-invnun'}
    return renel.mk_ren_el_t(tagmap[add_tr_space])


def _handle_wikitext_str(hctx, string):
    if wt_help.get_renopt(hctx, 'ro_no_varika'):
        return string.translate(hpo.DROP_VARIKA)
    return string


def _handle_wikitext_str_in_doc_part(_hctx, string):
    return my_use_true_gershayim.in_str(string)


def _handle_good_ending_in_body(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)
    the_ren_el_c = renel.mk_ren_el_tc('mam-good-ending', inner_handled)
    style = wt_help.get_renopt(hctx, 'ro_good_ending_style')
    if style == 'rv-no-br':
        return the_ren_el_c
    assert style is None  # i.e., the default style
    br_before_good_ending = renel.mk_ren_el_t('mam-br-before-good-ending')
    return br_before_good_ending, the_ren_el_c


def _handle_good_ending_in_doc_lemma(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)
    ih0 = my_utils.first_and_only_and_str(inner_handled)
    words = ih0.split(' ')
    abbrev = words[0] + ' ... ' + words[-1]
    return (abbrev,)


_MASK_E = 'e'  # cell E
_MASK_C = 'c'  # cell C
_MASK_L = 'l'  # doc lemma
_MASK_P = 'p'  # doc part
_MASK_EC = 'ec'
_MASK_EL = 'el'
_MASK_ECL = 'ecl'
_MASK_ELP = 'elp'
_HANDLER_SPECS_FOR_KETIV_QERE = {
    'כו"ק': {_MASK_EL: kq.handle_kq_ketiv_qere},
    'קו"כ': {_MASK_EL: kq.handle_kq_qere_ketiv},
    tmpln.K1Q1_MCOM: {_MASK_EL: kq.handle_k1q1_mcom},
    tmpln.K1Q2_SR_KQQ: {_MASK_EL: kq.handle_k1q2_sr_kqq},
    tmpln.K1Q2_SR_QQK: {_MASK_EL: kq.handle_k1q2_sr_qqk},
    tmpln.K1Q2_SR_BCOM: {_MASK_EL: kq.handle_k1q2_sr_bcom},
    tmpln.K1Q2_WR_KQQ: {_MASK_EL: kq.handle_k1q2_wr_kqq},
    tmpln.K1Q2_UR_QQK: {_MASK_EL: kq.handle_k1q2_ur_qkk},
    tmpln.K2Q1: {_MASK_EL: kq.handle_k2q1},
    tmpln.K2Q2: {_MASK_EL: kq.handle_k2q2},
    'קו"כ-אם': {_MASK_EL: _handle_kq_trivial_qere},
    'קרי ולא כתיב': {_MASK_EL: _handle_kq_qere_velo_ketiv},
    'כתיב ולא קרי': {_MASK_EL: kq.handle_kq_ketiv_velo_qere},
}
_HANDLER_SPECS_FOR_WHITESPACE = {
    'ססס': {
        _MASK_C: _handle_samekh3_in_c,
        _MASK_E: _handle_samekh3_in_e},
    'סס': {
        _MASK_C: _handle_samekh2_in_c,
        _MASK_E: _handle_samekh2_in_e},
    'פפפ': {
        _MASK_C: _handle_pe3_in_c,
        _MASK_E: _handle_pe3_in_e},
    'פפ': {
        _MASK_C: _handle_pe2_in_c,
        _MASK_E: _handle_pe2_in_e},
    'ר4': {_MASK_C: _ignore},
    'ר3': {_MASK_E: _handle_poetic_space_resh0123},
    'ר2': {_MASK_E: _handle_poetic_space_resh0123},
    'ר1': {
        _MASK_EL: _handle_poetic_space_resh0123,
        _MASK_C: _ignore},
    'ר0': {_MASK_EL: _handle_poetic_space_resh0123},
    'מ:ששש': {_MASK_EC: _handle_shirah_space},
    tmpln.NO_PAR_AT_STA_OF_PRQ: {_MASK_C: _ignore},
    tmpln.NO_PAR_AT_STA_OF_PRQ_EMT: {_MASK_C: _ignore},
}
_HANDLER_SPECS_FOR_MISC = {
    str: {
        _MASK_ECL: _handle_wikitext_str,
        _MASK_P: _handle_wikitext_str_in_doc_part},
    '__': {_MASK_C: _ignore},
    'נוסח': {_MASK_EC: _handle_doc},
    'מ:הערה': {_MASK_EC: _ignore},
    tmpln.SCRDFFTAR: {_MASK_EC: _handle_scrdfftar},
    tmpln.SLH_WORD: {_MASK_ELP: _handle_slh_word},
    'מ:לגרמיה-2': {_MASK_ELP: _handle_legarmeih_2},
    'מ:פסק': {_MASK_ELP: _handle_paseq},
    'מ:מקף אפור': {_MASK_EL: _handle_gray_maqaf},
    'מ:קמץ': {_MASK_EL: qamats_variation.handle},
    'מ:אות-ק': {_MASK_ELP: _handle_small_letter},
    'מ:אות-ג': {_MASK_ELP: _handle_large_letter},
    'מ:אות תלויה': {_MASK_EL: _handle_hung_letter},
    'מ:נו"ן הפוכה': {_MASK_EL: _handle_inverted_nun},
    'מ:כפול': {_MASK_E: _handle_dualcant},
    'מ:סיום בטוב': {
        _MASK_E: _handle_good_ending_in_body,
        _MASK_L: _handle_good_ending_in_doc_lemma},
}
_HANDLER_SPECS = {
    **_HANDLER_SPECS_FOR_KETIV_QERE,
    **_HANDLER_SPECS_FOR_WHITESPACE,
    **_HANDLER_SPECS_FOR_MISC,
}
_GEN_WT_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, 'e')
_COL_C_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, 'c')
_DOC_PARTS_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, 'p')
_DOC_LEMMA_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, 'l')
_DUALCANT_ARG_HELPER_DIC = {
    'rv-cant-dual': (1, str('כפול'), 'cant-dual'),
    'rv-cant-alef': (2, str('א'), 'cant-alef'),
    'rv-cant-bet': (3, str('ב'), 'cant-bet'),
}
#######################################################################
# Notes on ignored templates:
#
# We ignore plain scrdff templates in favor of (synthesized)
# scrdfftar templates.
#
# resh1_in_colc happens only two times:
#    between verses 1 and 2 of Psalm 70 and
#    between verses 1 and 2 of Psalm 108.
#
# We ignore resh4, as we do '__'.
#
#######################################################################
#
# The כפול argument has the combined cantillation.
# The א argument has the cantillation known as
#     תחתון in the Decalogues and פשוטה in G35:22.
# The ב argument has the cantillation known as
#     עליון in the Decalogues and מדרשית in G35:22.
# I.e.:
#     In the Decalogues, א/ב is תחתון/עליון.
#     In G35:22,         א/ב is פשוטה/מדרשית.
#
#######################################################################
