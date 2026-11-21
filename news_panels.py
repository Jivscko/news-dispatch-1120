"""Editorial illustration for the lead, and the Anthropic direction chart."""

from news_art import caps, font
from news_data import GREY, INK, LIGHT, MID, PAPER, PAPER_DARK, RIVER, SECTIONS


def lead_picture(d, box, section):
    """Drawn scene: a broken bridge span over a river under smoke and streaks."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cap_h = 20
    bottom = y1 - cap_h
    d.rectangle([x0, y0, x1, bottom], fill=PAPER_DARK)
    d.rectangle([x0, bottom, x1, y1], fill=PAPER)
    d.line([(x0, bottom), (x1, bottom)], fill=INK, width=1)

    body = bottom - y0
    deck_y = y0 + int(body * 0.46)
    river_y = deck_y + 5
    gap_c = x0 + int(w * 0.48)
    gap_w = int(w * 0.12)

    # sky: soft horizontal bands to keep the field from going flat
    for i, tone in enumerate(((238, 231, 216), (243, 237, 223), (247, 241, 228))):
        yy0 = y0 + int(body * i / 3.0)
        yy1 = y0 + int(body * (i + 1) / 3.0)
        if yy0 >= deck_y:
            continue
        d.rectangle([x0 + 1, yy0, x1 - 1, min(yy1, deck_y)], fill=tone)
    for i in range(3):
        yy = y0 + 12 + i * 13
        d.line([(x0 + 20 + i * 9, yy), (x0 + 150 + i * 21, yy)], fill=(228, 220, 204), width=2)

    # far and near skyline, kept as silhouettes for depth
    def skyline(bx, count, base, tone, seed):
        for i in range(count):
            bw = 12 + (i * 3 + seed) % 7
            bh = 12 + ((i * 11 + seed * 5) % 5) * 8
            rx = bx + i * (bw + 3)
            if rx + bw > x1 - 10:
                break
            d.rectangle([rx, base - bh, rx + bw, base], fill=tone)
        d.line([(bx - 4, base), (min(bx + count * 17, x1 - 8), base)], fill=(150, 143, 130))

    skyline(x0 + 14, 7, deck_y, (216, 208, 193), 1)
    skyline(gap_c + gap_w // 2 + 14, 9, deck_y, (208, 199, 183), 3)

    # river
    d.rectangle([x0 + 6, river_y, x1 - 6, bottom - 4], fill=RIVER)
    d.line([(x0 + 6, river_y), (x1 - 6, river_y)], fill=(150, 164, 164), width=1)
    for i in range(1, 6):
        yy = river_y + i * (bottom - 4 - river_y) // 6
        inset = 14 + i * 6
        d.line([(x0 + inset, yy), (x1 - inset - 10, yy)], fill=(204, 212, 210), width=1)
    for i in range(9):
        rx = x0 + 40 + i * 57
        ry = river_y + 8 + (i % 4) * 9
        d.line([(rx, ry), (rx + 16, ry)], fill=(212, 219, 216), width=2)

    # bridge deck: two segments, a destroyed middle, piers and cables
    for sx0, sx1 in ((x0 + 8, gap_c - gap_w // 2), (gap_c + gap_w // 2, x1 - 8)):
        d.rectangle([sx0, deck_y, sx1, deck_y + 6], fill=INK)
        d.rectangle([sx0, deck_y + 6, sx1, deck_y + 9], fill=(70, 65, 58))
    for frac in (0.08, 0.20, 0.33, 0.42, 0.62, 0.72, 0.84, 0.94):
        px = x0 + int(w * frac)
        if gap_c - gap_w // 2 - 8 < px < gap_c + gap_w // 2 + 8:
            continue
        d.rectangle([px - 2, deck_y + 9, px + 2, river_y + 20], fill=(56, 52, 46))
        d.line([(px, deck_y + 2), (px + 20, deck_y - 34)], fill=(122, 116, 105), width=1)

    # broken span stubs and a fallen plate
    d.polygon([(gap_c - gap_w // 2, deck_y), (gap_c - gap_w // 2 + 20, deck_y + 4),
               (gap_c - gap_w // 2 + 12, deck_y + 16), (gap_c - gap_w // 2 - 3, deck_y + 10)],
              fill=INK)
    d.polygon([(gap_c + gap_w // 2, deck_y), (gap_c + gap_w // 2 - 18, deck_y + 3),
               (gap_c + gap_w // 2 - 11, deck_y + 16), (gap_c + gap_w // 2 + 4, deck_y + 9)],
              fill=INK)
    d.polygon([(gap_c - 18, river_y + 12), (gap_c + 14, river_y + 9),
               (gap_c + 20, river_y + 20), (gap_c - 12, river_y + 22)], fill=(66, 61, 54))
    d.line([(gap_c - 14, river_y + 11), (gap_c + 12, river_y + 9)], fill=(150, 143, 128), width=1)

    # smoke columns, pale to dark, leaning over the gap
    for cx, topf in ((gap_c - 34, 0.10), (gap_c + 4, 0.00), (gap_c + 40, 0.14)):
        for j, (rw, rh, tone) in enumerate((
                (40, 17, (206, 200, 188)), (31, 14, (178, 172, 160)),
                (22, 11, (146, 140, 130)), (13, 8, (112, 106, 98)))):
            cy = y0 + int(body * topf) + j * 15
            d.ellipse([cx - rw + j * 4, cy - rh, cx + rw + j * 4, cy + rh], fill=tone)

    # missile streaks from the upper right, aimed at the gap
    for sx, sy, ex, ey in ((0.70, 0.02, 0.520, 0.30), (0.82, 0.05, 0.575, 0.26),
                           (0.93, 0.00, 0.640, 0.22)):
        ax, ay = x0 + int(w * sx), y0 + int(body * sy)
        bx, by = x0 + int(w * ex), y0 + int(body * ey)
        d.line([(ax, ay), (bx, by)], fill=SECTIONS["justice"], width=3)
        d.line([(ax - 12, ay + 4), (ax, ay)], fill=(206, 120, 118), width=1)
        d.polygon([(bx, by), (bx + 8, by - 11), (bx - 3, by - 8)], fill=SECTIONS["justice"])

    # caption strip
    f = font("sans_b", 8)
    caps(d, (x0 + 8, y1 - 14), "KYIV / BRIDGES OF THE CAPITAL / ILLUSTRATION", f, GREY, 0.4)
    right = "20 NOV 2026"
    d.text((x1 - 8 - d.textlength(right, font=f), y1 - 14), right, font=f, fill=GREY)


def direction_chart(d, box):
    """Red falling line, presented strictly as direction - no percentage."""
    x0, y0, x1, y1 = box
    red = SECTIONS["justice"]
    d.rectangle(box, fill=PAPER)
    d.rectangle([x0, y0, x1, y1], outline=LIGHT, width=1)
    d.rectangle([x0, y0, x0 + 4, y1], fill=SECTIONS["market"])

    f = font("sans_b", 9)
    caps(d, (x0 + 12, y0 + 6), "09 / MARKETS", f, SECTIONS["market"], 1.0)
    caps(d, (x0 + 12, y0 + 18), "ANTHROPIC, FIRST DAY OF TRADING", font("sans_b", 7.5),
         GREY, 0.4)

    px0, py0, px1, py1 = x0 + 16, y0 + 32, x1 - 30, y1 - 18
    d.line([(px0, py0), (px0, py1)], fill=MID, width=1)
    d.line([(px0, py1), (px1, py1)], fill=MID, width=1)
    for i in range(1, 4):
        yy = py0 + i * (py1 - py0) // 4
        d.line([(px0, yy), (px1, yy)], fill=(222, 216, 204), width=1)

    pts = [(0.00, 0.08), (0.13, 0.24), (0.25, 0.18), (0.38, 0.42),
           (0.52, 0.36), (0.63, 0.60), (0.76, 0.55), (0.88, 0.78), (1.00, 0.92)]
    xy = [(px0 + t * (px1 - px0), py0 + v * (py1 - py0)) for t, v in pts]
    d.line(xy, fill=red, width=3, joint="curve")
    ax, ay = xy[-1]
    d.polygon([(ax + 7, ay + 3), (ax - 10, ay - 3), (ax - 2, ay - 11)], fill=red)
    d.ellipse([xy[0][0] - 3, xy[0][1] - 3, xy[0][0] + 3, xy[0][1] + 3], fill=INK)

    d.rectangle([x1 - 72, y0 + 28, x1 - 16, y0 + 41], fill=PAPER)
    caps(d, (x1 - 68, y0 + 30), "FALLING", font("sans_b", 10), red, 0.8)
    caps(d, (x0 + 12, y1 - 11), "DIRECTION ONLY / NO % REPORTED", font("sans_b", 7),
         MID, 0.3)
