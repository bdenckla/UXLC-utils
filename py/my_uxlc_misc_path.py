""" Exports get """

import os


def get(filename):
    """
    Returns basename.xml in UXLC-misc-fixed if it exists there,
    otherwise returns basename.xml in UXLC-misc.
    """
    path_fixed = f'in/UXLC-misc-fixed/{filename}'
    if os.path.exists(path_fixed):
        return path_fixed
    return f'in/UXLC-misc/{filename}'
