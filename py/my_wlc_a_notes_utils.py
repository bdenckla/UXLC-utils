""" Exports side_note_string. """


def side_note_string(side_note):
    if isinstance(side_note, dict):
        assert list(side_note.keys()) == ['sn-blockquote']
        return side_note['sn-blockquote']
    assert isinstance(side_note, str)
    return side_note
