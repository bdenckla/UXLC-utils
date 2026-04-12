import sys
from html.parser import HTMLParser
from pathlib import Path

import _repo_path_setup
import py_fois.fois_mark_grammar_foi as fois_mark_grammar_foi


REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = REPO_ROOT / "gh-pages" / "fois" / "foi-mark-grammar.html"
_ORDINARY_PATTERNS_INTRO_PREFIX = "Additional patterns treated as ordinary"


class _OrdinaryPatternsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_intro_paragraph = False
        self._capture_list = False
        self._in_target_list = False
        self._in_list_item = False
        self._current_list_item_parts = []
        self.patterns = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self._in_intro_paragraph = True
        elif tag == "ul" and self._capture_list:
            self._capture_list = False
            self._in_target_list = True
        elif tag == "li" and self._in_target_list:
            self._in_list_item = True
            self._current_list_item_parts = []

    def handle_endtag(self, tag):
        if tag == "p":
            self._in_intro_paragraph = False
        elif tag == "li" and self._in_list_item:
            text = " ".join(
                part.strip() for part in self._current_list_item_parts if part.strip()
            )
            self.patterns.append(text)
            self._in_list_item = False
            self._current_list_item_parts = []
        elif tag == "ul" and self._in_target_list:
            self.patterns = tuple(self.patterns)
            self._in_target_list = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_intro_paragraph and text.startswith(
            _ORDINARY_PATTERNS_INTRO_PREFIX
        ):
            self._capture_list = True
            return
        if self._in_list_item:
            self._current_list_item_parts.append(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ordinary_override_rules = fois_mark_grammar_foi.ordinary_override_rules()
    _assert_unique_rule_keys(ordinary_override_rules)
    rendered_patterns = _rendered_patterns()
    expected_patterns = tuple(rule.description for rule in ordinary_override_rules)
    if rendered_patterns != expected_patterns:
        raise AssertionError(
            _mismatch_message(ordinary_override_rules, rendered_patterns)
        )
    print(
        f"Rule sync OK: {len(ordinary_override_rules)} ordinary override rules match {HTML_PATH}"
    )


def _assert_unique_rule_keys(ordinary_override_rules):
    rule_keys = tuple(rule.key for rule in ordinary_override_rules)
    if len(rule_keys) != len(set(rule_keys)):
        raise AssertionError(f"Duplicate ordinary override rule keys: {rule_keys}")


def _rendered_patterns():
    parser = _OrdinaryPatternsParser()
    parser.feed(HTML_PATH.read_text(encoding="utf-8"))
    rendered_patterns = parser.patterns
    if not rendered_patterns:
        raise AssertionError(
            f"Did not find rendered ordinary-pattern list in {HTML_PATH}"
        )
    return rendered_patterns


def _mismatch_message(ordinary_override_rules, rendered_patterns):
    expected_lines = [
        f"  {rule.key}: {rule.description}" for rule in ordinary_override_rules
    ]
    rendered_lines = [f"  {pattern}" for pattern in rendered_patterns]
    return "\n".join(
        (
            "Rendered ordinary-pattern list is out of sync with ordinary override rules.",
            "Expected:",
            *expected_lines,
            "Rendered:",
            *rendered_lines,
        )
    )


if __name__ == "__main__":
    main()
