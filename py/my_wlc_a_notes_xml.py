""" Exports write_xml. """

import xml.etree.ElementTree as ET
import my_open
import my_convert_citation_from_wlc_to_uxlc
import my_uxlc_book_abbreviations as u_bk_abbr
import my_uxlc_unicode_names
import my_uxlc

def write(records):
    """ Write records out in UXLC change proposal format. """
    dated_change_set_elem = ET.Element('date')  # dated change set
    date_elem = ET.SubElement(dated_change_set_elem, 'date')  # date of this dated change set
    date_elem.text = '2024.02.09'
    ucp_count = 0
    uxlc = {}
    for record in records:
        ucp = record['uxlc-change-proposal']
        if isinstance(ucp, int):
            ucp_count += 1
            change_elem = ET.SubElement(dated_change_set_elem, 'change')
            _add_misc(uxlc, change_elem, record, ucp_count)
    dated_change_set_tree = ET.ElementTree(dated_change_set_elem)
    #
    ET.indent(dated_change_set_tree)
    #
    xml_out_path = 'out/wlc_a_notes_changes.xml'
    my_open.with_tmp_openw(
        xml_out_path, {}, _etree_write_callback, dated_change_set_tree)


def _etree_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding='unicode')
    out_fp.write('\n')


def _add_misc(io_uxlc, change_elem, record, ucp_count):
    _add_n(change_elem, ucp_count)
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


def _add_n(change_elem, ucp_count):
    assert isinstance(ucp_count, int)
    ET.SubElement(change_elem, 'n').text = str(ucp_count)

def _add_citation(io_uxlc, change_elem, record):
    citation_elem = ET.SubElement(change_elem, 'citation')
    #
    wlc_bcv_str = record['bcv']
    uxlc_bkid = my_convert_citation_from_wlc_to_uxlc.get_uxlc_bkid(wlc_bcv_str)
    chnu, vrnu = my_convert_citation_from_wlc_to_uxlc.get_cv_pair(wlc_bcv_str)
    index = _index(io_uxlc, _qere_atom(record), (uxlc_bkid, chnu, vrnu))
    position = index + 1
    #
    ET.SubElement(citation_elem, 'book').text = uxlc_bkid
    ET.SubElement(citation_elem, 'c').text = str(chnu)
    ET.SubElement(citation_elem, 'v').text = str(vrnu)
    ET.SubElement(citation_elem, 'position').text = str(position)


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
    author_elem = ET.SubElement(change_elem, 'author')
    ET.SubElement(author_elem, 'name').text = 'Ben Denckla'
    ET.SubElement(author_elem, 'mail').text = 'bdenckla@alum.mit.edu'
    ET.SubElement(author_elem, 'confirmed').text = 'true'


def _add_description(change_elem, record):
    summ_in = record['summary']
    atiss_in = record['at issue']
    summ_out = _SUMMARY_MAP[summ_in]
    atiss_key = summ_in, atiss_in
    atiss_out = _AT_ISSUE_MAP.get(atiss_key) or ''

    desc = f'Note {summ_out}{atiss_out}'
    # XXX expand description (make summary more readable)
    ET.SubElement(change_elem, 'description').text = desc


_AT_ISSUE_MAP = {
    ('+dgsh', 'בּ'): ' to bet',
    ('+dgsh', 'וָּ'): ' to vav-qamats',
    ('+dgsh', 'פּ'): ' to pe',
    ('+dgsh', 'יּ'): ' to yod',
    ('+dgsh', 'דּ'): ' to dalet',
    ('+dgsh', 'כּ'): ' to kaf',
    ('+mapiq', 'הּ'): ' to he',
    ('+dgsh', 'טּ'): ' to tet',
    ('+dgsh', 'לּ'): ' to lamed',
    ('+dgsh', 'צּ'): ' to tsadi',
    #
    ('+shrq dt', 'וּ…'): ' to initial vav',
    ('+ḥlm dt', 'וֹ'): ' to vav',
    ('+shva', 'ךְ'): ' to final form of kaf',
    ('ḥtf ptḥ to ptḥ', 'עַ'): ' under ayin',
    #
    ('-dgsh', 'מ'): ' from mem',
}


_SUMMARY_MAP = {
    'qbts to shrq': 'qubuts to shuruq',
    '+mqf': 'added maqaf',
    '+dgsh': 'added dagesh',
    '-dgsh': 'removed dagesh',
    '+mapiq': 'added mapiq',
    '+shrq dt': 'added shuruq dot',
    '+ḥlm dt': 'added ḥolam malei dot',
    '+shva': 'added sheva',
    'ḥtf ptḥ to ptḥ': 'ḥataf pataḥ to pataḥ'
}


def _add_lc(change_elem, _record):
    lc_elem = ET.SubElement(change_elem, 'lc')
    ET.SubElement(lc_elem, 'folio').text = 'XXX fill me in folio'  # XXX
    ET.SubElement(lc_elem, 'column').text = 'XXX fill me in column'  # XXX
    ET.SubElement(lc_elem, 'line').text = 'XXX fill me in line'  # XXX
    ET.SubElement(lc_elem, 'credit').text = 'Credit: Sefaria.org.'


def _add_xtext_xuni(change_elem, record, xtext, xuni):
    qere_atom = _qere_atom(record)
    xuni_str = my_uxlc_unicode_names.names(qere_atom)
    ET.SubElement(change_elem, xtext).text = qere_atom
    ET.SubElement(change_elem, xuni).text = xuni_str


def _add_notes(change_elem, record):
    notes_elem = ET.SubElement(change_elem, 'notes')
    for remark in record['remarks']:
        ET.SubElement(notes_elem, 'note').text = remark


def _add_analysistags(change_elem, record):
    atags_elem = ET.SubElement(change_elem, 'analysistags')
    # XXX fill me in


def _add_transnotes(change_elem, record):
    trnotes_elem = ET.SubElement(change_elem, 'transnotes')
    trnote_elem = ET.SubElement(trnotes_elem, 'transnote')
    ET.SubElement(trnote_elem, 'action').text = 'Add'
    ET.SubElement(trnote_elem, 'type').text = 'a'
    ET.SubElement(trnote_elem, 'beforetext').text = 'XXX fill me in beforetext'  # XXX


def _add_status(change_elem):
    ET.SubElement(change_elem, 'status').text = 'Pending'

def _add_type(change_elem):
    ET.SubElement(change_elem, 'type').text = 'NoTextChange'


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
