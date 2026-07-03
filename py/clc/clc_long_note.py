"""Exports write_page: the shared "long notes" apparatus page (design doc §7.3).

Design doc §7.3 sketches an "intended" MAM-with-doc-style split: short notes inline
in the doc column, long ones relegated to a separate page. MAM-with-doc decides that
split automatically, by a length threshold (> 400 rendered chars). CLC deliberately
does NOT reuse that threshold: an editor opts a specific note in by hand (clc_render's
``_LONG_NOTE_SPECS``), so this module never inspects note length or decides anything
itself -- it only lays out whatever entries it is handed.

Every long note lives in this one shared page (not split per-book, unlike MAM's
per-book "big-doc" pages) since there is, for now, exactly one; splitting can happen
once there are enough entries to warrant it. Each entry keeps its own anchor so a
short inline note can link straight to its expanded body.
"""

import uxlc_misc.uxlc_utils_html as H

OUT_PATH = "gh-pages/clc/long-notes.html"

# ASCII slug for each dual-cant strand's display short name (clc_dual_cant's own
# Strand.short values), used only to keep the anchor id / URL fragment plain ASCII --
# display text elsewhere in the page is untouched.
_STRAND_SLUG = {
    "taḥton": "tahton",
    "elyon": "elyon",
    "pashut": "pashut",
    "midrashit": "midrashit",
}

# Same idea as _STRAND_SLUG, for an omitted-accent note's "kind" (clc_dual_cant's
# describe_diff.accent_name spelling) -- needed since one (book, ch, v, strand) can carry
# more than one omitted-accent long note (e.g. Deut 5:6's elyon wants both a tipeḥa and an
# etnaḥta), so kind must join strand in the anchor id to keep it unique.
_KIND_SLUG = {
    "pashta": "pashta",
    "meteg": "meteg",
    "merkha": "merkha",
    "tipeḥa": "tipeha",
    "etnaḥta": "etnahta",
    "silluq": "silluq",
}


def anchor_id(book_id, ch, v, strand, kind):
    """The long-notes page anchor id for one (book, ch, v, strand, kind) case."""
    return f"long-{book_id}-{ch}-{v}-{_STRAND_SLUG[strand]}-{_KIND_SLUG[kind]}"


def page_href(anchor):
    """Relative link to one entry, from any page in the same gh-pages/clc/ directory."""
    return f"long-notes.html#{anchor}"


def entry(anchor, heading, blocks):
    """One long-note page section: ``blocks`` is a list of H element/strings."""
    return {"anchor": anchor, "heading": heading, "blocks": blocks}


def write_page(entries):
    """Write OUT_PATH from ``entries`` (as built by clc_render.build_long_notes)."""
    body = [
        H.heading_level_1("Charitable Leningrad Codex — longer notes"),
        H.para(
            [
                "Notes relegated here from a main page’s doc column — opted in "
                "case-by-case by an editor, never by an automatic length threshold "
                "(see doc/clc-design.md §7.3)."
            ]
        ),
        *[_section(e) for e in entries],
    ]
    write_ctx = H.WriteCtx(title="CLC — longer notes", path=OUT_PATH, add_wbr=True)
    H.write_html_to_file(body, write_ctx, "../")
    return OUT_PATH


def _section(e):
    return H.div(
        [H.heading_level_2(e["heading"]), *e["blocks"]],
        {"id": e["anchor"], "class": "clc-long-note"},
    )
