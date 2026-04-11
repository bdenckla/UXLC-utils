# UXLC-utils

`py/main_uxlc_download_changes.py` refreshes both the UXLC Changes XML files and the Tanach XML zip.

- Canonical UXLC book XML files are stored in `in/UXLC-39`.
- Non-canonical extracted Tanach XML files (`*.DH.xml`, `TanachHeader.xml`, and `TanachIndex.xml`) are stored in `in/UXLC-rest`.
- The downloaded `Tanach.xml.zip` cache is stored in `./.novc`.