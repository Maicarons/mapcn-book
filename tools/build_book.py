#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble all book chapters into one continuous Markdown manuscript.

  * Normalizes every chapter H1 to the form "第 X 章 <rest>".
  * Inserts 4 part dividers and raw-openxml page breaks for a proper book layout.
  * Prepends the preface and appends a disclaimer section.
Code fences are tracked so in-code "# comments" are never treated as headings.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CHAPTERS_DIR = os.path.join(REPO, "docs", "chapters")
PREFACE = os.path.join(REPO, "docs", "preface.md")
OUT_DIR = os.path.join(REPO, "manuscript")
os.makedirs(OUT_DIR, exist_ok=True)

# chapter number -> part title (inserted right before that chapter)
PARTS = {
    1: "第一部分 入门与环境",
    3: "第二部分 地图基础与交互",
    7: "第三部分 图形与数据",
    11: "第四部分 进阶与实战",
}

PAGE_BREAK = "\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n"


def normalize_chapter(text: str) -> str:
    lines = text.split("\n")
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
    promo = minlvl - 1

    out = []
    in_code = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code:
            out.append(ln)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1)) - promo
            if lvl < 1:
                lvl = 1
            content = m.group(2).strip()
            if lvl == 1:
                tm = re.match(r"^第?\s*(\d+)\s*[.章]?\s*(.*)$", content)
                if tm:
                    content = "第 %s 章 %s" % (tm.group(1), tm.group(2).strip())
            out.append("%s %s" % ("#" * lvl, content))
        else:
            out.append(ln)
    return "\n".join(out).strip()


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def main():
    nums = sorted(
        int(re.match(r"chapter(\d+)\.md", f).group(1))
        for f in os.listdir(CHAPTERS_DIR)
        if re.match(r"chapter(\d+)\.md", f)
    )

    parts = []
    preface = read(PREFACE).strip()
    parts.append(PAGE_BREAK + preface)

    for i in nums:
        if i in PARTS:
            parts.append(PAGE_BREAK + "# %s" % PARTS[i])
        ch = read(os.path.join(CHAPTERS_DIR, "chapter%02d.md" % i))
        ch = normalize_chapter(ch)
        parts.append(PAGE_BREAK + ch)

    disclaimer = """
# 版权与免责声明

本书《Mapcn 从入门到进阶》由 AI 辅助文档生成流程编撰，内容以 mapcn 项目官方文档为基线整理而成，仅供学习与技术参考之用。

mapcn 基于 MapLibre GL 构建，相关商标与版权归原权利人所有。本书不主张对 mapcn 或 MapLibre 的任何知识产权。

免责声明：尽管本书已尽量对照官方文档核验事实与语法，但软件版本演进迅速，文中个别参数、默认值或行为可能随版本更新而变化。在涉及生产环境的关键决策时，请务必以官方文档与社区的最新结论为准。因使用本书内容所导致的任何直接或间接后果，编撰方不承担责任。

—— 编撰团队，2026 年 8 月
"""
    parts.append(PAGE_BREAK + disclaimer.strip())

    body = "\n\n".join(parts)

    metadata = """---
title: Mapcn 从入门到进阶
subtitle: 基于 mapcn 官方文档的系统性实战指南
author: WorkBuddy 文档生成团队
date: 2026 年 8 月
lang: zh
---
"""
    out_path = os.path.join(OUT_DIR, "book.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(metadata + "\n" + body + "\n")
    print("Built", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
