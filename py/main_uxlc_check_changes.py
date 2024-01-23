""" Exports main """

import xml.etree.ElementTree
import my_uxlc
import my_uxlc_misc_path
import my_uxlc_bhl_appendix_a
import my_tanakh_book_names as tbn
import my_uxlc_page_break_info as page_break_info
import my_uxlc_changes_loc as changes_loc
import my_uxlc_lci_augrec as lci_augrec
import my_uxlc_lci_rec_to_xml as lci_rec_to_xml
import my_uxlc_change_prep as prep
import my_uxlc_changes
import my_open
import my_xml_node


def _listify(list_or_nonlist):
    if isinstance(list_or_nonlist, list):
        return list_or_nonlist
    return [list_or_nonlist]


def _get_changes(changeset):
    date = changeset['date']
    if 'change' not in changeset:
        # Sometimes a changeset just has a date, because it is an empty
        # placeholder, to be filled in with changes later.
        return []
    changes = _listify(changeset['change'])
    return [prep.date_qualify_and_reformat(date, c) for c in changes]


def _get_lines(change):
    return [change['description']] + change['notes']


def _dump_txt_write_callback(lines, out_fp):
    out_fp.write('\n'.join(lines))


def _dump_txt(changes, path):
    list_of_lists = list(map(_get_lines, changes))
    lines = sum(list_of_lists, [])
    my_open.with_tmp_openw(path, {}, _dump_txt_write_callback, lines)


def _do_one_changes_file(bhla, filename):
    release_date, changes = _do_one_changes_file_core(filename)
    changes = [{'release': release_date, **c} for c in changes]
    changes = [{'bhla': _join_bhla(bhla, c), **c} for c in changes]
    return changes


def _do_one_changes_file_core(filename):
    """
    Convert a Changes file to JSON format. (E.g., for import into Excel).
    """
    xml_input_path = my_uxlc_misc_path.get(filename)
    tree = xml.etree.ElementTree.parse(xml_input_path)
    root = tree.getroot()
    root_dic = my_xml_node.to_dic(root)
    # release_major_dot_minor = root_dic['target']  # E.g. 'UXLC 1.2'
    release_date = root_dic['filedate']
    changesets_list = _listify(root_dic['dates']['date'])
    list_of_lists = list(map(_get_changes, changesets_list))
    changes = sum(list_of_lists, [])
    basename = filename.removesuffix('.xml')
    assert basename != filename
    txt_output_path = f'out/UXLC-misc/{basename}.txt'
    _dump_txt(changes, txt_output_path)
    return release_date, changes


def _join_bhla(bhla, change_record):
    citation = change_record['citation']
    if citation in bhla:
        return True
    cite_sod = citation.split('.')   # sod: split on dot
    return cite_sod[0] in bhla


def _get_all_changes():
    bhla = my_uxlc_bhl_appendix_a.read()
    all_changes = []
    for filename in my_uxlc_changes.FILENAMES:
        changes = _do_one_changes_file(bhla, filename)
        all_changes.extend(changes)
    return all_changes


def _get_uxlc():
    return {bkid: my_uxlc.read(bkid) for bkid in tbn.ALL_BOOK_IDS}


def _write_page_break_info(pbi):
    lciars = page_break_info.get_lci_augrecs(pbi)
    lciars_f = lci_augrec.flatten_many2(lciars)
    json_output_path1 = 'out/UXLC-misc/lci_augrecs.json'
    my_open.json_dump_to_file_path(lciars_f, json_output_path1)
    #
    pg_lens = page_break_info.get_page_lengths(pbi)
    pg_lens_f = lci_augrec.flatten_page_lengths(pg_lens)
    json_output_path2 = 'out/UXLC-misc/page_counts.json'
    my_open.json_dump_to_file_path(pg_lens_f, json_output_path2)
    #
    lci_recs_dot_json = page_break_info.read_lci_recs_dot_json()
    xml_elementtree = lci_rec_to_xml.get_etree(lci_recs_dot_json)

    xml_out_path = 'out/UXLC-misc/lci_recs.xml'
    my_open.with_tmp_openw(
        xml_out_path, {}, _pbi_write_callback, xml_elementtree)


def _pbi_write_callback(xml_elementtree, out_fp):
    xml_elementtree.write(out_fp, encoding='unicode')
    out_fp.write('\n')


def main():
    """
    Convert various Changes files to JSON format.
    """
    uxlc = _get_uxlc()
    pbi = page_break_info.read_in(uxlc)
    changes = _get_all_changes()
    check_results_f = changes_loc.check(uxlc, pbi, changes)
    #
    json_output_path1 = 'out/UXLC-misc/all_changes.json'
    my_open.json_dump_to_file_path(changes, json_output_path1)
    json_output_path2 = 'out/UXLC-misc/all_changes_loc_checks.json'
    my_open.json_dump_to_file_path(check_results_f, json_output_path2)
    _write_page_break_info(pbi)


if __name__ == "__main__":
    main()
