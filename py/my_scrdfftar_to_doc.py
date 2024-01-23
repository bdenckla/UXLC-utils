""" Exports scrdfftar_to_doc """
import my_mam_wiki_tmpl2 as wtp
import my_template_names as tmpln
import my_use_true_gershayim


def convert(wtseq):  # wt: Wikitext
    """
    For each scrdfftar at the top level of wtseq,
    turn that scrdfftar into a doc.

    For each doc at the top level of wtseq,
    if that doc's target is a scrdfftar,
    fold that scrdfftar's contents into the doc.

    Also, remove any scrdff from the top level of wtseq.

    We only care about top level because other code
    recurses and ends up calling this again at lower
    levels.
    """
    wtseq_type = type(wtseq)
    wtseq_f = wtseq_type(filter(_is_not_scrdff, wtseq))
    return wtseq_type(map(_handle, wtseq_f))


def _handle(wtel):
    if _is_scrdfftar_template(wtel):
        return _make_doc_tmpl(wtel, [])
    if _is_doc_of_scrdfftar(wtel):
        return _handle_doc_of_scrdfftar(wtel)
    return wtel


def _make_doc_tmpl(scrdfftar, existing_doc_parts):
    scrdfftar_targ = wtp.template_element(scrdfftar, wtp.SDT_ARG_IDX_FOR_TARG)
    scrdfftar_note = wtp.template_element(scrdfftar, wtp.SDT_ARG_IDX_FOR_NOTE)
    # In this context, we don't care about starpos
    new_doc_tmpl_els = [['נוסח'], scrdfftar_targ]
    new_doc_tmpl_els.append(_tweak_sdt_text(scrdfftar_note))
    new_doc_tmpl_els.extend(existing_doc_parts)
    return wtp.mktmpl(new_doc_tmpl_els)


def _tweak_sdt_text(scrdfftar_text):
    return _add_provenance(my_use_true_gershayim.in_seq(scrdfftar_text))


def _handle_doc_of_scrdfftar(doc_tmpl):
    # Turn this:
    #     doc(
    #         [scrdfftar(scrdfftar_targ, scrdfftar_text)],
    #         doc_part1,
    #         doc_part2, ...)
    # into this:
    #     doc(
    #         scrdfftar_targ,
    #         scrdfftar_text,
    #         doc_part1,
    #         doc_part2, ...)
    # or this, if scrdfftar_text is redundant with what's already expressed
    # in the doc parts:
    #     doc(
    #         scrdfftar_targ,
    #         doc_part1,
    #         doc_part2, ...)
    doc_tmpl_els = wtp.template_elements(doc_tmpl)
    scrdfftar = doc_tmpl_els[1][0]
    return _make_doc_tmpl(scrdfftar, doc_tmpl_els[2:])


def _is_not_scrdff(wtel):
    return not wtp.is_scrdff_template(wtel)


def _is_doc_of_scrdfftar(wtel):
    if not wtp.is_doc_template(wtel):
        return False
    doc1 = wtp.template_element(wtel, 1)
    return (
        len(doc1) == 1 and _is_scrdfftar_template(doc1[0]))


def _is_scrdfftar_template(wtel):
    return wtp.is_template_with_name(wtel, tmpln.SCRDFFTAR)


def _add_provenance(scrdfftar_text):
    assert isinstance(scrdfftar_text[0], str)
    new_scrdfftar_text_0 = '(מ:הערה) ' + scrdfftar_text[0]
    return [new_scrdfftar_text_0, *scrdfftar_text[1:]]
