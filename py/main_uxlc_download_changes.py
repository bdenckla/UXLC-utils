"""
    Base Usage:
    ./py/venv/Scripts/python.exe ./py/main_uxlc_download_changes.py
"""

import requests

import my_open
import my_utils
import my_uxlc_changes


def _do_one_download(date):
    filename_in_url = _filename(date, '%20')
    url = f'https://hcanat.us/Changes/{date}%20-%20Changes/{filename_in_url}'
    result_of_get = requests.get(url, timeout=10)
    result_of_get.encoding = 'utf-8'
    filename_in_out_path = _filename(date, ' ')
    out_path = f'in/UXLC-misc/{filename_in_out_path}'
    my_utils.show_progress_g(__file__, out_path)
    text = result_of_get.text
    my_open.with_tmp_openw(out_path, {'newline': ''}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def _filename(date, space):
    return f'{date}{space}-{space}Changes.xml'


def main():
    """ Download various Changes XML file from hcanat.us """
    for filename in my_uxlc_changes.FILENAMES:
        if 'fake' in filename:
            continue
        date = filename[:10]
        _do_one_download(date)


if __name__ == "__main__":
    main()
