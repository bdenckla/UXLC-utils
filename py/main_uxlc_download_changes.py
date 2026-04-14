"""
Base Usage:
.venv/Scripts/python.exe py/main_uxlc_download_changes.py
"""

from pathlib import Path
import random
import time
import zipfile

import requests

import main_0_mega
import py_misc.my_open as my_open
import py_misc.my_uxlc as my_uxlc
import py_misc.my_uxlc_changes as my_uxlc_changes


_UXLC_ZIP_URL = "https://tanach.us/Books/Tanach.xml.zip"
_UXLC_39_DIR = Path(my_uxlc.UXLC_CANONICAL_DIR)
_UXLC_REST_DIR = Path("in/UXLC-rest")
_NOVC_DIR = Path(".novc")
_UXLC_ZIP_PATH = _NOVC_DIR / "Tanach.xml.zip"
_DELAY_MIN = 1.5
_DELAY_MEAN = 3.0
_REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; uxlc-download-changes/1.0; "
        "+educational/personal-study)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "he,en;q=0.5",
    "Referer": "https://tanach.us/Books/",
    "Connection": "keep-alive",
}


def _do_one_download(session, date):
    filename_in_url = _filename(date, "%20")
    url = f"https://tanach.us/Changes/{date}%20-%20Changes/{filename_in_url}"
    filename_in_out_path = _filename(date, " ")
    out_path = f"in/UXLC-misc/{filename_in_out_path}"
    _show_progress(out_path)
    text = _read_url_as_text(session, url, timeout=10)
    my_open.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def _filename(date, space):
    return f"{date}{space}-{space}Changes.xml"


def _make_session():
    session = requests.Session()
    session.headers.update(_REQUEST_HEADERS)
    return session


def _polite_sleep():
    extra = random.expovariate(1.0 / (_DELAY_MEAN - _DELAY_MIN))
    time.sleep(_DELAY_MIN + extra)


def _read_url_as_bytes(session, url, timeout):
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def _read_url_as_text(session, url, timeout):
    return _read_url_as_bytes(session, url, timeout).decode("utf-8")


def _download_latest_uxlc(session):
    _UXLC_39_DIR.mkdir(parents=True, exist_ok=True)
    _UXLC_REST_DIR.mkdir(parents=True, exist_ok=True)
    _NOVC_DIR.mkdir(parents=True, exist_ok=True)
    _show_progress(str(_UXLC_ZIP_PATH))
    with open(_UXLC_ZIP_PATH, "wb") as out_fp:
        out_fp.write(_read_url_as_bytes(session, _UXLC_ZIP_URL, timeout=30))
    _extract_uxlc_zip(_UXLC_ZIP_PATH)


def _extract_uxlc_zip(zip_path):
    with zipfile.ZipFile(zip_path) as zip_fp:
        for zip_info in zip_fp.infolist():
            if zip_info.is_dir():
                continue
            member_name = Path(zip_info.filename).name
            if not member_name.endswith(".xml"):
                continue
            out_dir = _target_dir_for_member(member_name)
            out_path = out_dir / member_name
            _show_progress(str(out_path))
            with zip_fp.open(zip_info) as in_fp, open(out_path, "wb") as out_fp:
                out_fp.write(in_fp.read())


def _target_dir_for_member(member_name):
    if member_name in my_uxlc.CANONICAL_XML_FILE_NAMES:
        return _UXLC_39_DIR
    return _UXLC_REST_DIR


def _show_progress(path):
    print(f"{Path(__file__).name} {path}")


def main():
    """Download UXLC inputs, then rebuild downstream derived outputs."""
    session = _make_session()
    _download_latest_uxlc(session)
    for filename in my_uxlc_changes.FILENAMES:
        if "fake" in filename:
            continue
        _polite_sleep()
        date = filename[:10]
        _do_one_download(session, date)
    main_0_mega.main()


if __name__ == "__main__":
    main()
