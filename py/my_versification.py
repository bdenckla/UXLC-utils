"""
This module exports:
    get_cvm_rec_from_bcvt(bcvt)
    cvm_rec_get_parts(cvm_rec)
    convert_from_mam(bkids, books_mpp, vtrad)
    is_nu10_35_or_36(bcvt)
"""


import my_utils
import my_tanakh_book_names as tbn
import my_mam_wiki_tmpl2 as wtp
import my_template_names as tmpln
import my_versification_helpers as helpers
import my_versification_data
import my_mam_in as mi


def get_cvm_rec_from_bcvt(bcvt):
    """ Get a cvm_rec from an a bcvt in any vtrad """
    vtrad = tbn.bcvt_get_vtrad(bcvt)
    return _DIC_FROM_BCVT_TO_CVM_REC[vtrad].get(bcvt)


def cvm_rec_get_parts(cvm_rec):
    """ Extract the type and cvm part of a cvm_rec. """
    return cvm_rec['_cvm_rec']


def convert_from_mam(bkids, books_mpp, vtrad):
    """
    1. Expand the set of book IDs to include "next" books.
    2. For each book in "books" whose ID is in that expanded set of book
       IDs, return the equivalent of that book in the given vtrad.
    """
    ebkids = tbn.add_part2_bkids(bkids)
    return {b: _convert_book(b, books_mpp[b], vtrad) for b in ebkids}


def is_nu10_35_or_36(bcvt):
    """ Return whether bcvt is Numbers 10:35 or 10:36 """
    vtrad = tbn.bcvt_get_vtrad(bcvt)
    out = bcvt in (tbn.nu10(35, vtrad), tbn.nu10(36, vtrad))
    if out:
        assert _is_same_in_tmam(bcvt)
    return out


# bcvtmam: a 4-element tuple consisting of:
#     bkid: tbn book ID
#     chnu: chapter number
#     vrnu: verse number
#     vtrad: expected to be tbn.VT_MAM


def _identity(bcvtmam, vtrad):
    chnu = tbn.bcvt_get_chnu(bcvtmam)
    vrnu = tbn.bcvt_get_vrnu(bcvtmam)
    cvtxxx = tbn.mk_cvt(chnu, vrnu, vtrad)
    return helpers.mk_maprec_1_to_1(cvtxxx)


def _get_minirows(bcvtmam, mam_minirow, vtrad):
    """
    Possibly split up mam_minirow into multiple minirows appropriate for
    the versification.
    """
    if saf_fun := _SPLITTERS_AND_FRIENDS[vtrad].get(bcvtmam):
        return saf_fun(mam_minirow)
    return (mam_minirow,)


def _convert_book(bkid, book_mpp, vtrad):
    xxx_verses = {}
    for cvtmam, mam_minirow in book_mpp['verses'].items():
        bcvtmam = tbn.mk_bcvt(bkid, cvtmam)
        maprec = _get_maprec(bcvtmam, vtrad)
        xxx_minirows = _get_minirows(bcvtmam, mam_minirow, vtrad)
        for cvve, xxx_minirow in my_utils.szip(maprec, xxx_minirows):
            cvtxxx = helpers.cvve_get_cvv(cvve)
            assert cvtxxx not in xxx_verses
            xxx_verses[cvtxxx] = xxx_minirow
    out_book = dict(book_mpp)
    out_book['good_ending'] = _convert_ge(book_mpp['good_ending'], bkid, vtrad)
    out_book['verses'] = xxx_verses
    return out_book


def _convert_ge(good_ending, bkid, vtrad):
    if good_ending is None:
        return None
    out_ge = dict(good_ending)
    cvtmam = good_ending['last_chapnver']
    bcvtmam = tbn.mk_bcvt(bkid, cvtmam)
    maprec = _get_maprec(bcvtmam, vtrad)
    cvve = my_utils.first_and_only(maprec)
    out_ge['last_chapnver'] = helpers.cvve_get_cvv(cvve)
    return out_ge


def _one_to_many_v01decalogue(mam_minirow):
    # v01decalogue: verse 1 of a Decalogue (E 20:2 or D 5:6)
    mra_cde = mam_minirow.CP, None, (mam_minirow.EP[0],)
    assert mam_minirow.EP[1] == ' '
    mrb_cde = None, None, (mam_minirow.EP[2],)
    assert len(mam_minirow.EP) == 3
    assert isinstance(mam_minirow, mi.MinirowExt)
    mra = mi.MinirowExt(*mra_cde, tuple())
    mrb = mi.MinirowExt(*mrb_cde, mam_minirow.next_CP)
    return mra, mrb


def _one_to_many_v11decalogue(mam_minirow):
    # v11decalogue: verse 11 of a Decalogue (E 20:12 or D 5:16)
    mr0_e = (mam_minirow.EP[0],)  # Minirow 0, column E
    #
    mr1_c = (mam_minirow.EP[1],)  # Minirow 1, column c
    mr1_e = (mam_minirow.EP[2],)  # Minirow 1, column e
    #
    mr2_c = (mam_minirow.EP[3],)  # Minirow 2, column c
    mr2_e = (mam_minirow.EP[4],)  # Minirow 2, column e
    #
    mr3_c = (mam_minirow.EP[5],)  # Minirow 3, column c
    mr3_e = (mam_minirow.EP[6],)  # Minirow 3, column e
    assert len(mam_minirow.EP) == 7
    assert isinstance(mam_minirow, mi.MinirowExt)
    mr0 = mi.MinirowExt(mam_minirow.CP, None, mr0_e, mr1_c)
    mr1 = mi.MinirowExt(mr1_c, None, mr1_e, mr2_c)
    mr2 = mi.MinirowExt(mr2_c, None, mr2_e, mr3_c)
    mr3 = mi.MinirowExt(mr3_c, None, mr3_e, mam_minirow.next_CP)
    return mr0, mr1, mr2, mr3


def _one_to_many_joshua_21_35(mam_minirow):
    return mam_minirow, None, None


def _one_to_one_numbers_25_18(mam_minirow):
    assert isinstance(mam_minirow, mi.MinirowExt)
    tmpl = wtp.mktmpl([[tmpln.NO_PAR_AT_STA_OF_PRQ]])
    assert mam_minirow.next_CP == (tmpl,)
    mra = mi.MinirowExt(
        mam_minirow.CP,
        mam_minirow.DP,
        mam_minirow.EP,
        tuple())
    return (mra,)


def _one_to_many_numbers_26_1(mam_minirow):
    tmpl = wtp.mktmpl([[tmpln.NO_PAR_AT_STA_OF_PRQ]])
    assert mam_minirow.CP == (tmpl,)
    mra_cde = None, None, (mam_minirow.EP[0],)
    ep1 = mam_minirow.EP[1]
    assert _is_doc_of_double_pe(ep1)
    double_pe = wtp.mktmpl([['פפ']])
    mrb_cde = (double_pe,), None, (mam_minirow.EP[2],)
    assert len(mam_minirow.EP) == 3
    assert isinstance(mam_minirow, mi.MinirowExt)
    mra = mi.MinirowExt(*mra_cde, mrb_cde[0])
    mrb = mi.MinirowExt(*mrb_cde, mam_minirow.next_CP)
    return mra, mrb


def _is_doc_of_double_pe(wtel):
    # Return whether wtel is doc(pp,...)
    # Or, (אאא added to address RTL issues):
    # אאא {{נוסח|{{פפ}}|...}} אאא
    if not wtp.is_template_with_name(wtel, 'נוסח'):
        return False
    doc_target = wtp.template_i0(wtel, 1)
    if not wtp.is_template_with_name(doc_target, 'פפ'):
        return False
    return True


_SPLITTERS_AND_FRIENDS_SEF = {
    my_versification_data.EXODUS_20_2_MAM: _one_to_many_v01decalogue,
    my_versification_data.DEUTER_5_6_MAM: _one_to_many_v01decalogue,
    my_versification_data.JOSHUA_21_35_MAM: _one_to_many_joshua_21_35,
}
_SPLITTERS_AND_FRIENDS_BHS = {
    **_SPLITTERS_AND_FRIENDS_SEF,
    my_versification_data.EXODUS_20_12_MAM: _one_to_many_v11decalogue,
    my_versification_data.NUMBERS_25_18_MAM: _one_to_one_numbers_25_18,
    my_versification_data.NUMBERS_26_1_MAM: _one_to_many_numbers_26_1,
    my_versification_data.DEUTER_5_16_MAM: _one_to_many_v11decalogue,
}
_SPLITTERS_AND_FRIENDS = {
    tbn.VT_SEF: _SPLITTERS_AND_FRIENDS_SEF,
    tbn.VT_BHS: _SPLITTERS_AND_FRIENDS_BHS,
}


def _mk_dic_from_bcvt_to_cvm_rec(vtrad):
    out = {}
    bcv_dic_from_mam_to_xxx = my_versification_data.BCV_DIC_FROM_MAM_TO_XXX[vtrad]
    for bcvtmam, maprec in bcv_dic_from_mam_to_xxx.items():
        bkid = tbn.bcvt_get_bkid(bcvtmam)
        for cvve_bhs in maprec:
            cvtbhs = helpers.cvve_get_cvv(cvve_bhs)
            cvve_type = helpers.cvve_get_type(cvve_bhs)
            bcvtbhs = tbn.mk_bcvt(bkid, cvtbhs)
            cvtmam = tbn.bcvt_get_cvt(bcvtmam)
            if cvve_type == helpers.CVVE_TYPE_SAME_CONTENTS:
                if tbn.eq_mod_vtrad(cvtbhs, cvtmam):
                    continue
            out[bcvtbhs] = helpers.cvm_rec_mk(cvve_type, cvtmam)
    return out


def _get_maprec(bcvtmam, vtrad):
    """
        Given bcvtmam (see comment above), returns a maprec.
        A maprec is tuple of pairs where those pairs consist of:
            a cvt
            a boolean telling whether that verse is empty
        (The "empty or not" boolean is only for Joshua 21:36 & 21:37.)
    """
    assert tbn.bcvt_is_tmam(bcvtmam)
    maprec = my_versification_data.BCV_DIC_FROM_MAM_TO_XXX[vtrad].get(bcvtmam)
    return maprec or _identity(bcvtmam, vtrad)


def _is_same_in_tmam(bcvt):
    """ Return whether bcvt is the same as in the MAM vtrad """
    vtrad = tbn.bcvt_get_vtrad(bcvt)  # extract just the vtrad
    if vtrad == tbn.VT_MAM:
        return True
    bcv_novt = tbn.bcvt_get_bcv_triple(bcvt)  # strip the vtrad off
    bcvtmam = tbn.mk_bcvtmam(*bcv_novt)  # add t=VT_MAM
    round_trip = _get_maprec(bcvtmam, vtrad)
    if len(round_trip) != 1:
        return False
    same = helpers.CVVE_TYPE_SAME_CONTENTS
    if helpers.cvve_get_type(round_trip[0]) != same:
        return False
    return helpers.cvve_get_cvv(round_trip[0]) == tbn.bcvt_get_cvt(bcvt)


_DIC_FROM_BCVT_TO_CVM_REC = {
    tbn.VT_SEF: _mk_dic_from_bcvt_to_cvm_rec(tbn.VT_SEF),
    tbn.VT_BHS: _mk_dic_from_bcvt_to_cvm_rec(tbn.VT_BHS),
}
