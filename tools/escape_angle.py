#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escape bare capitalized <Component> tags in chapter prose (idempotent).

VitePress / Pandoc treat a bare `<Map>` in prose as an HTML tag. Inside code
fences (``` ... ```) and inline code (`...`) such tags must stay literal, so
this script only escapes capitalized tags that appear in *real prose* — outside
fences and outside backtick spans. Already-escaped entities are left untouched.

IMPORTANT: this script NEVER removes or rewrites inline-code spans. It walks
each line tracking both code-fence state and inline-backtick state, and only
rewrites a line when an actual escape occurred.

Run: python tools/escape_angle.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAPTERS_DIR = os.path.join(REPO, "docs", "chapters")


def escape_line(ln: str) -> str:
    """Escape capitalized tags in prose only; preserve inline code & fences."""
    out = []
    i = 0
    n = len(ln)
    in_inline = False
    while i < n:
        c = ln[i]
        if c == '`':
            in_inline = not in_inline
            out.append(c)
            i += 1
            continue
        if (not in_inline) and c == '<':
            m = re.match(r"<(\/?[A-Z][A-Za-z0-9]*)([^>]*)>", ln[i:])
            if m:
                out.append("&lt;%s%s&gt;" % (m.group(1), m.group(2)))
                i += len(m.group(0))
                continue
        out.append(c)
        i += 1
    return "".join(out)


def process(text: str) -> str:
    lines = text.split("\n")
    out = []
    in_fence = False
    changed = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        new_ln = escape_line(ln)
        if new_ln != ln:
            changed = True
        out.append(new_ln)
    return "\n".join(out), changed


def main():
    for fn in sorted(os.listdir(CHAPTERS_DIR)):
        if not re.match(r"^chapter\d+\.md$", fn):
            continue
        path = os.path.join(CHAPTERS_DIR, fn)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new, changed = process(text)
        if changed:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print("%s -> escaped bare tag(s)" % fn)
        else:
            print("%s -> no change" % fn)


if __name__ == "__main__":
    main()
