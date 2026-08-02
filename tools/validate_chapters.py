#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate chapters: find TRUE corruption only.
True corruption = a prose line (outside fenced code) containing two
consecutive spaces in the MIDDLE (preceded AND followed by a non-space char),
i.e. an inline-code span that was stripped. Also report any bare <Tag> in prose.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAPTERS_DIR = os.path.join(REPO, "docs", "chapters")

fence_re = re.compile(r"^\s*```")
# bare <X> or </X> in prose (uppercase tag)
tag_re = re.compile(r"<(?:\/?[A-Z][A-Za-z0-9]*)(?:\s[^>]*)?>")

total_double = 0
total_tag = 0
for i in range(1, 15):
    fn = "chapter%02d.md" % i
    path = os.path.join(CHAPTERS_DIR, fn)
    if not os.path.exists(path):
        print("MISSING", fn); continue
    in_fence = False
    for lnno, ln in enumerate(open(path, encoding="utf-8"), 1):
        if fence_re.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # strip trailing newline
        s = ln.rstrip("\n")
        # true mid-line double space: non-space, two spaces, non-space
        for m in re.finditer(r"\S  \S", s):
            total_double += 1
            print("[DOUBLE %s:%d] %s" % (fn, lnno, s))
            break
        # bare tag (only flag if not already escaped &amp; &lt;)
        for m in tag_re.finditer(s):
            # ignore if part of an already-escaped entity
            if "&lt;" in s or "&gt;" in s:
                continue
            total_tag += 1
            print("[TAG %s:%d] %s" % (fn, lnno, s))
            break

print("\nTRUE mid-line double-space hits:", total_double)
print("BARE <Tag> hits:", total_tag)
