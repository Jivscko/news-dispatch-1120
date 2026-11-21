"""World locator panel: ten numbered pins, one per reported story location."""

from news_art import caps, font
from news_data import GREY, INK, LIGHT, MID, PAPER, SECTIONS
from news_geo import LAT_BOTTOM, LAT_TOP, LAND, MAP_KEY, PINS


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * (y1 - y0)
    return x, y


def map_panel(d, box, map_h):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PAPER)
    d.rectangle([x0, y0, x1, y1], outline=LIGHT, width=1)
    d.rectangle([x0, y0, x1, y0 + 18], fill=(238, 233, 222))

    caps(d, (x0 + 8, y0 + 5), "THE DAY ON THE MAP", font("sans_b", 9), INK, 1.2)
    right = "10 PINS / 10 STORIES"
    d.text((x1 - 8 - d.textlength(right, font=font("sans_b", 7)), y0 + 6),
           right, font=font("sans_b", 7), fill=GREY)

    m = (x0 + 8, y0 + 24, x1 - 8, y0 + 24 + map_h)
    d.rectangle(m, fill=(237, 241, 238))

    # graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, LAT_TOP, m)
        d.line([(gx, m[1]), (gx, m[3])], fill=(226, 231, 226), width=1)
    for lat in range(-30, 61, 30):
        _, gy = project(-180, lat, m)
        d.line([(m[0], gy), (m[2], gy)], fill=(226, 231, 226), width=1)

    # land
    for ring in LAND:
        pts = [project(lon, lat, m) for lon, lat in ring]
        d.polygon(pts, fill=(205, 199, 184))
        d.line(pts + [pts[0]], fill=(150, 144, 130), width=1)

    # pins
    section_of = {1: "world", 2: "politics", 3: "energy", 4: "justice", 5: "justice",
                  6: "politics", 7: "world", 8: "world", 9: "market", 10: "market"}
    for num, lon, lat, dx, dy in PINS:
        tx, ty = project(lon, lat, m)
        bx, by = tx + dx, ty + dy
        d.line([(tx, ty), (bx, by)], fill=INK, width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=INK)
        col = SECTIONS[section_of[num]]
        d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=col, outline=PAPER, width=1)
        d.text((bx, by - 0.5), str(num), font=font("sans_b", 7), fill=PAPER, anchor="mm")

    # key
    ky = m[3] + 4
    for i, line in enumerate(MAP_KEY):
        d.text((x0 + 8, ky + i * 8), line, font=font("narrow_b", 7.5), fill=GREY)
    d.line([(x0 + 8, m[3] + 2), (x1 - 8, m[3] + 2)], fill=LIGHT, width=1)
    d.text((x0 + 8, y1 - 8), "LOCATOR / NOT TO SCALE", font=font("sans_b", 7), fill=MID)
