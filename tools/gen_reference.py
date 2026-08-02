#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate docs/reference/*.md study notes from docs-zh/*.md translations.

Each official-doc translation is repackaged as a "官方文档研读" reference page:
  * H1 rewritten to "<原标题>（官方文档研读）"
  * A short "研读说明" preamble linking it to the relevant book chapters
  * Bare capitalized <Component> in prose (outside code fences / inline code)
    are escaped to &lt;...&gt; so VitePress / Pandoc do not mis-parse them.

IMPORTANT: the escape step NEVER removes or rewrites inline-code spans. It walks
each line tracking both code-fence state and inline-backtick state, and only
rewrites a line when an actual escape occurred.

Internal links `./NN-topic(.md)` are remapped from the source numbering to the
output numbering (the book prepends an extra introduction chapter, shifting the
rest by +1), so cross-reference links resolve inside the published site.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC_DIR = os.path.join(REPO, "docs-zh")
REF_DIR = os.path.join(REPO, "docs", "reference")
os.makedirs(REF_DIR, exist_ok=True)

# (src_file, out_file, book_chapters_hint)
MAP = [
    ("00-introduction.md",   "01-introduction.md",   "第 1 章（初识 mapcn）"),
    ("01-installation.md",   "02-installation.md",   "第 2 章（环境准备与安装）"),
    ("02-basic-map.md",      "03-basic-map.md",      "第 3 章（你的第一张地图）"),
    ("03-controls.md",       "04-controls.md",       "第 4 章（地图控件与交互）"),
    ("04-markers.md",        "05-markers.md",        "第 5 章（标记点）"),
    ("05-popups.md",         "06-popups.md",         "第 6 章（弹窗与提示框）"),
    ("06-routes.md",         "07-routes.md",         "第 7 章（路线与路径规划）"),
    ("07-arcs.md",           "08-arcs.md",           "第 8 章（弧线连接）"),
    ("08-geojson.md",        "09-geojson.md",        "第 9 章（GeoJSON 与区域地图）"),
    ("09-clusters.md",       "10-clusters.md",       "第 10 章（海量点聚合）"),
    ("10-advanced-usage.md", "11-advanced-usage.md", "第 11–13 章（进阶与实战）"),
    ("11-api-reference.md",  "12-api-reference.md",  "全书组件速查"),
]

# source basename (no ext) -> output basename (no ext)
REMAP = {os.path.splitext(s)[0]: os.path.splitext(o)[0] for s, o, _ in MAP}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip("\n")
    return text


def _escape_line(ln: str) -> str:
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


def escape_angle_in_prose(text: str) -> str:
    """Escape capitalized <Component> tags that are NOT in code fences or inline code."""
    lines = text.split("\n")
    out = []
    in_fence = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        out.append(_escape_line(ln))
    return "\n".join(out)


def fix_links(text: str) -> str:
    """Remap ./src-name(.md) links to the corresponding output filenames."""
    def repl(m):
        lead, name, ext, trail = m.group(1), m.group(2), m.group(3), m.group(4)
        if name in REMAP:
            return "%s%s%s%s" % (lead, REMAP[name], ext, trail)
        return m.group(0)
    return re.sub(r"(\]\(\./)([A-Za-z0-9_\-]+?)(\.md)?(\))", repl, text)


def first_h1(text: str):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def main():
    for src_name, out_name, chapters in MAP:
        src = os.path.join(SRC_DIR, src_name)
        with open(src, encoding="utf-8") as f:
            body = f.read()
        body = strip_frontmatter(body)
        title = first_h1(body)
        body = re.sub(r"^#\s+.*$", "", body, count=1, flags=re.M).lstrip("\n")
        body = escape_angle_in_prose(body)
        body = fix_links(body)

        preamble = (
            f"> **研读说明**：本页为 mapcn 官方文档「{title}」的中文研读笔记，"
            f"内容以官方文档为基线整理，作为正文之外的查阅与补充。\n"
            f"> 相关正文：{chapters}。如与官方文档存在出入，请以官方文档为准。\n\n"
        )
        new_title = f"# {title}（官方文档研读）\n\n"
        out = new_title + preamble + body + "\n"
        with open(os.path.join(REF_DIR, out_name), "w", encoding="utf-8") as f:
            f.write(out)
        print("reference/%s  (from %s, title=%s)" % (out_name, src_name, title))


if __name__ == "__main__":
    main()
