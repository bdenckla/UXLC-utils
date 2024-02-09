""" Exports write_xml. """

import xml.etree.ElementTree as ET
import my_open
import my_convert_citation_from_wlc_to_uxlc

def write_xml(records):
    """ Write records out in UXLC change proposal format. """
    dated_change_set_elem = ET.Element('date')  # dated change set
    date_elem = ET.SubElement(dated_change_set_elem, 'date')  # date of this dated change set
    date_elem.text = '2024.02.09'
    for i, record in enumerate(records):
        change_elem = ET.SubElement(dated_change_set_elem, 'change')
        one_based_index_elem = ET.SubElement(change_elem, 'n')
        one_based_index_elem.text = str(i + 1)
        _add_citation(change_elem, record)
    #
    dated_change_set_tree = ET.ElementTree(dated_change_set_elem)
    ET.indent(dated_change_set_tree)
    #
    xml_out_path = 'out/wlc_a_notes_changes.xml'
    my_open.with_tmp_openw(
        xml_out_path, {}, _etree_write_callback, dated_change_set_tree)


def _etree_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding='unicode')
    out_fp.write('\n')


def _add_citation(change_elem, record):
    citation_elem = ET.SubElement(change_elem, 'citation')
    book_elem = ET.SubElement(citation_elem, 'book')
    wlc_bcv_str = record['bcv']
    book_elem.text = my_convert_citation_from_wlc_to_uxlc.get_uxlc_bkid(wlc_bcv_str)
    chap_elem = ET.SubElement(citation_elem, 'c')
    verse_elem = ET.SubElement(citation_elem, 'v')



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

