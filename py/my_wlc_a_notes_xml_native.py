""" Exports write_native_to_html. """

import my_html


def write_to_html(native, record):
    """ Write XML (represented as a native Python dict) to an HTML file. """
    rows = list(map(_make_key_value_row, native.items()))
    #
    body_contents = []
    if 'img' in record:
        body_contents.append(my_html.img({'src': record['img']}))
    body_contents.append(my_html.table(rows))
    ucp_n = int(native['n'])
    ucp_n_str_02 = f'{ucp_n:02d}'
    title = f'UXLC change proposal {ucp_n_str_02}'
    path = f'uxlc_change_proposal_{ucp_n_str_02}.html'
    write_ctx = my_html.WriteCtx(title, f'docs/{path}')
    my_html.write_html_to_file(body_contents, write_ctx)
    return path


def _make_key_value_row(kv_pair):
    key, value = kv_pair
    cell_for_key = my_html.table_datum(key)
    if key in ('reftext', 'changetext'):
        attr = {'lang': 'hbo', 'dir': 'rtl'}
    else:
        attr = None
    cell_for_value = my_html.table_datum(value, attr)
    return my_html.table_row([cell_for_key, cell_for_value])
