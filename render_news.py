#!/usr/bin/env python3
"""Front page for Friday, 20 November 2026.

Ten reported items, one page: lead story, a numeral strip, a world locator,
varied-size cards, a direction-only market chart and a full index.

Pillow only, no network, no external assets, deterministic output.
"""

import datetime
import os

from PIL import Image, ImageDraw

import news_data as D
from news_art import caps, caps_width, caps_centred, font, tint, wrap
from news_cards import draw_card
from news_map import map_panel
from news_panels import direction_chart, lead_picture

assert datetime.date(2026, 11, 20).strftime("%A") == "Friday"

W = H = 1024
M = 26
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")


def rule(d, y, width=2, fill=None):
    d.line([(M, y), (W - M, y)], fill=fill or D.RULE, width=width)


def masthead(d):
    """Shrunken nameplate: the lead, not the title, carries the page."""
    f = font("sans_b", 8)
    caps(d, (M, 18), "GLOBAL EDITION / TEN STORIES", f, D.GREY, 1.1)
    caps_width_right = caps_width(d, D.DATE_LONG, f, 1.1)
    caps(d, (W - M - caps_width_right, 18), D.DATE_LONG, f, D.GREY, 1.1)

    title = "THE WORLD DISPATCH"
    face = font("serif_b", 58)
    while caps_width(d, title, face, 3.0) > W - 2 * M and face.size > 30:
        face = font("serif_b", face.size - 1)
    caps_centred(d, 32, title, face, D.INK, 3.0, width=W)
    rule(d, 96, 3)
    rule(d, 102, 1)


def lead_block(d, y0):
    """Biggest thing on the page: headline, picture and deck for story 01."""
    sec = D.SECTIONS[D.LEAD["section"]]
    d.rectangle([M, y0, M + 5, y0 + 12], fill=sec)
    caps(d, (M + 12, y0 + 1), D.LEAD["kick"], font("sans_b", 10), sec, 1.4)

    face = font("serif_b", 64)
    for line in D.LEAD["lines"]:
        assert d.textlength(line, font=face) <= W - 2 * M, "lead line too wide"
    y = y0 + 20
    for line in D.LEAD["lines"]:
        d.text((M, y), line, font=face, fill=D.INK)
        y += 62

    top = y + 2
    lead_picture(d, (M, top, 610, top + 150), sec)

    dx, dw = 628, W - M - 628
    deck_face = font("serif", 16)
    dy = top + 2
    for line in wrap(d, D.LEAD["deck"], deck_face, dw)[:3]:
        d.text((dx, dy), line, font=deck_face, fill=D.GREY)
        dy += 20
    d.line([(dx, dy + 3), (W - M, dy + 3)], fill=D.LIGHT, width=1)
    dy += 10
    small = font("serif", 12)
    for line in wrap(d, D.LEAD["deck2"], small, dw)[:2]:
        d.text((dx, dy), line, font=small, fill=D.MID)
        dy += 15
    d.rectangle([dx, top + 132, W - M, top + 132], fill=sec)
    caps(d, (dx, top + 137), D.LEAD["src"], font("sans_b", 7.5), D.INK, 0.7)
    return top + 150


def numerals(d, y0, y1):
    """Strip of large figures, each labelled with the fact it measures."""
    rule(d, y0, 2)
    rule(d, y1, 2)
    n = len(D.NUMERALS)
    inner = (W - 2 * M) - 4 * 12
    cw = inner / n
    for i, (num, lab1, lab2) in enumerate(D.NUMERALS):
        x = M + i * (cw + 12)
        if i:
            d.line([(x - 6, y0 + 8), (x - 6, y1 - 8)], fill=D.LIGHT, width=1)
        face = font("serif_b", 46)
        d.text((x, y0 + 6), num, font=face, fill=D.INK)
        lf = font("sans_b", 7.5)
        caps(d, (x, y0 + 56), lab1, lf, D.GREY, 0.7)
        caps(d, (x, y0 + 67), lab2, lf, D.GREY, 0.7)


def index_rail(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=D.PAPER)
    d.rectangle([x0, y0, x1, y1], outline=D.LIGHT, width=1)
    d.rectangle([x0, y0, x0 + 4, y1], fill=D.INK)
    caps(d, (x0 + 12, y0 + 6), "INDEX / ALL TEN STORIES", font("sans_b", 8), D.INK, 1.0)
    d.line([(x0 + 12, y0 + 18), (x1 - 8, y0 + 18)], fill=D.LIGHT, width=1)

    sec_of = {k["num"]: k["section"] for k in D.STORIES}
    sec_of[1] = D.LEAD["section"]
    col_w = (x1 - x0 - 20) / 2
    for i, (num, slug) in enumerate(D.INDEX):
        col, row = i // 5, i % 5
        x = x0 + 12 + col * col_w
        y = y0 + 24 + row * 19
        nf = font("serif_b", 9)
        d.text((x, y), "%02d" % num, font=nf, fill=D.SECTIONS[sec_of[num]])
        d.text((x + 17, y + 1.5), slug, font=font("narrow_b", 8), fill=D.INK)


def footer(d, y0):
    rule(d, y0, 2)
    f = font("sans_b", 10)
    caps(d, (M, y0 + 8), D.DATE_LONG, f, D.INK, 1.0)
    rf = font("sans_b", 10)
    w = caps_width(d, D.ALL_DATED, rf, 1.0)
    caps(d, (W - M - w, y0 + 8), D.ALL_DATED, rf, D.INK, 1.0)
    small = font("sans_b", 7)
    caps(d, (M, y0 + 26), "THE WORLD DISPATCH / ONE PAGE / TWENTY-SECOND YEAR OF THE DISPATCH", small, D.GREY, 0.6)
    caps(d, (W - M - caps_width(d, "STORY 01 LEADS THIS PAGE", small, 0.6), y0 + 26),
         "STORY 01 LEADS THIS PAGE", small, D.GREY, 0.6)


def main():
    img = Image.new("RGB", (W, H), D.PAPER)
    d = ImageDraw.Draw(img)

    masthead(d)
    lead_bottom = lead_block(d, 110)

    ny0, ny1 = lead_bottom + 10, lead_bottom + 96
    numerals(d, ny0, ny1)

    top = ny1 + 10
    left, right = 640, 656
    draw_card(d, (M, top, left, top + 118), _story(D.FEATURE), "feature")
    for i, num in enumerate(D.MEDIUM):
        cx = M if i % 2 == 0 else M + 297 + 17
        cy = top + 126 + (i // 2) * 102
        draw_card(d, (cx, cy, cx + 297, cy + 94), _story(num), "medium")
    cw = (left - M - 3 * 9) / 4
    for i, num in enumerate(D.COMPACT):
        cx = M + i * (cw + 9)
        draw_card(d, (cx, top + 330, cx + cw, top + 440), _story(num), "compact")

    map_panel(d, (right, top, W - M, top + 200), 140)
    direction_chart(d, (right, top + 208, W - M, top + 308))
    index_rail(d, (right, top + 316, W - M, top + 440))

    footer(d, 956)
    img.save(OUT, format="PNG", optimize=True)
    return OUT


def _story(num):
    for s in D.STORIES:
        if s["num"] == num:
            return s
    raise KeyError(num)


if __name__ == "__main__":
    path = main()
    print("wrote", path, os.path.getsize(path), "bytes")
