#!/usr/bin/env python3
"""Render entry.png: a newspaper front page for Friday, 20 November 2026.

Standard-library + Pillow only, no network, no external assets, fully
deterministic (no random values). Run:  python3 render_news.py
"""

import datetime
import os

from PIL import Image, ImageDraw, ImageFont

# The date is the anchor of the whole page; fail loudly if it ever moves.
assert datetime.date(2026, 11, 20).strftime("%A") == "Friday"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 36
PAPER = (245, 241, 230)
INK = (26, 26, 26)
RED = (168, 28, 38)
GREY = (88, 82, 74)
FAINT = (196, 188, 174)
RULE = (42, 38, 32)

FONT_PATHS = {
    "serif_bold": [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def load_font(family, size):
    for path in FONT_PATHS[family]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, font, max_width):
    """Greedy word wrap against real font metrics."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, family, max_width, start, floor=18, tracking=0.0):
    """Largest size at which `text` fits `max_width`."""
    size = start
    while size > floor:
        font = load_font(family, size)
        width = draw.textlength(text, font=font) + tracking * len(text)
        if width <= max_width:
            return font
        size -= 1
    return load_font(family, floor)


def centred(draw, y, text, font, fill, width=W, x0=0, tracking=0.0):
    if tracking:
        total = sum(draw.textlength(ch, font=font) + tracking for ch in text) - tracking
        x = x0 + (width - total) / 2
        for ch in text:
            draw.text((x, y), ch, font=font, fill=fill)
            x += draw.textlength(ch, font=font) + tracking
        return total
    w = draw.textlength(text, font=font)
    draw.text((x0 + (width - w) / 2, y), text, font=font, fill=fill)
    return w


class Pen:
    """Draw helpers in a normalised 100x100 box, so icons scale cleanly."""

    def __init__(self, draw, x, y, size, color=INK, scale=1.0):
        self.d = draw
        self.x = x
        self.y = y
        self.s = size / 100.0
        self.color = color
        self.scale = scale

    def _p(self, px, py):
        return (self.x + px * self.s, self.y + py * self.s)

    def line(self, pts, width=None, color=None):
        w = width if width is not None else max(2, int(7 * self.s))
        self.d.line([self._p(px, py) for px, py in pts], fill=color or self.color, width=w, joint="curve")

    def rect(self, x0, y0, x1, y1, width=None, color=None, fill=None):
        w = width if width is not None else max(2, int(6 * self.s))
        self.d.rectangle(
            [self._p(x0, y0), self._p(x1, y1)],
            outline=None if fill is not None and width == 0 else (color or self.color),
            width=w,
            fill=fill,
        )

    def box(self, x0, y0, x1, y1, fill):
        self.d.rectangle([self._p(x0, y0), self._p(x1, y1)], fill=fill)

    def ellipse(self, x0, y0, x1, y1, width=None, color=None, fill=None):
        w = width if width is not None else max(2, int(6 * self.s))
        self.d.ellipse(
            [self._p(x0, y0), self._p(x1, y1)],
            outline=color or self.color,
            width=w,
            fill=fill,
        )

    def poly(self, pts, color=None, fill=None, width=None):
        if fill is not None:
            self.d.polygon([self._p(px, py) for px, py in pts], fill=fill)
        if width is not None:
            self.line(pts + [pts[0]], width=width, color=color)

    def text(self, px, py, msg, size, fill=None, family="sans_bold", anchor="mm"):
        font = load_font(family, max(8, int(size * self.s * 1.6)))
        self.d.text(self._p(px, py), msg, font=font, fill=fill or self.color, anchor=anchor)


# ---------------------------------------------------------------- icons


def icon_servers(p):
    """Federal tech outage: server racks with a fault marker."""
    for top in (18, 44):
        p.rect(16, top, 62, top + 20, width=5)
        p.line([(24, top + 7), (36, top + 7)], width=4)
        p.ellipse(50, top + 5, 56, top + 11, width=4)
        p.line([(24, top + 14), (34, top + 14)], width=4)
    p.line([(62, 28), (74, 28)], width=4)
    p.line([(68, 22), (80, 34)], width=7, color=RED)
    p.line([(80, 22), (68, 34)], width=7, color=RED)
    p.line([(12, 74), (84, 74)], width=5)


def icon_bridge(p):
    """Missile barrage on Kyiv bridges: broken span, falling missile."""
    p.line([(8, 74), (36, 74)], width=6)
    p.line([(64, 74), (92, 74)], width=6)
    p.line([(8, 74), (8, 88)], width=5)
    p.line([(92, 74), (92, 88)], width=5)
    p.line([(14, 74), (26, 52)], width=4)
    p.line([(86, 74), (74, 52)], width=4)
    p.line([(26, 52), (44, 58)], width=4)
    p.line([(74, 52), (58, 60)], width=4)
    # falling missile
    p.poly([(48, 8), (56, 20), (50, 26), (42, 20)], fill=INK)
    p.line([(46, 27), (44, 38)], width=4)
    p.line([(52, 27), (54, 38)], width=4)
    # blast sparks
    p.line([(30, 40), (36, 46)], width=3, color=RED)
    p.line([(64, 36), (70, 42)], width=3, color=RED)
    p.line([(46, 44), (50, 52)], width=3, color=RED)


def icon_energy(p):
    """Senate energy bill: capitol columns and a bolt."""
    p.line([(16, 26), (50, 10), (84, 26)], width=4)
    for x in (26, 40, 54, 68):
        p.line([(x, 32), (x, 64)], width=4)
    p.line([(16, 70), (84, 70)], width=4)
    p.line([(12, 78), (88, 78)], width=4)
    p.poly([(54, 34), (44, 56), (52, 56), (46, 74), (62, 50), (53, 50)], fill=RED)


def icon_clock(p):
    """Execution lasting more than an hour: a clock with a long hand."""
    p.ellipse(16, 16, 84, 84, width=6)
    p.ellipse(45, 45, 55, 55, width=4)
    for a, b in (((50, 16), (50, 25)), ((84, 50), (75, 50)),
                 ((50, 84), (50, 75)), ((16, 50), (25, 50))):
        p.line([a, b], width=4)
    p.line([(50, 50), (50, 27)], width=5)
    p.line([(50, 50), (74, 60)], width=6, color=RED)
    p.text(50, 92, "1 HR +", 11, fill=RED)


def icon_shell(p):
    """Delayed detonation of lead explosives: shell casing and halt mark."""
    p.poly([(50, 10), (64, 30), (64, 78), (36, 78), (36, 30)], width=4)
    p.line([(36, 66), (64, 66)], width=3)
    p.line([(36, 40), (64, 40)], width=3)
    p.line([(26, 88), (74, 88)], width=5)
    p.text(50, 84, "HALT", 9, fill=RED)


def icon_bars(p):
    """Closing Rikers Island: prison bars behind a padlock."""
    p.rect(20, 18, 80, 82, width=5)
    for x in (34, 50, 66):
        p.line([(x, 18), (x, 82)], width=4)
    p.line([(20, 50), (80, 50)], width=3)
    p.ellipse(42, 44, 58, 60, width=4, fill=PAPER)
    p.rect(40, 56, 60, 72, width=4, fill=PAPER)
    p.line([(50, 60), (50, 66)], width=3)


def icon_uk_eu(p):
    """EU and UK reset relations: two linked discs with insignia."""
    p.ellipse(10, 24, 58, 72, width=5)
    p.ellipse(46, 28, 92, 74, width=5)
    p.text(34, 48, "EU", 13, fill=INK)
    p.text(70, 51, "UK", 13, fill=INK)
    p.line([(58, 50), (46, 50)], width=4, color=RED)


def icon_border(p):
    """Estonia closes its border: fence and a curtain line."""
    p.line([(12, 40), (88, 40)], width=5)
    p.line([(12, 62), (88, 62)], width=5)
    for x in (24, 44, 64, 84):
        p.line([(x, 26), (x, 84)], width=4)
    p.poly([(12, 12), (88, 12), (88, 26), (12, 26)], fill=RED)
    p.line([(12, 88), (88, 88)], width=3, color=GREY)


def icon_chart(p):
    """Anthropic IPO: a falling share price line."""
    p.line([(14, 14), (14, 86)], width=4)
    p.line([(14, 86), (88, 86)], width=4)
    p.line([(22, 28), (38, 42), (50, 34), (64, 58), (80, 72)], width=5, color=RED)
    p.poly([(70, 72), (84, 78), (80, 62)], fill=RED)
    p.line([(22, 14), (22, 86)], width=2, color=FAINT)
    p.line([(14, 28), (88, 28)], width=2, color=FAINT)


def icon_chip(p):
    """China's AI firms short of Nvidia chips: a chip with missing pins."""
    p.rect(26, 26, 74, 74, width=5)
    p.rect(40, 40, 60, 60, width=4)
    p.text(50, 50, "AI", 11, fill=INK)
    for y in (34, 50, 66):
        p.line([(14, y), (26, y)], width=4)
        p.line([(74, y), (86, y)], width=4)
    for x in (34, 50, 66):
        p.line([(x, 14), (x, 26)], width=4)
    # broken pin
    p.line([(50, 74), (50, 80)], width=4, color=RED)
    p.line([(46, 82), (54, 82)], width=3, color=RED)


# ---------------------------------------------------------------- page

STORIES = [
    {
        "section": "POLITICS",
        "head": "White House removes cyber-security chief after federal tech outages",
        "icon": icon_servers,
    },
    {
        "section": "ENERGY",
        "head": "Senate passes bipartisan energy bill amid green objections",
        "icon": icon_energy,
    },
    {
        "section": "JUSTICE",
        "head": "Texas execution takes more than an hour",
        "icon": icon_clock,
    },
    {
        "section": "DEFENCE",
        "head": "US Army delays explosives test after lawsuit",
        "icon": icon_shell,
    },
    {
        "section": "NEW YORK",
        "head": "Mamdani sets out plan to close Rikers Island jail",
        "icon": icon_bars,
    },
    {
        "section": "EUROPE",
        "head": "EU and UK agree to reset relations, ten years after Brexit",
        "icon": icon_uk_eu,
    },
    {
        "section": "BALTIC",
        "head": "Estonia to close Russian border; Moscow cries 'new Iron Curtain'",
        "icon": icon_border,
    },
    {
        "section": "MARKETS",
        "head": "Anthropic stock drops on first day of trading after IPO",
        "icon": icon_chart,
    },
    {
        "section": "TECH",
        "head": "China's AI firms face a shortage of Nvidia chips",
        "icon": icon_chip,
    },
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------
    d.line([(MARGIN, 26), (W - MARGIN, 26)], fill=RULE, width=3)
    kicker = load_font("sans_bold", 12)
    kx = MARGIN + d.textlength("NO. 11,220", font=kicker) + 26
    d.text((MARGIN, 34), "NO. 11,220", font=kicker, fill=GREY)
    d.text((kx, 34), "TWELVE PAGES", font=kicker, fill=GREY)
    right = "ONE DOLLAR"
    d.text((W - MARGIN - d.textlength(right, font=kicker), 34), right, font=kicker, fill=GREY)

    title = "THE WORLD DISPATCH"
    font = fit_font(d, title, "serif_bold", W - 2 * MARGIN, 82, floor=40)
    centred(d, 52, title, font, INK)

    d.line([(MARGIN, 146), (W - MARGIN, 146)], fill=RULE, width=2)
    date_font = load_font("sans_bold", 15)
    centred(d, 154, "FRIDAY, 20 NOVEMBER 2026 - GLOBAL EDITION", date_font, INK, tracking=1.6)
    d.line([(MARGIN, 180), (W - MARGIN, 180)], fill=RULE, width=2)

    # --- lead story ----------------------------------------------
    lead_top = 198
    col_l = 520
    d.text((MARGIN, lead_top), "WORLD  /  LEAD STORY", font=load_font("sans_bold", 13), fill=RED)
    lead_font = load_font("serif_bold", 50)
    lead_lines = [
        "Russia fires",
        "retaliatory missile",
        "barrage at Kyiv bridges",
    ]
    y = lead_top + 24
    for line in lead_lines:
        d.text((MARGIN, y), line, font=lead_font, fill=INK)
        y += 52

    sub_font = load_font("serif", 17)
    sub = (
        "Strikes hit crossings over the Dnipro on Friday as Moscow answered "
        "recent attacks; rescue crews worked the damaged spans."
    )
    y += 6
    for line in wrap(d, sub, sub_font, col_l)[:3]:
        d.text((MARGIN, y), line, font=sub_font, fill=GREY)
        y += 21

    d.text((MARGIN, y + 8), "BY OUR KYIV CORRESPONDENT", font=load_font("sans_bold", 11), fill=INK)
    d.line([(MARGIN, y + 26), (MARGIN + 220, y + 26)], fill=RED, width=2)

    # lead picture panel
    px0, py0, px1, py1 = 592, 188, W - MARGIN, 482
    d.rectangle([px0, py0, px1, py1], fill=(236, 230, 217), outline=RULE, width=2)
    icon_bridge(Pen(d, px0 + 86, py0 + 12, 224))
    d.line([(px0 + 12, py1 - 36), (px1 - 12, py1 - 36)], fill=FAINT, width=2)
    d.text((px0 + 12, py1 - 28), "KYIV: a damaged Dnipro crossing, Friday.", font=load_font("sans", 12), fill=GREY)

    # --- grid of remaining stories --------------------------------
    grid_top = 520
    grid_bottom = 958
    gutter_x = 24
    col_w = (W - 2 * MARGIN - 2 * gutter_x) / 3
    row_h = (grid_bottom - grid_top) / 3

    # section band between lead and grid
    band_y = 500
    band_font = load_font("sans_bold", 12)
    band = "THE REST OF THE DAY  -  NINE STORIES"
    band_w = d.textlength(band, font=band_font) + 1.5 * len(band)
    gap = 14
    d.line([(MARGIN, band_y + 18), ((W - band_w) / 2 - gap, band_y + 18)], fill=RULE, width=2)
    d.line([((W + band_w) / 2 + gap, band_y + 18), (W - MARGIN, band_y + 18)], fill=RULE, width=2)
    centred(d, band_y, band, band_font, RED, tracking=1.5)

    for idx, story in enumerate(STORIES):
        col, row = idx % 3, idx // 3
        x = MARGIN + col * (col_w + gutter_x)
        y = grid_top + row * row_h

        if col > 0:
            vx = MARGIN + col * (col_w + gutter_x) - gutter_x / 2
            d.line([(vx, y + 6), (vx, y + row_h - 10)], fill=FAINT, width=2)
        if row > 0:
            d.line([(MARGIN, y - 8), (W - MARGIN, y - 8)], fill=FAINT, width=2)

        d.line([(x, y + 3), (x + 30, y + 3)], fill=RED, width=3)
        d.text((x, y + 12), story["section"], font=load_font("sans_bold", 12), fill=RED)

        story["icon"](Pen(d, x + 2, y + 40, 66))

        head_font = load_font("serif_bold", 18)
        lines = wrap(d, story["head"], head_font, col_w - 84)
        if len(lines) > 4:
            raise AssertionError("headline does not fit the card: %r" % story["head"])
        ty = y + 32
        for line in lines:
            d.text((x + 82, ty), line, font=head_font, fill=INK)
            ty += 21

    # --- footer ---------------------------------------------------
    d.line([(MARGIN, 970), (W - MARGIN, 970)], fill=RULE, width=2)
    foot = load_font("sans", 11)
    d.text((MARGIN, 980), "THE WORLD DISPATCH", font=foot, fill=GREY)
    mid = "FRIDAY, 20 NOVEMBER 2026"
    d.text(((W - d.textlength(mid, font=foot)) / 2, 980), mid, font=foot, fill=GREY)
    page = "PAGE 1 OF 12"
    d.text((W - MARGIN - d.textlength(page, font=foot), 980), page, font=foot, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = main()
    print("wrote", path, os.path.getsize(path), "bytes")
