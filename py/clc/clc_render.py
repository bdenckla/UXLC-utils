"""Exports write_book: render a CLC book as a 3-column always-link page.

Layout (design doc §7.3, build-order step 4): one row per verse, columns
``text | ref | doc``. The verse-number (ref) is a narrow central spine with the
Hebrew text on its left and the doc apparatus on its right; keeping the text
adjacent to the ref means a short verse stays butted against its label (no need
for zebra shading to tie the two together). The text column is running verse
text; every noted word is an always-link (no MAM short-inline / long-link
threshold) to its note in the doc column of the same row. CLC defines its own
``clc-*`` CSS vocabulary parallel
to MAM's ``mam-doc-*`` (design doc §8); the rules live in gh-pages/style.css.
"""

from dataclasses import dataclass

import mb_cmn.hebrew_punctuation as hpu   # for hpu.MAQ (־, U+05BE)
import mb_diff_mpu.describe_diff as describe_diff
import clc.clc_attribution as clc_attribution
import clc.clc_dual_cant as clc_dual_cant
import clc.clc_kq as clc_kq
import clc.clc_long_note as clc_long_note
import clc.clc_note as clc_note
import uxlc_misc.uxlc_utils_html as H

_OUT_DIR = "gh-pages/clc"
_HBO_ATTR = {"lang": "hbo", "dir": "rtl"}


def out_label(book_id, chapters=None):
    """Filename stem for a (possibly chapter-limited) book page.

    Whole book -> "Exodus"; limited to chapter(s) -> "Exodus-20" so a focused
    page never clobbers a future full-book "Exodus.html". ``chapters`` is a set of
    1-based chapter numbers (or None / empty for the whole book).
    """
    if not chapters:
        return book_id
    return f"{book_id}-" + "-".join(str(c) for c in sorted(chapters))


def _disp_label(book_id, chapters=None):
    """Human label for title/heading: 'Exodus' or 'Exodus 20'."""
    if not chapters:
        return book_id
    return f"{book_id} " + ", ".join(str(c) for c in sorted(chapters))


def write_book(book_id, book, notes, chapters=None):
    """Write gh-pages/clc/<label>.html and return its path.

    ``chapters`` (a set of 1-based chapter numbers, or None) limits rendering to
    those chapters; the page label/title carry the limit (see ``out_label``).
    Numbering still comes from the enumerate index, so skipping keeps ch/v correct.
    """
    notes_by_atom = _group_by_atom(notes)
    rows = [H.table_row_of_headers(("text", "ref", "doc"))]
    for chidx, chapter in enumerate(book):
        ch = chidx + 1
        if chapters is not None and ch not in chapters:
            continue
        for vridx, verse in enumerate(chapter):
            v = vridx + 1
            if clc_dual_cant.is_dual_cant(book_id, ch, v):
                rows.extend(_dual_cant_rows(book_id, ch, v, verse, notes_by_atom))
            else:
                rows.append(_verse_row(ch, v, verse, notes_by_atom))
    label = out_label(book_id, chapters)
    disp = _disp_label(book_id, chapters)
    table = H.table(rows, {"class": "clc-3col border-collapse"})
    body = _body_wrapper(disp, notes, table)
    out_path = f"{_OUT_DIR}/{label}.html"
    write_ctx = H.WriteCtx(title=f"CLC — {disp}", path=out_path, add_wbr=True)
    H.write_html_to_file(body, write_ctx, "../")
    return out_path


def _group_by_atom(notes):
    grouped = {}
    for note in notes:
        grouped.setdefault((note.ch, note.v, note.atom_index), []).append(note)
    return grouped


def _verse_row(ch, v, verse, notes_by_atom):
    ref_cell = H.table_datum(f"{ch}:{v}", {"class": "clc-ref"})
    text_cell = H.table_datum(
        _text_contents(ch, v, verse, notes_by_atom),
        {**_HBO_ATTR, "class": "clc-text"},
    )
    doc_cell = H.table_datum(
        _doc_contents(ch, v, verse, notes_by_atom), {"class": "clc-doc"}
    )
    return H.table_row((text_cell, ref_cell, doc_cell))


def _dual_cant_rows(book_id, ch, v, verse, notes_by_atom):
    # A dual-cantillation verse (e.g. Gen 35:22) becomes three grouped rows:
    # combined (C), strand alef (א), strand bet (ב). The combined row keeps the
    # full always-link behaviour (its notes/anchors); the strand rows show the
    # strictly-split text plain, with only a short strand label in the doc
    # column. CSS ties the three into one verse block (gh-pages/style.css).
    views = clc_dual_cant.strand_views(book_id, ch, v, verse)
    strands = [vw for vw in views if vw.suffix != clc_dual_cant.SUFFIX_COMBINED]
    rows = []
    for pos, view in enumerate(views):
        ref_cell = H.table_datum(
            f"{ch}:{v}-{view.suffix}", _strand_ref_attr(view.tooltip, pos, len(views))
        )
        if view.suffix == clc_dual_cant.SUFFIX_COMBINED:
            text_cell = H.table_datum(
                _text_contents(ch, v, view.atoms, notes_by_atom),
                {**_HBO_ATTR, "class": "clc-text"},
            )
            doc_cell = H.table_datum(
                _doc_contents(ch, v, view.atoms, notes_by_atom), {"class": "clc-doc"}
            )
        else:
            # De-highlight against the OTHER strand (the two strands agree here),
            # not the combined form — see _plain_text_contents.
            other = next(vw for vw in strands if vw is not view)
            text_cell = H.table_datum(
                _plain_text_contents(view.atoms, other.atoms),
                {**_HBO_ATTR, "class": "clc-text"},
            )
            doc_cell = H.table_datum(_strand_doc_contents(view), {"class": "clc-doc"})
        rows.append(H.table_row((text_cell, ref_cell, doc_cell)))
    return rows


def _strand_doc_contents(view):
    # The strand label, then this strand's synthesized notes (clc_dual_cant._strand_notes):
    # one "added out of thin air" note per SUPPLIED punctuation mark, and one note per accent
    # the strand wants but UXLC OMITTED (noted, never supplied — §7.7).
    contents = [H.span(view.doc_label, {"class": "clc-strand-label"})]
    for note in view.notes:
        contents.append(H.line_break())
        if note["source"] == clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT:
            contents.append(_omitted_note_block(note))
        else:
            contents.append(_added_note_block(note))
    return contents


_LC_CORROBORATED_LINK = "https://bdenckla.github.io/wlc-utils/accgram/supplied-marks.html"


def _omitted_note_sentence(note):
    # "the <strand> strand calls for a(n) <accent> on <word> here, but UXLC's combined text
    # carries only the <other> strand's <present accent>, and it is beyond the limits of CLC's
    # charity to supply the missing <accent>" — the word in rtl Hebrew, NO bracketed mark
    # (nothing is added to the strand; cf. _added_note_block). The accent UXLC *does* have is
    # named, not abstracted. Accents are noted, never supplied (§7.7).
    #
    # "the LC has only..." (crediting the manuscript, not just UXLC's own transcription of it)
    # replaces "UXLC's combined text carries" whenever this note is grounded beyond CLC's own
    # synthesis: either wlc-utils's grammar-checker corroboration (issue #36,
    # clc_dual_cant._LC_CORROBORATED) or an editor-attached long note making its own independent
    # case (clc_dual_cant._HAS_LONG_NOTE) — e.g. Deut 5:13's taḥton pashta, whose long note cites
    # UXLC's own note citing BHL Appendix A. A long note attached here is expected to itself
    # justify that stronger claim, not just restate CLC's own reasoning at length.
    #
    # A missing *meteg* takes softened wording (_omitted_meteg_sentence) instead: a meteg is
    # not an accent, so the "calls for … / charity to supply" framing — which treats the wanted
    # mark as genuinely wanted — over-claims. See that helper for the reasoning.
    #
    # Factored out of _omitted_note_block so the long-notes page (clc_long_note, via
    # clc_render.build_long_notes) can recap the exact same sentence, never a paraphrase.
    if note["kind"] == "meteg" and note.get("present_kind"):
        return _omitted_meteg_sentence(note)
    article = "an" if note["kind"][:1] in "aeiou" else "a"
    lc_corroborated = note.get("lc_corroborated", False)
    grounded = lc_corroborated or note.get("has_long_note", False)
    carries = "the LC has" if grounded else "UXLC’s combined text carries"
    has = (f"only the {note['other_strand']} strand’s {note['present_kind']}"
           if note.get("present_kind") else f"no accent for the {note['strand']} strand")
    return [
        f"The {note['strand']} strand calls for {article} {note['kind']} on ",
        H.span(note["snippet"], _HBO_ATTR),
        f" here, but {carries} {has}, and it is beyond the limits"
        f" of CLC’s charity to supply the missing {note['kind']}"
        + ("" if lc_corroborated else "."),
    ]


def _omitted_meteg_sentence(note):
    # Softened wording for an omitted *meteg* (the strand wants a meteg U+05BD where UXLC's
    # single mark is the OTHER strand's accent). Unlike the accent path in _omitted_note_
    # sentence, this does NOT say the strand "calls for" the mark, nor that CLC's charity
    # declines to "supply the missing meteg." A meteg (gaʿya) is metrical, not part of the
    # cantillation/trope system, and even the gaʿyot usually deemed obligatory are not
    # consistently written in the manuscripts; the special gaʿya on יהיה-type verbs (Deut
    # 5:7's יִהְיֶה־) is not clearly of the obligatory kind at all (cf. Yeivin, ITM). So the
    # situation is not a wanted-but-withheld accent but a single manuscript mark that CLC must
    # transcribe one way or the other: it reads that mark as the OTHER strand's accent, which
    # — unlike the meteg — the chant truly needs. Where an editor attaches a long note (§7.3,
    # clc_dual_cant._HAS_LONG_NOTE), _omitted_note_block links to its further discussion.
    present = note["present_kind"]
    article = "an" if present[:1] in "aeiou" else "a"
    return [
        f"A meteg might be expected in the {note['strand']} strand here on ",
        H.span(note["snippet"], _HBO_ATTR),
        f", but the LC has only a single mark, which is best transcribed as {article} {present}"
        f" since, unlike the meteg, the {present} is truly needed.",
    ]


def _omitted_note_block(note):
    # Wraps _omitted_note_sentence with whatever tail(s) this note's grounding calls for:
    # the wlc-utils link (lc_corroborated) and/or a link to this note's own long-notes-page
    # entry (has_long_note) — see clc_dual_cant._LC_CORROBORATED / _HAS_LONG_NOTE. Either,
    # neither, or (in principle) both may apply; each appends its own trailing sentence.
    contents = list(_omitted_note_sentence(note))
    if note.get("lc_corroborated"):
        contents.extend(
            [
                " — see the grammar checker’s ",
                H.anchor("supplied accents", {"href": _LC_CORROBORATED_LINK}),
                " page.",
            ]
        )
    if note.get("has_long_note"):
        book_id, ch, v = note["verse_loc"]
        anchor = clc_long_note.anchor_id(book_id, ch, v, note["strand"])
        contents.extend(
            [
                " See more details in ",
                H.anchor("this longer note", {"href": clc_long_note.page_href(anchor)}),
                ".",
            ]
        )
    return H.div(contents, {"class": "clc-added-note"})


def _added_note_block(note):
    # "<name> in <strand word><[mark]> added out of thin air, to improve legibility"
    # — snippet in rtl Hebrew, the supplied mark echoed in the bracketed/green
    # style used in the text column. The snippet and its bracketed mark share one
    # dir="rtl" wrapper (so [dir] → unicode-bidi: isolate) — otherwise, in this
    # LTR note, the isolated snippet reorders correctly but the trailing [mark]
    # floats to the wrong (LTR) side. Wrapped, the whole <word>[mark] reorders as
    # one RTL unit, matching the text column (whose td is itself dir="rtl").
    return H.div(
        [
            f"{note['kind']} in ",
            H.span(
                [H.span(note["snippet"], _HBO_ATTR), _added_span(note["char"])],
                {"dir": "rtl"},
            ),
            " added out of thin air, to improve legibility",
        ],
        {"class": "clc-added-note"},
    )


def _strand_ref_attr(tooltip, pos, count):
    # Group the strand rows into one verse block: the first row keeps the top
    # divider, the last keeps the bottom one, the middle rows drop both.
    classes = ["clc-ref", "clc-ref-strand"]
    if pos == 0:
        classes.append("clc-strand-first")
    if pos == count - 1:
        classes.append("clc-strand-last")
    return {"class": " ".join(classes), "title": tooltip}


def _text_contents(ch, v, verse, notes_by_atom):
    # Group ketiv/qere atoms into units (clc_kq) so each renders as one boxed
    # ruby — qere on the baseline, ketiv above — and adjacent independent pairs
    # stay visibly separate from a grouped multi-word unit. Plain words render
    # exactly as before: an always-link if noted, otherwise bare text.
    pieces = []
    for item in clc_kq.iter_render_units(verse):
        if isinstance(item, clc_kq.KqUnit):
            pieces.append(clc_kq.kq_ruby(item, notes_by_atom, ch, v))
            _append_join_space(pieces, clc_kq.join_text(item))
        else:
            href = _note_href(ch, v, item.position, notes_by_atom.get((ch, v, item.position)))
            if href:
                pieces.append(H.anchor(item.text, {"href": href, "class": "clc-doc-target"}))
            else:
                pieces.append(item.text)
            _append_join_space(pieces, item.text)
    return pieces


def _relegated_anchor(note):
    # Non-None iff this UXLC x-note is relegated to the long-notes page instead of an
    # inline same-row block (design doc §7.3, case-by-case — see _LONG_NOTE_SPECS).
    return _UXLC_NOTES_RELEGATED.get((note.book, note.ch, note.v, note.atom_index, note.note_code))


def _note_href(ch, v, position, atom_notes):
    # The word's always-link target: the local same-row anchor if it has any note that
    # still renders there, else — if EVERY note on this atom is relegated (above) — the
    # long-notes page anchor instead (design doc §7.3's "the always-link then points
    # across to the anchored body on that page instead of into the same-row doc cell"),
    # else None (unnoted word, no link).
    if not atom_notes:
        return None
    if any(_relegated_anchor(n) is None for n in atom_notes):
        return f"#{_anchor_id(ch, v, position)}"
    anchors = {_relegated_anchor(n) for n in atom_notes}
    assert len(anchors) == 1, (ch, v, position, anchors)  # one atom, one long note, for now
    (anchor,) = anchors
    return clc_long_note.page_href(anchor)


def _plain_text_contents(strand_atoms, other_atoms):
    # Like _text_contents but with no note always-links — used by the alef/bet
    # strand rows of a dual-cant verse, whose notes/anchors live on the combined
    # row only (re-emitting them here would duplicate anchor ids). Each word
    # identical across the two strands (taxton == elyon — i.e. not a divergence
    # atom) is de-highlighted (clc-strand-same) so the few divergence words stand
    # out by contrast. A word that differs from the OTHER strand stays highlighted
    # — including one equal to the combined form yet diverging from its sibling
    # (e.g. ex 20:9 כל, whose taxton keeps a dagesh elyon drops), and one carrying a
    # SUPPLIED mark (clc_dual_cant additions) the other strand lacks; any supplied
    # mark is rendered bracketed/green right after the word.
    pieces = []
    for strand_atom, other_atom in zip(strand_atoms, other_atoms):
        atom_text = strand_atom["text"]
        additions = strand_atom.get("additions", ())
        same_across_strands = atom_text == other_atom["text"] and tuple(
            additions
        ) == tuple(other_atom.get("additions", ()))
        if same_across_strands:
            pieces.append(H.span(atom_text, {"class": "clc-strand-same"}))
        else:
            pieces.append(atom_text)
        for added in additions:
            pieces.append(_added_span(added))
        _append_join_space(pieces, additions[-1] if additions else atom_text)
    return pieces


def _added_span(added_char):
    # A maqaf/sof-pasuq SUPPLIED to this strand for legibility (clc_dual_cant):
    # bracketed, the mark itself green (clc-added-during-detangling) to flag
    # "added, not in the codex". Brackets stay in running-text color.
    return H.span(
        ["[", H.span(added_char, {"class": "clc-added-during-detangling"}), "]"],
        {"class": "clc-added-bracket"},
    )


def _append_join_space(pieces, join_key):
    # Smart-join: a unit ending in maqaf butts directly against the next (one
    # hyphenated compound, e.g. אֶת־הָאָרֶץ); add_wbr still allows a line break at
    # the maqaf. `join_key` is the unit's text — or, for a strand atom that
    # SUPPLIES a trailing mark, that mark — so a supplied maqaf butts while a
    # supplied sof-pasuq still gets a following space. Only non-maqaf units get one.
    if not join_key.endswith(hpu.MAQ):
        pieces.append(" ")


def _doc_contents(ch, v, verse, notes_by_atom):
    blocks = []
    for atidx, _atom in enumerate(verse):
        position = atidx + 1
        atom_notes = notes_by_atom.get((ch, v, position))
        if not atom_notes:
            continue
        visible = [n for n in atom_notes if _relegated_anchor(n) is None]
        if visible:
            blocks.append(_note_block(ch, v, position, visible))
    return blocks


def _note_block(ch, v, position, atom_notes):
    entries = [
        H.span(atom_notes[0].atom_text, _HBO_ATTR),
    ]
    for note in atom_notes:
        entries.append(H.line_break())
        if note.is_uxlc_departure:
            entries.append(_departure_note_block(note))
        else:
            entries.append(H.span(f"[{note.note_code}] ", {"class": "clc-note-code"}))
            if note.superseding_uxlc_change:
                entries.append(
                    clc_attribution.superseding_change_cite(note.superseding_uxlc_change)
                )
            else:
                entries.append(note.note_text)
                entries.append(clc_attribution.note_cite(note.source_url))
    return H.div(entries, {"id": _anchor_id(ch, v, position), "class": "clc-note"})


def _departure_note_block(note):
    # States plainly that CLC replaced UXLC's own reading (never "shared" -- that
    # framing was rejected), naming the two marks via _accent_diff_names rather than
    # hardcoding "pashta"/"qadma" so this reads correctly if reused for a different
    # mark pair later. No note-code prefix or Hebrew snippets -- those belong to
    # showing the UXLC note itself, which this note deliberately doesn't (its whole
    # point is that CLC now departs from UXLC here) -- but "pending change" itself
    # links to the UXLC change record, reusing clc_attribution's link builder.
    old_name, new_name = _accent_diff_names(note.uxlc_reading, note.clc_reading)
    return H.div(
        [
            f"Here CLC replaces UXLC's {old_name} with a {new_name}. UXLC has a ",
            clc_attribution.change_record_link(
                note.superseding_uxlc_change, "pending change"
            ),
            " making this correction.",
        ],
        {"class": "clc-added-note"},
    )


def _accent_diff_names(uxlc_reading, clc_reading):
    # Diff the two same-length readings at their single differing character, naming
    # each via the canonical mb_diff_mpu authority (mirrors clc_dual_cant's own
    # _accent_name/_present_accent pattern) -- so this note never hardcodes
    # "pashta"/"qadma" and stays correct if reused for a different departure later.
    assert len(uxlc_reading) == len(clc_reading), (uxlc_reading, clc_reading)
    diffs = [(a, b) for a, b in zip(uxlc_reading, clc_reading) if a != b]
    assert len(diffs) == 1, (uxlc_reading, clc_reading, diffs)
    old_char, new_char = diffs[0]
    return describe_diff.accent_name(old_char), describe_diff.accent_name(new_char)


def _anchor_id(ch, v, position):
    return f"clc-{ch}-{v}-{position}"


_BHL_TITLE = "Dotan’s Biblia Hebraica Leningradensia"
_WLC_TITLE = "Westminster Leningrad Codex"
_BHS_TITLE = "Biblia Hebraica Stuttgartensia"


def _dt_5_13_taxton_extra(_book, notes):
    # "See the UXLC note on this word. The lack of this pashta is noted in BHL
    # Appendix A." -- UXLC's own Deut 5:13.2-t note (suppressed inline, see
    # _UXLC_NOTES_RELEGATED below) already says as much ("BHL Appendix A has no
    # pashta on the final mem."); this just surfaces that citation instead of
    # reproducing the note's full text a second time.
    #
    # Second paragraph: the flip side of that same absence. wlc-utils's grammar checker
    # (the accgram detangler) supplies a strand's missing accent so it parses -- but it
    # never had to for this pashta, because WLC already carries it (wrongly). Named
    # generically as "the grammar checker" per Ben; the BHS-origin guess stays hedged.
    uxlc_note = next(
        n for n in notes
        if (n.book, n.ch, n.v, n.atom_index, n.note_code) == ("Deuter", 5, 13, 2, "t")
    )
    # A list of paragraphs (each a list of inline pieces).
    return [
        [
            "See the ",
            H.anchor("UXLC note", {"href": uxlc_note.source_url, "target": "_blank"}),
            " on this word. The lack of this pashta is noted in ",
            H.abbr("BHL", {"title": _BHL_TITLE}),
            " Appendix A.",
        ],
        [
            "This pashta is also not among the accents the grammar checker has to supply"
            " to ",
            H.abbr("WLC", {"title": _WLC_TITLE}),
            " when detangling the two strands: unlike a genuine omission, it is already"
            " present in WLC — erroneously, presumably carried over from ",
            H.abbr("BHS", {"title": _BHS_TITLE}),
            ", though this has not yet been verified.",
        ],
    ]


# Yeivin, Introduction to the Tiberian Masorah §355 (the special "phonetic" gaʿya of
# היה/חיה-root forms), in Ben's adaptation on phonetic-hbo. House style for such deep
# links is a "section NNN" anchor (cf. MAM-basics rocc_4_mid_word_ga3ya_with_shewa).
_YEIVIN_ITM_355_URL = "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns355"


def _dt_5_7_elyon_meteg_extra(_book, _notes):
    # Why the elyon's missing mark here is treated as an optional meteg, not a wanted
    # accent (see _omitted_meteg_sentence for the short-note wording this expands on):
    # the mark is the special gaʿya of היה/חיה-root forms, whose marking Yeivin (ITM §355)
    # calls inconsistent across manuscripts and absent from the ḥillufim lists.
    #
    # The one caveat Yeivin adds — this gaʿya IS "as a rule" marked when the word is joined by
    # maqqef to an *initially-stressed* following word — may or may not cover Deut 5:7 (יהיה־לך).
    # Do NOT adjudicate it: an earlier draft claimed לך is "final-stressed, not initial," so the
    # exception fails — but whether Yeivin counts לך as initially stressed is genuinely unclear
    # (it turns on whether he reckons syllable/stress in modern or Masoretic terms — e.g. a vocal
    # shewa forming no syllable of its own would make לְךָ pattern with his monosyllables). Per
    # Ben, we do NOT litigate that in the note. Either way CLC's move stands: a gaʿya is metrical
    # (not an accent), "as a rule" is not "always," and — decisively — the one mark the LC
    # actually carries is the taxton's merkha, which the chant needs; CLC reads the mark as that
    # merkha and invents no second one for the gaʿya. No inline UXLC x-note is relegated for this
    # one. The rendered note keeps none of this argument in prose: it is just a one-sentence
    # pointer to Yeivin ITM §355 (where his own "as a rule" caveat lives) plus the aside below.
    #
    # Closing aside (paired with the LC folio-102A detail image this spec carries): the mark
    # is this note's main subject, but the word's own initial yod is a separate act of
    # charity — most of its top has flaked off, and it is read from the faint
    # surviving remnants together with the context. Charity is CLC's central principle, so
    # it is worth surfacing even where the mark, not the letter, is the occasion for the note.
    #
    # Returns a list of paragraphs (each a list of inline pieces); see _build_long_note_entry.
    return [
        [
            "Regarding the meteg that might be expected on ",
            H.span("יִהְיֶה־", _HBO_ATTR),
            ", see ",
            H.anchor("section 355", {"href": _YEIVIN_ITM_355_URL, "target": "_blank"}),
            " of Yeivin’s Introduction to the Tiberian Masorah.",
        ],
        [
            "Aside: the mark transcribed as merkha is this note’s main subject,"
            " but it should be noted that the word’s initial yod is a charitable transcription,"
            " since most of the top of the yod seems to have flaked off."
            " This yod is transcribed as present based on"
            " expectation combined with"
            " the tail that did not flake off,"
            " plus the faint remnants that seem to have remained even after flaking.",
        ],
    ]


@dataclass(frozen=True)
class _LongNoteSpec:
    """One editor-opted-in long note (design doc §7.3) -- case-by-case, never an
    automatic length threshold. ``strand``/``kind`` locate the clc_dual_cant omitted-
    accent note this long note expands on (see clc_dual_cant._HAS_LONG_NOTE, which
    must independently list the same case); ``relegated_position``/``relegated_code``
    is the UXLC x-note this long note's own citation subsumes, so it is suppressed
    from its usual same-row doc-cell block instead of showing twice -- ``None``/``""``
    when this long note relegates no inline UXLC note (e.g. Deut 5:7's elyon meteg, pure
    further discussion). ``image_filename`` is a file under gh-pages/img/ (empty string
    for no image) -- fetched by hand, once, from the UXLC note's own detail image (see
    .novc/fetch_dt_5_13_2_t_image.py) and committed as a static asset, never re-downloaded
    at build time; ``image_credit`` is that source page's own credit line, carried forward
    alongside it. ``extra_blocks`` is ``(book, notes) -> [H pieces]``, this note's own added
    content beyond the verse/short-note recap every long note gets automatically."""

    book_id: str
    ch: int
    v: int
    strand: str
    kind: str
    relegated_position: object  # int, or None when no inline UXLC note is relegated
    relegated_code: str
    image_filename: str
    image_credit: str
    extra_blocks: object


_LONG_NOTE_SPECS = (
    _LongNoteSpec(
        "Deuter", 5, 13, "taḥton", "pashta", 2, "t",
        "Deuter.5.13.2-t.jpg", "Sefaria.org",
        _dt_5_13_taxton_extra,
    ),
    _LongNoteSpec(
        "Deuter", 5, 7, "elyon", "meteg", None, "",
        "Deuter.5.7.2.LC-102A-col3-line22.jpg", "Sefaria.org",
        _dt_5_7_elyon_meteg_extra,
    ),
)

# Derived from _LONG_NOTE_SPECS: (book, ch, v, atom_index, note_code) -> long-note
# anchor id, consulted by _relegated_anchor/_note_href/_doc_contents to suppress a
# relegated UXLC x-note's inline block and redirect its always-link. Only specs that
# actually relegate an inline UXLC note participate (relegated_position is not None) --
# a pure-further-discussion long note like Deut 5:7's elyon meteg subsumes nothing.
_UXLC_NOTES_RELEGATED = {
    (spec.book_id, spec.ch, spec.v, spec.relegated_position, spec.relegated_code):
        clc_long_note.anchor_id(spec.book_id, spec.ch, spec.v, spec.strand)
    for spec in _LONG_NOTE_SPECS
    if spec.relegated_position is not None
}


def build_long_notes(book_id, book, notes, chapters=None):
    """Build this build job's long-note page entries (design doc §7.3), for the
    caller (main_clc.py) to accumulate across jobs and hand to clc_long_note.write_page
    once. ``book``/``notes`` are collect_for_book's own return values -- reused here,
    never re-read from disk. ``chapters`` mirrors write_book's own chapter limit."""
    entries = []
    for spec in _LONG_NOTE_SPECS:
        if spec.book_id != book_id:
            continue
        if chapters is not None and spec.ch not in chapters:
            continue
        entries.append(_build_long_note_entry(spec, book, notes))
    return entries


def _build_long_note_entry(spec, book, notes):
    verse_atoms = book[spec.ch - 1][spec.v - 1]
    views = clc_dual_cant.strand_views(spec.book_id, spec.ch, spec.v, verse_atoms)
    strands = [vw for vw in views if vw.suffix != clc_dual_cant.SUFFIX_COMBINED]
    view, note = _find_strand_note(strands, spec.strand, spec.kind)
    other = next(vw for vw in strands if vw is not view)
    anchor = clc_long_note.anchor_id(spec.book_id, spec.ch, spec.v, spec.strand)
    heading = f"{spec.book_id} {spec.ch}:{spec.v} — {view.doc_label}"
    verse_recap = H.para([H.span(_plain_text_contents(view.atoms, other.atoms), _HBO_ATTR)])
    # Labeled so a reader landing here from the always-link (not from the short note's
    # own "see more details" link) can tell which part is a verbatim recap of what the
    # main page already says, versus the content that's new to this page.
    short_recap = H.para(["Inline note (repeated from main page): ", *_omitted_note_sentence(note)])
    # extra_blocks returns a list of paragraphs (each a list of inline pieces); the
    # "Further discussion:" label leads the first, the rest (e.g. Deut 5:7's aside) follow.
    para_contents = spec.extra_blocks(book, notes)
    extra_paras = [H.para(["Further discussion: ", *para_contents[0]])]
    extra_paras += [H.para(pc) for pc in para_contents[1:]]
    blocks = [verse_recap, short_recap]
    if spec.image_filename:
        blocks.append(_long_note_image(spec))
    blocks.extend(extra_paras)
    return clc_long_note.entry(anchor, heading, blocks)


def _long_note_image(spec):
    # The image sits between the short-note recap and the further discussion it
    # illustrates. gh-pages/clc/long-notes.html -> gh-pages/img/ is one level up.
    return H.div(
        [
            H.img(
                {
                    "src": f"../img/{spec.image_filename}",
                    "alt": f"Manuscript detail for {spec.book_id} {spec.ch}:{spec.v}",
                    "class": "clc-long-note-img",
                }
            ),
            H.para([f"Credit: {spec.image_credit}."], {"class": "clc-long-note-img-credit"}),
        ],
        {"class": "clc-long-note-img-wrap"},
    )


def _find_strand_note(strands, strand, kind):
    for view in strands:
        for note in view.notes:
            if note.get("strand") == strand and note.get("kind") == kind:
                return view, note
    raise LookupError((strand, kind))


def _body_wrapper(book_id, notes, table):
    style = "max-width: 60rem; margin-left: auto; margin-right: auto"
    contents = [
        H.heading_level_1(f"Charitable Leningrad Codex — {book_id}"),
        clc_attribution.top_credit(),
        _intro_para(notes),
        table,
    ]
    return [H.div(contents, {"style": style})]


def _intro_para(notes):
    return H.para(
        [
            "CLC walking skeleton. This page surfaces UXLC's own ",
            H.code("<x>"),
            f" notes ({_code_counts_text(notes)}) as always-links — the under-bar "
            "codes m/d plus the general transcription-uncertainty catch-all t — each "
            "carrying its tanach.us note-page prose (an atom whose note page is not "
            "yet downloaded shows a bare [note not yet downloaded] placeholder, never "
            "invented text). No accent grammar and no charitable resolution yet — see "
            "doc/clc-design.md.",
        ]
    )


def _code_counts_text(notes):
    counts = {}
    for note in notes:
        counts[note.note_code] = counts.get(note.note_code, 0) + 1
    parts = [f"{counts[code]}×{code}" for code in ("m", "d", "t") if code in counts]
    return ", ".join(parts) if parts else "none"
