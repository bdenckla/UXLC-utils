""" Exports write_xml. """

import xml.etree.ElementTree as ET
import my_open
import my_uxlc
import my_uxlc_unicode_names
import my_convert_citation_from_wlc_to_uxlc
import my_uxlc_book_abbreviations as u_bk_abbr
import my_wlc_a_notes_xml_native as native
import my_wlc_a_notes_xml_etan as etan

def write(io_records):
    """ Write records out in UXLC change proposal format. """
    dated_change_set = ET.Element('date')
    ET.SubElement(dated_change_set, 'date').text = '2024.02.09'
    uxlc = {}
    for io_record in io_records:
        ucp_seq = io_record.get('uxlc-change-proposal-sequential')
        if ucp_seq is not None:
            change_elem = etan.top_elem(dated_change_set, 'change')
            _add_misc(uxlc, change_elem, io_record)
            io_record['path-to-ucp'] = native.write_to_html(change_elem['native'], io_record)
    dated_change_set_tree = ET.ElementTree(dated_change_set)
    #
    ET.indent(dated_change_set_tree)
    #
    xml_out_path = 'out/wlc_a_notes_changes.xml'
    my_open.with_tmp_openw(
        xml_out_path, {}, _etree_write_callback, dated_change_set_tree)


def _etree_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding='unicode')
    out_fp.write('\n')


def _add_misc(io_uxlc, change_elem, record):
    _add_n(change_elem, record)
    _add_citation(io_uxlc, change_elem, record)
    _add_author(change_elem)
    _add_description(change_elem, record)
    _add_lc(change_elem, record)
    _add_xtext_xuni(change_elem, record, 'reftext', 'refuni')
    _add_xtext_xuni(change_elem, record, 'changetext', 'changeuni')
    _add_notes(change_elem, record)
    _add_analysistags(change_elem, record)
    _add_transnotes(change_elem, record)
    _add_status(change_elem)
    _add_type(change_elem)


def _add_n(change_elem, record):
    ucp_seq = record['uxlc-change-proposal-sequential']
    etan.sub_elem_text(change_elem, 'n', str(ucp_seq))

def _add_citation(io_uxlc, change_elem, record):
    citation_elem = etan.sub_elem(change_elem, 'citation')
    #
    wlc_bcv_str = record['bcv']
    uxlc_bkid = my_convert_citation_from_wlc_to_uxlc.get_uxlc_bkid(wlc_bcv_str)
    chnu, vrnu = my_convert_citation_from_wlc_to_uxlc.get_cv_pair(wlc_bcv_str)
    index = _index(io_uxlc, _qere_atom(record), (uxlc_bkid, chnu, vrnu))
    position = index + 1
    #
    etan.sub_elem_text(citation_elem, 'book', uxlc_bkid)
    etan.sub_elem_text(citation_elem, 'c', str(chnu))
    etan.sub_elem_text(citation_elem, 'v', str(vrnu))
    etan.sub_elem_text(citation_elem, 'position', str(position))


def _index(io_uxlc, word, bcv):
    verse_words = _get_verse_words(io_uxlc, bcv)
    index = verse_words.index(word)
    assert index != -1
    return index


def _get_verse_words(io_uxlc, bcv):
    uxlc_bkid, chnu, vrnu = bcv
    if uxlc_bkid not in io_uxlc:
        std_bkid = u_bk_abbr.BKNA_MAP_UXLC_TO_STD[uxlc_bkid]
        io_uxlc[uxlc_bkid] = my_uxlc.read(std_bkid)
    chidx = chnu - 1
    vridx = vrnu - 1
    return io_uxlc[uxlc_bkid][chidx][vridx]


def _add_author(change_elem):
    author_elem = etan.sub_elem(change_elem, 'author')
    etan.sub_elem_text(author_elem, 'name', 'Ben Denckla')
    etan.sub_elem_text(author_elem, 'mail', 'bdenckla@alum.mit.edu')
    etan.sub_elem_text(author_elem, 'confirmed', 'true')


def _add_description(change_elem, record):
    reason = record['at issue English']
    desc = f'Note {reason}'
    etan.sub_elem_text(change_elem, 'description', desc)


def _add_lc(change_elem, record):
    lc_elem = etan.sub_elem(change_elem, 'lc')
    etan.sub_elem_text(lc_elem, 'folio', _fill_me_in(record, 'folio'))
    etan.sub_elem_text(lc_elem, 'column', _fill_me_in(record, 'column'))
    etan.sub_elem_text(lc_elem, 'line', _fill_me_in(record, 'line'))
    etan.sub_elem_text(lc_elem, 'credit', 'Credit: Sefaria.org.')


def _fill_me_in(record, key):
    if key in record:
        return str(record[key])
    return f'XXX fill me in {key}'


def _add_xtext_xuni(change_elem, record, xtext, xuni):
    qere_atom = _qere_atom(record)
    xuni_str = my_uxlc_unicode_names.names(qere_atom)
    etan.sub_elem_text(change_elem, xtext, qere_atom)
    etan.sub_elem_text(change_elem, xuni, xuni_str)


def _add_notes(change_elem, record):
    notes_elem = etan.sub_elem(change_elem, 'notes')
    if 'qere-atom' in record:
        fqere = record['qere']  # full qere
        fqere_note = f'The qere atom at issue is part of the qere compound {fqere}.'
        etan.sub_elem_text(notes_elem, 'note', fqere_note)
    mpk_note = _mpk_note_aued_for_dc(record['MPK'])
    etan.sub_elem_text(notes_elem, 'note', mpk_note)
    for remark in record['remarks']:
        etan.sub_elem_text(notes_elem, 'note', _aued_for_dc(remark))
    side_notes = record.get('side-notes') or []
    for side_note in side_notes:
        etan.sub_elem_text(notes_elem, 'note', _aued_for_dc(side_note))

_AUED = 'א\N{HEBREW MARK UPPER DOT}'
_AUED_WITH_EXP = f'{_AUED} (א with an extraordinary upper dot)'


def _mpk_note_aued_for_dc(mpk):
    # use aued (alef with an extraordinary upper dot) instead of dc (dotted circle)
    mpk_aued = mpk.replace('\N{DOTTED CIRCLE}', _AUED)
    if _AUED in mpk_aued:
        exp = (
            f' (We use {_AUED_WITH_EXP} to stand in for a blank space.)'
        )
    else:
        exp = ''
    return f'The manuscript’s pointed ketiv (MPK) is {mpk_aued}.{exp}'


def _aued_for_dc(string):
    return string.replace('dotted circle', _AUED_WITH_EXP)


def _add_analysistags(change_elem, record):
    atags_elem = etan.sub_elem(change_elem, 'analysistags')
    # XXX fill me in analysistags


def _add_transnotes(change_elem, record):
    trnotes_elem = etan.sub_elem(change_elem, 'transnotes')
    trnote_elem = etan.sub_elem(trnotes_elem, 'transnote')
    etan.sub_elem_text(trnote_elem, 'action', 'Add')
    etan.sub_elem_text(trnote_elem, 'type', 'a')
    etan.sub_elem_text(trnote_elem, 'beforetext', 'XXX fill me in beforetext')  # XXX


def _add_status(change_elem):
    etan.sub_elem_text(change_elem, 'status', 'Pending')

def _add_type(change_elem):
    etan.sub_elem_text(change_elem, 'type', 'NoTextChange')


def _qere_atom(record):
    return record.get('qere-atom') or record['qere']

# <n>1</n>
# <citation>
#     <book>Dan</book>
#     <c>2</c>
#     <v>16</v>
#     <position>8</position>
# </citation>
# <author>
#     <name>Daniel Holman</name>
#     <mail>daniel.holman@mail.com</mail>
#     <confirmed>true</confirmed>
# </author>
# <description>Note possible dagesh in the first nun and weak dot in tsere under the tav.  Add note 't'.</description>
# <lc>
#     <folio>Folio_438B</folio>
#     <column>2</column>
#     <line>24</line>
#     <credit>Credit: Sefaria.org.</credit>
# </lc>
# <reftext>יִנְתֵּן־</reftext>
# <refuni>yod     hiriq     nun     sheva     tav     dagesh     tsere     final-nun     maqaf     </refuni>
# <changetext>יִנְתֵּן־</changetext>
# <changeuni>yod     hiriq     nun     sheva     tav     dagesh     tsere     final-nun     maqaf     </changeuni>
# <notes>
#     <note>The text is in good condition near this word. A reddish blob appears in nun; it is poorly formed and ill-positioned, compared to the dagesh in the tav. The blob will not be transcribed as a dagesh. The leading dot in the tsere under the tav is reddish and small but well-formed and well positioned. It will remain a tsere.</note>
#     <note>BHL has no dagesh in the nun and a tsere under the tav.  BHLA has no entry for this verse.</note>
# </notes>
# <analysistags>
#     <aBHL/>
# </analysistags>
# <transnotes>
#     <transnote>
#         <action>Add</action>
#         <type>t</type>
#         <beforetext>יִנְ</beforetext>
#     </transnote>
# </transnotes>
# <status>Pending</status>
# <type>NoTextChange</type>
