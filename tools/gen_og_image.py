#!/usr/bin/env python3
"""Generate a 1200x630 Open Graph share card (raster PNG) for the mapcn-book site.

Social crawlers (Twitter/X, Facebook, LinkedIn, Slack, Discord) reject SVG og:image,
so we ship a real raster PNG. Design follows mapcn's minimal monochrome + teal accent
language: light gradient field, faint route lines, a teal map pin, and the book title.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OUT = sys.argv[1] if len(sys.argv) > 1 else "docs/public/og-cover.png"

FONT_DIR = "C:/Windows/Fonts"
REG = f"{FONT_DIR}/msyh.ttc"      # Microsoft YaHei (regular face index 0)
BOLD = f"{FONT_DIR}/msyhbd.ttc"   # Microsoft YaHei Bold

# Brand palette (consistent with site theme-color #0F766E)
TEAL = (15, 118, 110)
TEAL_DK = (13, 94, 88)
SLATE_900 = (15, 23, 42)
SLATE_600 = (71, 85, 105)
SLATE_500 = (100, 116, 139)
LINE = (203, 213, 225)   # slate-300


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def vgrad(draw, top, bottom):
    """Vertical gradient by drawing 1px-tall horizontal lines."""
    for y in range(H):
        t = y / (H - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def curve(draw, pts, color, width, steps=80):
    """Draw a smooth curve through pts using chained quadratic segments."""
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        # approximate with line segments
        for s in range(steps):
            t0 = s / steps
            t1 = (s + 1) / steps
            ax = x0 + (mx - x0) * (3 * t0 * t0 - 2 * t0 * t0 * t0)
            ay = y0 + (my - y0) * (3 * t0 * t0 - 2 * t0 * t0 * t0)
            bx = x0 + (mx - x0) * (3 * t1 * t1 - 2 * t1 * t1 * t1)
            by = y0 + (my - y0) * (3 * t1 * t1 - 2 * t1 * t1 * t1)
            draw.line([(ax, ay), (bx, by)], fill=color, width=width)


def draw_pin(draw, cx, cy, size, color):
    """Teardrop map pin: head circle + downward tip + inner white dot."""
    r = size / 2
    head_cy = cy - size * 0.32
    # head
    draw.ellipse([cx - r, head_cy - r, cx + r, head_cy + r], fill=color)
    # tip
    draw.polygon(
        [(cx - r * 0.78, head_cy + r * 0.35),
         (cx + r * 0.78, head_cy + r * 0.35),
         (cx, cy + size * 0.55)],
        fill=color,
    )
    # inner dot
    ir = r * 0.40
    draw.ellipse([cx - ir, head_cy - ir, cx + ir, head_cy + ir], fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    vgrad(d, (248, 250, 252), (226, 232, 240))  # slate-50 -> slate-200

    # Faint route lines — keep them above or below the text block for clarity
    routes = [
        [(60, 110), (300, 85), (520, 145), (760, 100), (950, 125)],
        [(40, 165), (260, 140), (500, 200), (740, 150)],
        [(60, 540), (220, 570), (380, 540)],
    ]
    for rt in routes:
        curve(d, rt, LINE, 5)

    # Pin dots at route ends (teal)
    for (x, y) in [(950, 125), (740, 150), (380, 540)]:
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=TEAL)

    # Big hero pin on the left
    draw_pin(d, 250, 330, 150, TEAL)

    # Text block (right of pin), keep within right margin
    tx = 460
    f_title = font(BOLD, 62)
    f_sub = font(REG, 30)
    f_small = font(REG, 22)

    d.text((tx, 235), "Mapcn 从入门到进阶", font=f_title, fill=SLATE_900)
    d.text((tx, 318), "基于官方文档的系统性实战指南", font=f_sub, fill=SLATE_600)
    d.text((tx, 370),
           "MapLibre GL · React 地图组件库 · 14 章实战",
           font=f_small, fill=SLATE_500)

    # Thin teal divider
    d.line([(tx, 425), (tx + 640, 425)], fill=TEAL, width=4)

    # Site url footer
    f_url = font(REG, 24)
    d.text((tx, 452), "maicarons.github.io/mapcn-book", font=f_url, fill=TEAL_DK)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
