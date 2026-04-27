"""
Base Usage:
.venv/Scripts/python.exe py/main_uxlc_download_changes.py
"""

from pathlib import Path
import zipfile

import main_0_mega
from mb_cmn import polite_download
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
    text = session.get_text(url, timeout=10, encoding="utf-8")
    my_open.with_tmp_openw(out_path, {"newline": ""}, _write_callback, text)


def _write_callback(text, out_fp):
    out_fp.write(text)


def _filename(date, space):
    return f"{date}{space}-{space}Changes.xml"


def _download_latest_uxlc(session):
    _UXLC_39_DIR.mkdir(parents=True, exist_ok=True)
    _UXLC_REST_DIR.mkdir(parents=True, exist_ok=True)
    _NOVC_DIR.mkdir(parents=True, exist_ok=True)
    _show_progress(str(_UXLC_ZIP_PATH))
    with open(_UXLC_ZIP_PATH, "wb") as out_fp:
        out_fp.write(session.get_bytes(_UXLC_ZIP_URL, timeout=30))
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
    with polite_download.PoliteDownloader(_UXLC_DOWNLOAD_CONFIG) as session:
        _download_latest_uxlc(session)
        for filename in my_uxlc_changes.FILENAMES:
            if "fake" in filename:
                continue
            date = filename[:10]
            _do_one_download(session, date)
    main_0_mega.main()


_UXLC_DOWNLOAD_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=(
        "Mozilla/5.0 (compatible; uxlc-download-changes/1.0; "
        "+educational/personal-study)"
    ),
    default_timeout_s=30.0,
    accept_language="he,en;q=0.5",
    referer="https://tanach.us/Books/",
    default_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    throttle=polite_download.ThrottleConfig(
        min_delay_s=_DELAY_MIN, mean_delay_s=_DELAY_MEAN
    ),
    retry=polite_download.RetryConfig(max_attempts=4),
    cache=polite_download.CacheConfig(dir_path=".novc/http-cache/tanach-us"),
    obey_robots_txt=True,
)


if __name__ == "__main__":
    main()
