import py_misc.my_html as my_html


def rmn(string):
    return my_html.span(string, {"class": "romanized"})
