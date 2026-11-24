#!/usr/bin/env python3
"""THE DAY IN PICTURES — one day's world news as a hero-led cover.

Front page for Monday 23 November 2026, built to be read at a glance:
one big picture for the lead story, three pictured second stories, and
six more in large type. No network, no randomness, no timestamps: the
same tables always produce the same bytes.

Layout, top to bottom: navy masthead; the COP31 hero scene; the lead
headline and deck; three pictured second stories (NATO, markets,
Hormuz); an ALSO TODAY strip of six; a footer line. 1 + 3 + 6 = 10
stories, every one legible at about 300 pixels across.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 24
RIGHT = PAGE_W - EDGE

INK = (18, 18, 18)
PAPER = (255, 255, 255)
NAVY = (13, 38, 74)
NAVY_DARK = (9, 28, 56)
FLAG_RED = (176, 32, 32)
GOLD = (255, 196, 66)
MUTED = (105, 105, 105)
HAIRLINE = (40, 40, 40)
SEA = (44, 80, 116)
SEA_LIGHT = (64, 108, 144)

# Hero dusk palette.
SKY_TOP = (24, 30, 58)
SKY_MID = (74, 58, 88)
SKY_LOW = (198, 96, 58)
SUN = (232, 122, 54)
SUN_CORE = (246, 168, 92)
HILL = (30, 34, 54)
HALL = (214, 184, 138)
HALL_ROOF = (148, 50, 46)
WINDOW = (255, 214, 120)
CHAIR = (16, 16, 24)

FONT_DIRS = ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts")


def load_font(size, bold=False, serif=False):
    """Serif bold for display type, sans for body; DejaVu fallbacks."""
    if serif and bold:
        names = ("DejaVuSerif-Bold.ttf", "DejaVuSans-Bold.ttf")
    elif bold:
        names = ("DejaVuSans-Bold.ttf", "DejaVuSerif-Bold.ttf")
    elif serif:
        names = ("DejaVuSerif.ttf", "DejaVuSans.ttf")
    else:
        names = ("DejaVuSans.ttf", "DejaVuSerif.ttf")
    for name in names:
        for folder in FONT_DIRS:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap_text(text, font, max_width):
    """Greedy word wrap measured with the real font; never splits a word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(canvas, x, y, lines, font, fill, leading):
    """Draw stacked lines; return the y just below the last one."""
    for line in lines:
        canvas.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_rule(canvas, x0, x1, y, width=2):
    canvas.line([(x0, y), (x1, y)], fill=HAIRLINE, width=width)


def draw_kicker(canvas, x, y, text, size=15):
    font = load_font(size, bold=True)
    canvas.text((x, y), text, font=font, fill=FLAG_RED)
    return y + size + 5


# ---------------------------------------------------------------- stories

LEAD = {
    "kicker": "LEAD  •  ANTALYA",
    "head": "COP31 COLLAPSES AS EU REJECTS PACT WITH NO FOSSIL-FUEL LINE",
    "deck": (
        "The longest climate summit on record ends with no deal after "
        "the EU and island states refuse a pact that never names fossil "
        "fuels."
    ),
    "art_caption": "ANTALYA  •  THE TALKS COLLAPSE",
}

SECOND = [
    {
        "kicker": "BRUSSELS  •  NATO",
        "head": "NATO Council meets on Russian missile in Poland",
        "deck": (
            "Ministers gather after a Kh-101 missile fell near "
            "Nowy Lipowiec."
        ),
        "scene": "nato",
    },
    {
        "kicker": "TAIPEI  •  MARKETS",
        "head": "Asia braces as the AI rout rolls on",
        "deck": (
            "Taiwan's short-selling ban takes effect as the Kospi "
            "slides 3.7%."
        ),
        "scene": "markets",
    },
    {
        "kicker": "GULF  •  HORMUZ",
        "head": "Two more tankers burn in the Gulf",
        "deck": (
            "Ships catch fire after hitting mines, Iran's navy says."
        ),
        "scene": "hormuz",
    },
]

# Six more stories, each one line in large type.
ALSO = [
    ("LIBYA", "Sea drones hit a Russian corvette; it capsizes."),
    ("MEXICO", "11 killed in Sinaloa after cartel boss arrest."),
    ("USA", "Democrats win Congress, biggest win since 1992."),
    ("OKINAWA", "Shuri Castle's restored main hall opens."),
    ("GENEVA", "Gukesh defends the chess world title."),
    ("MOTOGP", "Marquez seals a record-tying eighth title."),
]

FOOTER = (
    "All stories first reported Monday 23 November 2026  •  "
    "Compiled from wire and press reports  •  THE DAY IN PICTURES"
)


# ---------------------------------------------------------------- sections

def paint_masthead(canvas):
    canvas.rectangle([0, 0, PAGE_W, 84], fill=NAVY)
    title_font = load_font(52, bold=True, serif=True)
    canvas.text((EDGE, 10), "THE DAY IN PICTURES", font=title_font, fill=PAPER)
    sub_font = load_font(13, bold=True)
    canvas.text((EDGE, 64), "ONE DAY  •  ONE PICTURE  •  EVERY STORY THAT MATTERED",
                font=sub_font, fill=(200, 210, 225))
    day_font = load_font(16, bold=True)
    date_font = load_font(22, bold=True)
    meta_font = load_font(13, bold=True)
    for text, font, y, fill in (
        ("MONDAY", day_font, 8, PAPER),
        ("23 NOVEMBER 2026", date_font, 28, GOLD),
        ("10 STORIES THAT MATTERED", meta_font, 58, PAPER),
    ):
        width = font.getlength(text)
        canvas.text((RIGHT - width, y), text, font=font, fill=fill)


def paint_hero(canvas, x0, y0, x1, y1):
    """Dusk over the Antalya conference hall: empty chairs, delegates
    walking away, a low sun over the bay. The collapse, in one picture."""
    w, h = x1 - x0, y1 - y0
    # Vertical dusk gradient in 24 bands.
    bands = 24
    for i in range(bands):
        t = i / (bands - 1)
        if t < 0.5:
            u = t / 0.5
            col = tuple(int(SKY_TOP[c] + (SKY_MID[c] - SKY_TOP[c]) * u)
                        for c in range(3))
        else:
            u = (t - 0.5) / 0.5
            col = tuple(int(SKY_MID[c] + (SKY_LOW[c] - SKY_MID[c]) * u)
                        for c in range(3))
        yb = y0 + i * h // bands
        ye = y0 + (i + 1) * h // bands
        canvas.rectangle([x0, yb, x1, ye], fill=col)
    # Low sun, right of centre, with a pale core.
    sx, sy, sr = x0 + w - 210, y0 + 66, 52
    canvas.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SUN)
    canvas.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=SUN_CORE)
    # Hills on the horizon.
    horizon = y1 - 118
    canvas.polygon([(x0, horizon + 30), (x0 + 180, horizon - 26),
                    (x0 + 360, horizon + 12), (x0 + 560, horizon - 34),
                    (x0 + 760, horizon + 6), (x1, horizon - 14),
                    (x1, y1), (x0, y1)], fill=HILL)
    # The conference hall: long low block, warm lit windows, red roof.
    hx0, hx1 = x0 + 60, x0 + w - 320
    hy0, hy1 = horizon - 52, horizon + 6
    canvas.rectangle([hx0, hy0, hx1, hy1], fill=HALL)
    canvas.rectangle([hx0 - 8, hy0 - 12, hx1 + 8, hy0], fill=HALL_ROOF)
    for i in range(9):
        wx = hx0 + 16 + i * 34
        canvas.rectangle([wx, hy0 + 14, wx + 16, hy0 + 34], fill=WINDOW)
    # Sea strip under the sun, with its reflection.
    canvas.rectangle([x0, horizon + 6, x1, y1 - 78], fill=SEA)
    for i, rw in enumerate((150, 110, 70)):
        ry = horizon + 16 + i * 10
        canvas.rectangle([sx - rw // 2, ry, sx + rw // 2, ry + 4],
                         fill=SUN_CORE)
    # Foreground terrace: a row of empty chairs, the collapse in one
    # picture. The terrace is a lighter slate than the chairs so the
    # silhouettes read; the legs stop above the caption bar.
    terrace = y1 - 78
    canvas.rectangle([x0, terrace, x1, y1], fill=(30, 32, 48))
    for i in range(5):
        cx = x0 + 90 + i * 170
        canvas.rectangle([cx, terrace - 30, cx + 64, terrace + 8],
                         fill=CHAIR)  # back
        canvas.rectangle([cx - 6, terrace + 8, cx + 70, terrace + 18],
                         fill=CHAIR)  # seat
        canvas.rectangle([cx + 4, terrace + 18, cx + 10, terrace + 48],
                         fill=CHAIR)
        canvas.rectangle([cx + 54, terrace + 18, cx + 60, terrace + 48],
                         fill=CHAIR)
    # Caption bar across the bottom of the picture.
    canvas.rectangle([x0, y1 - 28, x1, y1], fill=NAVY_DARK)
    caption_font = load_font(14, bold=True)
    canvas.text((x0 + 12, y1 - 24), LEAD["art_caption"],
                font=caption_font, fill=PAPER)


def paint_lead(canvas):
    y = 500
    y = draw_kicker(canvas, EDGE, y, LEAD["kicker"])
    head_font = load_font(40, bold=True, serif=True)
    head_lines = wrap_text(LEAD["head"], head_font, RIGHT - EDGE)
    y = draw_lines(canvas, EDGE, y, head_lines, head_font, INK, 46)
    deck_font = load_font(16)
    deck_lines = wrap_text(LEAD["deck"], deck_font, RIGHT - EDGE)
    draw_lines(canvas, EDGE, y + 4, deck_lines, deck_font, INK, 20)


def paint_vignette(canvas, kind, x0, y0, x1, y1):
    """A small drawn picture for a second story."""
    w, h = x1 - x0, y1 - y0
    if kind == "nato":
        canvas.rectangle([x0, y0, x1, y1], fill=NAVY)
        # A row of flags on poles, and a podium with microphones.
        flag_cols = [(0, 51, 153), (176, 32, 32), (255, 196, 66),
                     (255, 255, 255), (34, 120, 60)]
        for i, col in enumerate(flag_cols):
            fx = x0 + 24 + i * 56
            canvas.rectangle([fx, y0 + 18, fx + 3, y0 + 78], fill=PAPER)
            canvas.rectangle([fx + 3, y0 + 18, fx + 38, y0 + 44], fill=col)
        canvas.rectangle([x0 + w // 2 - 52, y0 + h - 34,
                          x0 + w // 2 + 52, y1], fill=NAVY_DARK)
        canvas.rectangle([x0 + w // 2 - 52, y0 + h - 40,
                          x0 + w // 2 + 52, y0 + h - 34], fill=GOLD)
        for mx in (x0 + w // 2 - 20, x0 + w // 2 + 16):
            canvas.line([(mx, y0 + h - 40), (mx - 8, y0 + h - 62)],
                        fill=PAPER, width=3)
            canvas.ellipse([mx - 14, y0 + h - 70, mx - 2, y0 + h - 58],
                           fill=PAPER)
    elif kind == "markets":
        canvas.rectangle([x0, y0, x1, y1], fill=(12, 16, 24))
        # Candlesticks falling left to right, then a red trend line.
        tops = [26, 34, 44, 52, 62, 74, 84]
        for i, top in enumerate(tops):
            bx = x0 + 22 + i * 40
            canvas.rectangle([bx, y0 + top, bx + 16, y0 + top + 26],
                             fill=FLAG_RED)
            canvas.line([(bx + 8, y0 + top - 8), (bx + 8, y0 + top + 34)],
                        fill=FLAG_RED, width=2)
        pts = [(x0 + 16, y0 + 22), (x0 + 90, y0 + 40), (x0 + 160, y0 + 52),
               (x0 + 230, y0 + 74), (x0 + w - 16, y0 + h - 18)]
        canvas.line(pts, fill=(255, 90, 70), width=4, joint="curve")
    elif kind == "hormuz":
        canvas.rectangle([x0, y0, x1, y1], fill=SEA)
        canvas.rectangle([x0, y0 + h - 34, x1, y1], fill=SEA_LIGHT)
        # Two tanker silhouettes, flames and smoke above the second.
        for tx, tw in ((x0 + 24, 96), (x0 + 150, 120)):
            canvas.rectangle([tx, y0 + h - 58, tx + tw, y0 + h - 34],
                             fill=(10, 10, 16))
            canvas.rectangle([tx + tw - 34, y0 + h - 78, tx + tw - 22,
                              y0 + h - 58], fill=(10, 10, 16))
        fx, fy = x0 + 200, y0 + h - 78
        for dx, dy, r in ((0, 0, 16), (16, -10, 12), (-14, -8, 11)):
            canvas.ellipse([fx + dx - r, fy + dy - r, fx + dx + r,
                            fy + dy + r], fill=(232, 122, 54))
        for dx, dy, r in ((-30, -34, 14), (-8, -48, 18), (16, -40, 12)):
            canvas.ellipse([fx + dx - r, fy + dy - r, fx + dx + r,
                            fy + dy + r], fill=(90, 90, 96))


def paint_second(canvas):
    col_w = 309
    gap_x = 16
    y0 = 676
    for index, story in enumerate(SECOND):
        x = EDGE + index * (col_w + gap_x)
        paint_vignette(canvas, story["scene"], x, y0, x + col_w, y0 + 112)
        y = draw_kicker(canvas, x, y0 + 120, story["kicker"], size=13)
        head_font = load_font(19, bold=True, serif=True)
        head_lines = wrap_text(story["head"], head_font, col_w)
        y = draw_lines(canvas, x, y, head_lines, head_font, INK, 22)
        deck_font = load_font(13)
        deck_lines = wrap_text(story["deck"], deck_font, col_w)[:3]
        draw_lines(canvas, x, y + 2, deck_lines, deck_font, INK, 15)


def paint_also(canvas):
    header_font = load_font(16, bold=True)
    canvas.text((EDGE, 904), "ALSO TODAY", font=header_font, fill=NAVY)
    label_font = load_font(15, bold=True)
    body_font = load_font(15)
    col_w = 476
    for index, (label, text) in enumerate(ALSO):
        col = index // 3
        row = index % 3
        x = EDGE + col * 500
        y = 926 + row * 21
        canvas.text((x, y), label, font=label_font, fill=FLAG_RED)
        lw = label_font.getlength(label)
        # Never let a line run into the next column: trim with an
        # ellipsis if the measured width would overflow the column.
        max_w = col_w - lw - 8
        while body_font.getlength(text) > max_w and len(text) > 4:
            text = text[:-2]
        if body_font.getlength(ALSO[index][1]) > max_w:
            text = text[:-1] + "…"
        canvas.text((x + lw + 8, y), text, font=body_font, fill=INK)


def paint_footer(canvas):
    font = load_font(11)
    width = font.getlength(FOOTER)
    canvas.text(((PAGE_W - width) / 2, 1006), FOOTER, font=font, fill=MUTED)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    canvas = ImageDraw.Draw(page)
    paint_masthead(canvas)
    paint_hero(canvas, EDGE, 92, RIGHT, 480)
    paint_lead(canvas)
    draw_rule(canvas, EDGE, RIGHT, 664)
    paint_second(canvas)
    draw_rule(canvas, EDGE, RIGHT, 896)
    paint_also(canvas)
    paint_footer(canvas)
    return page


def main(argv):
    target = argv[1] if len(argv) > 1 else "entry.png"
    folder = os.path.dirname(os.path.abspath(target))
    os.makedirs(folder, exist_ok=True)
    page = build_page()
    page.save(target, format="PNG")
    print("wrote {0} ({1}x{2})".format(target, PAGE_W, PAGE_H))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
