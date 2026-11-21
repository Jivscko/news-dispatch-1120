"""Drawing primitives: fonts, wrapping, tracked capitals, tints."""

import os

from PIL import ImageFont

from news_data import PAPER

FONTS = {
    "serif_b": [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ],
    "sans_b": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ],
    "narrow_b": [
        "/usr/share/fonts/opentype/urw-base35/NimbusSansNarrow-Bold.otf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
}

_cache = {}


def font(slot, size):
    """Cached truetype object; falls back through the slot's path list."""
    key = (slot, size)
    if key not in _cache:
        chosen = None
        for path in FONTS[slot]:
            if os.path.exists(path):
                chosen = path
                break
        if chosen is None:
            raise RuntimeError("no font available for slot %r" % slot)
        _cache[key] = ImageFont.truetype(chosen, size)
    return _cache[key]


def wrap(draw, text, face, width):
    """Greedy word wrap measured against real glyph widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=face) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def caps(draw, xy, text, face, fill, track=0.0):
    """Draw tracked capitals, returning the advance width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=face, fill=fill)
        x += draw.textlength(ch, font=face) + track
    return x - xy[0]


def caps_width(draw, text, face, track=0.0):
    if not text:
        return 0.0
    return sum(draw.textlength(ch, font=face) + track for ch in text) - track


def caps_centred(draw, y, text, face, fill, track=0.0, width=1024, x0=0):
    w = caps_width(draw, text, face, track)
    return caps(draw, (x0 + (width - w) / 2, y), text, face, fill, track)


def wrap_caps(draw, text, face, width, track=0.0):
    """Wrap a capitals string by tracked width."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if caps_width(draw, trial, face, track) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, slot, width, start, floor=8, track=0.0):
    """Largest font size at which `text` fits `width`."""
    size = start
    while size > floor:
        face = font(slot, size)
        if draw.textlength(text, font=face) + track * len(text) <= width:
            return face
        size -= 1
    return font(slot, floor)


def tint(section, weight):
    """Paper mixed with a section colour, for card washes."""
    base = PAPER
    return tuple(round(b * (1 - weight) + c * weight) for b, c in zip(base, section))


def hairline(draw, x0, y0, x1, y1, fill, width=1):
    draw.line([(x0, y0), (x1, y1)], fill=fill, width=width)


def dotted(draw, x0, y0, x1, y1, fill, step=6):
    """Deterministic dotted rule."""
    span = x1 - x0
    n = max(1, int(span // step))
    for i in range(n + 1):
        x = x0 + i * step
        draw.rectangle([x, y0, min(x + 2, x1), y0], fill=fill)
