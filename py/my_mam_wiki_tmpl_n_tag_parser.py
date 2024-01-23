""" Exports parse """

import my_mam_wiki_tmpl_parser as tmpl_parser
import my_mam_wiki_tag_parser as tag_parser
import my_mam_wiki_tmpl_n_tag_unparser as unparser


def parse(string):
    """ Chain the template and tag parsers """
    parsed = tag_parser.parse(tmpl_parser.parse(string))
    unparsed = unparser.unparse(parsed)
    assert tmpl_parser.debold(string) == unparsed
    return parsed
