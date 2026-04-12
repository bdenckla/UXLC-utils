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
        self._target_list_depth = 0
        self._item_stack = []
        self.patterns = []

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self._in_intro_paragraph = True
        elif tag == "ul" and self._capture_list:
            self._capture_list = False
            self._target_list_depth = 1
        elif tag == "ul" and self._target_list_depth:
            self._target_list_depth += 1
        elif tag == "li" and self._target_list_depth:
            self._item_stack.append({"text-parts": [], "subitems": []})

    def handle_endtag(self, tag):
        if tag == "p":
            self._in_intro_paragraph = False
        elif tag == "li" and self._item_stack:
            item_data = self._item_stack.pop()
            item = fois_mark_grammar_foi.OrdinaryPatternDisplayItem(
                _joined_text(item_data["text-parts"]),
                tuple(item_data["subitems"]),
            )
            if self._item_stack:
                self._item_stack[-1]["subitems"].append(item)
            else:
                self.patterns.append(item)
        elif tag == "ul" and self._target_list_depth:
            self._target_list_depth -= 1
            if self._target_list_depth:
                return
            self.patterns = tuple(self.patterns)

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_intro_paragraph and text.startswith(
            _ORDINARY_PATTERNS_INTRO_PREFIX
        ):
            self._capture_list = True
            return
        if self._item_stack:
            self._item_stack[-1]["text-parts"].append(text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ordinary_override_rules = fois_mark_grammar_foi.ordinary_override_rules()
    _assert_unique_rule_keys(ordinary_override_rules)
    rendered_patterns = _rendered_patterns()
    expected_patterns = fois_mark_grammar_foi.ordinary_pattern_display_items()
    if rendered_patterns != expected_patterns:
        raise AssertionError(_mismatch_message(expected_patterns, rendered_patterns))
    print(
        f"Rule sync OK: {len(ordinary_override_rules)} ordinary override rules and the rendered ordinary-pattern list match {HTML_PATH}"
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


def _joined_text(parts):
    return " ".join(part.strip() for part in parts if part.strip())


def _mismatch_message(expected_patterns, rendered_patterns):
    expected_lines = _pattern_lines(expected_patterns)
    rendered_lines = _pattern_lines(rendered_patterns)
    return "\n".join(
        (
            "Rendered ordinary-pattern list is out of sync with ordinary override rules.",
            "Expected:",
            *expected_lines,
            "Rendered:",
            *rendered_lines,
        )
    )


def _pattern_lines(patterns, indent=2):
    lines = []
    prefix = " " * indent + "- "
    for pattern in patterns:
        lines.append(f"{prefix}{pattern.text}")
        if pattern.subitems:
            lines.extend(_pattern_lines(pattern.subitems, indent + 2))
    return lines


if __name__ == "__main__":
    main()
