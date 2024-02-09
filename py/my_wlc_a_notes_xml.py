""" Exports write_xml. """

import xml.etree.ElementTree as ET
import my_open

def write_xml(records):
    """ Write records out in UXLC change proposal format. """
    dated_change_set_elem = ET.Element('date')  # dated change set
    date = ET.SubElement(dated_change_set_elem, 'date')  # date of this dated change set
    date.text = '2024.02.09'
    for i, _rec in enumerate(records):
        change = ET.SubElement(dated_change_set_elem, 'change')
        citation = ET.SubElement(change, 'citation')
        one_based_index_elem = ET.SubElement(citation, 'n')
        one_based_index_elem.text = str(i + 1)
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

