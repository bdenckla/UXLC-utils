""" Exports various ren_el constructors & getters. """


def mk_ren_el_t(tag: str):
    """
    Return a render element with only a tag (no contents).
    """
    return {'_ren_tag': tag}


def mk_ren_el_tc(tag, contents):
    """
    Return a render element with contents.
    """
    if isinstance(contents, str):
        contents_tuple = (contents,)
    else:
        assert isinstance(contents, tuple)
        contents_tuple = contents
    return {**mk_ren_el_t(tag), 'contents': contents_tuple}


def mk_ren_el_tca(tag, contents, attr):
    """
    Return a render element with contents and attributes.
    """
    return {**mk_ren_el_tc(tag, contents), 'attr': attr}


def mk_ren_el_tcd(tag, contents, doc_lemma, doc_parts):
    """
    Return a render element with contents, a doc lemma, and doc parts.
    """
    return {
        **mk_ren_el_tc(tag, contents),
        'doc_lemma': doc_lemma,
        'doc_parts': doc_parts
    }


def get_ren_el_tag(ren_el):
    """ Return the tag of ren_el. """
    return ren_el['_ren_tag']


def get_ren_el_tc(ren_el):
    """ Return the tag and contents of ren_el. """
    return get_ren_el_tag(ren_el), ren_el['contents']


def get_ren_el_contents(ren_el):
    """ Return contents if they exist. """
    return ren_el.get('contents')


def get_ren_el_attr(ren_el):
    """ Return attributes if they exist. """
    return ren_el.get('attr')


def ren_el_is_t_only(ren_el):
    """ Return whether the ren_el has only a tag. """
    return tuple(ren_el.keys()) == ('_ren_tag',)


def obj_is_ren_el(obj):
    """ Return whether obj is a ren_el. """
    return isinstance(obj, dict) and '_ren_tag' in tuple(obj.keys())
