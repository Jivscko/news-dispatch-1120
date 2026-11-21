"""Secondary story cards: one wide feature, four medium, four compact briefs."""

from news_art import caps, font, tint, wrap
from news_data import GREY, INK, LIGHT, MID, PAPER, SECTIONS

METRICS = {
    "feature": dict(pad=11, num=13, kick=9.5, head=26, lead=28, dek=11.5, src=8,
                    bar=6, lines=2),
    "medium": dict(pad=8, num=11, kick=8.5, head=16, lead=17.5, dek=9.5, src=7,
                   bar=4, lines=2),
    "compact": dict(pad=7, num=10, kick=7, head=12, lead=13.5, dek=8.5, src=7,
                    bar=3, lines=4),
}


def draw_card(d, box, story, style):
    m = METRICS[style]
    col = SECTIONS[story["section"]]
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=tint(col, 0.07))
    d.rectangle([x0, y0, x0 + m["bar"], y1], fill=col)
    d.rectangle([x0, y0, x1, y1], outline=LIGHT, width=1)

    tx = x0 + m["bar"] + m["pad"]
    tw = x1 - m["pad"] - tx
    y = y0 + m["pad"] - 1

    # number and kicker line
    num = "%02d" % story["num"]
    nf = font("serif_b", m["num"])
    d.text((tx, y - 1), num, font=nf, fill=col)
    nx = tx + d.textlength(num, font=nf) + 6
    kface = font("sans_b", m["kick"])
    caps(d, (nx, y + m["num"] * 0.18), story["kick"], kface, col, 0.6)
    y += m["num"] + 3

    # headline
    hface = font("serif_b", m["head"])
    hlines = wrap(d, story["head"], hface, tw)
    if len(hlines) > m["lines"]:
        smallest = font("serif_b", max(9, m["head"] - 3))
        hlines = wrap(d, story["head"], smallest, tw)
        if len(hlines) > m["lines"]:
            raise AssertionError("headline overflows %s card: %r" % (style, story["head"]))
        hface = smallest
    for line in hlines:
        d.text((tx, y), line, font=hface, fill=INK)
        y += m["lead"]

    # dek
    y += 1
    dface = font("serif", m["dek"])
    dlines = wrap(d, story["dek"], dface, tw)
    room = max(0, int((y1 - m["pad"] - y - m["src"] - 3) // (m["dek"] + 2)))
    for line in dlines[:min(2, room)]:
        d.text((tx, y), line, font=dface, fill=GREY)
        y += m["dek"] + 2

    # source line
    sface = font("sans_b", m["src"])
    src = "SOURCE: DAY FILE %02d / %s" % (story["num"], story["where"])
    while d.textlength(src, font=sface) > tw and m["src"] > 5:
        sface = font("sans_b", sface.size - 1)
        if sface.size <= 5:
            break
    d.text((tx, y1 - m["pad"] - sface.size + 1), src, font=sface, fill=MID)
