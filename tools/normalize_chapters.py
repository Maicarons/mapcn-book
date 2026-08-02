#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize the book chapter markdown files for VitePress (idempotent).

Fixes / guarantees:
  * Every chapter has exactly one top-level H1 of the form
    "# 第 NN 章 <title>" (zero-padded for < 10), regardless of whatever the
    author originally wrote.
  * Heading levels are consistent: if the shallowest real (non-code) heading
    is deeper than H1, all headings are promoted so the title becomes H1.
Code fences are tracked so in-code "# comments" are never treated as headings.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAPTERS_DIR = os.path.join(REPO, "docs", "chapters")


def normalize(text: str, num: int) -> str:
    lines = text.split("\n")

    # Pass 1: find min heading level among REAL (non-code) headings.
    in_code = False
    levels = []
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s", ln)
        if m:
            levels.append(len(m.group(1)))
    minlvl = min(levels) if levels else 1
    promo = minlvl - 1  # shift everything up so the top heading becomes H1

    # Pass 2: transform.
    out = []
    in_code = False
    title_rewritten = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code:
            out.append(ln)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m and not title_rewritten:
            lvl = len(m.group(1)) - promo
            if lvl < 1:
                lvl = 1
            content = m.group(2).strip()
            # strip any existing "第 N 章 / 第N章 / N." prefix
            cleaned = re.sub(r"^第\s*\d+\s*[.章]?\s*", "", content).strip()
            cleaned = re.sub(r"^\d+\.\s*", "", cleaned).strip()
            new_title = "第 %02d 章 %s" % (num, cleaned)
            out.append("# %s" % new_title)
            title_rewritten = True
        elif m:
            lvl = len(m.group(1)) - promo
            if lvl < 1:
                lvl = 1
            out.append("%s %s" % ("#" * lvl, m.group(2).strip()))
        else:
            out.append(ln)
    return "\n".join(out)


def main():
    for fn in sorted(os.listdir(CHAPTERS_DIR)):
        m = re.match(r"^chapter(\d+)\.md$", fn)
        if not m:
            continue
        num = int(m.group(1))
        path = os.path.join(CHAPTERS_DIR, fn)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        new = normalize(text, num)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print("%s -> %s" % (fn, new.split("\n", 1)[0]))


if __name__ == "__main__":
    main()
