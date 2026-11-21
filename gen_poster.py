#!/usr/bin/env python3
"""Draw the 21 November 2026 front page with Pillow shapes only.

Every picture below is built from rectangles, ellipses, polygons and
lines drawn in code. Nothing is downloaded and nothing is random, so
running this file twice writes exactly the same bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
EDGE = 26

PAPER = (247, 242, 230)
CARD = (255, 252, 244)
INK = (24, 28, 38)
NAVY = (27, 44, 82)
RED = (193, 39, 45)
TEAL = (18, 116, 110)
AMBER = (214, 141, 28)
SKY = (198, 220, 235)
LAND = (232, 222, 158)
MUTED = (92, 96, 104)
WHITE = (255, 255, 255)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_width, leading=None):
    step = leading or int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.18)


def star_points(cx, cy, outer, inner, spikes=8):
    pts = []
    for i in range(spikes * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def arc_points(x0, y0, x1, y1, lift, steps=24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)
        pts.append((x, y))
    return pts


def little_missile(draw, cx, cy, angle_deg, body=RED):
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    nose = (cx + ux * 16, cy + uy * 16)
    tail = (cx - ux * 14, cy - uy * 14)
    left = (cx + px * 5, cy + py * 5)
    right = (cx - px * 5, cy - py * 5)
    draw.polygon([nose, left, tail, right], fill=body, outline=INK)
    fin1 = (tail[0] + px * 8 - ux * 4, tail[1] + py * 8 - uy * 4)
    fin2 = (tail[0] - px * 8 - ux * 4, tail[1] - py * 8 - uy * 4)
    draw.polygon([tail, fin1, fin2], fill=INK)


def warning_triangle(draw, cx, cy, size):
    pts = [(cx, cy - size), (cx - size, cy + size * 0.8), (cx + size, cy + size * 0.8)]
    draw.polygon(pts, fill=(250, 199, 44), outline=INK, width=3)
    fnt = font(SANS_BOLD, int(size * 1.1))
    w = draw.textlength("!", font=fnt)
    draw.text((cx - w / 2, cy - size * 0.55), "!", font=fnt, fill=INK)


# ---------------------------------------------------------------- lead map

def draw_lead_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY, outline=INK, width=2)

    poland = [
        (x0 + 42, y0 + 78), (x0 + 96, y0 + 38), (x0 + 190, y0 + 30),
        (x0 + 272, y0 + 52), (x0 + 300, y0 + 108), (x0 + 282, y0 + 190),
        (x0 + 222, y0 + 238), (x0 + 128, y0 + 244), (x0 + 60, y0 + 202),
        (x0 + 34, y0 + 132),
    ]
    draw.polygon(poland, fill=LAND, outline=INK, width=3)
    draw.text((x0 + 118, y0 + 112), "POLAND", font=font(SANS_BOLD, 27), fill=NAVY)
    wx, wy = x0 + 168, y0 + 152
    draw.ellipse([wx - 6, wy - 6, wx + 6, wy + 6], fill=RED, outline=INK, width=2)
    draw.text((wx - 62, wy - 8), "Warsaw", font=font(SANS, 15), fill=INK)

    # dashed eastern border
    bx = x0 + 322
    yy = y0 + 18
    while yy < y1 - 24:
        draw.line([(bx, yy), (bx, yy + 12)], fill=INK, width=3)
        yy += 20
    draw.text((bx + 8, y1 - 28), "EAST →", font=font(SANS_BOLD, 14), fill=INK)

    impacts = [(x0 + 238, y0 + 96), (x0 + 196, y0 + 196)]
    launches = [(x1 - 18, y0 + 44), (x1 - 12, y0 + 150)]
    for (lx, ly), (ix, iy) in zip(launches, impacts):
        draw.line(arc_points(lx, ly, ix, iy, 52), fill=RED, width=4)
        draw.polygon(star_points(ix, iy, 20, 8), fill=(250, 140, 40), outline=RED)
        draw.ellipse([ix - 4, iy - 4, ix + 4, iy + 4], fill=RED)
    little_missile(draw, x0 + 330, y0 + 58, 168)
    little_missile(draw, x0 + 300, y0 + 158, 178)

    # suspected drone: small cross with four rotors
    dx, dy = x0 + 120, y0 + 62
    draw.line([(dx - 13, dy - 13), (dx + 13, dy + 13)], fill=INK, width=3)
    draw.line([(dx - 13, dy + 13), (dx + 13, dy - 13)], fill=INK, width=3)
    for ox, oy in [(-13, -13), (13, -13), (-13, 13), (13, 13)]:
        draw.ellipse([dx + ox - 5, dy + oy - 5, dx + ox + 5, dy + oy + 5],
                     outline=INK, width=2)
    draw.text((dx - 34, dy + 18), "drone?", font=font(SANS_BOLD, 13), fill=INK)

    warning_triangle(draw, x1 - 34, y0 + 34, 20)
    draw.text((x0 + 14, y1 - 26), "2 missiles down inside Poland",
              font=font(SANS_BOLD, 15), fill=RED)


# ------------------------------------------------------------ grid pictures

def pic_courthouse(draw, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    left, right = cx - 86, cx + 86
    # tall pediment over four clear columns, scales standing in front
    draw.polygon([(left, y0 + 16), (cx, y0 + 1), (right, y0 + 16)],
                 fill=NAVY, outline=INK)
    draw.rectangle([left - 4, y0 + 16, right + 4, y0 + 21], fill=INK)
    for i in range(4):
        col_x = left + 10 + i * 42
        draw.rectangle([col_x, y0 + 23, col_x + 12, y1 - 8], fill=WHITE, outline=INK, width=2)
    draw.rectangle([left - 8, y1 - 8, right + 8, y1 - 2], fill=NAVY)
    sx = cx
    draw.line([(sx, y0 + 24), (sx, y1 - 10)], fill=AMBER, width=5)
    draw.line([(sx - 30, y0 + 28), (sx + 30, y0 + 28)], fill=AMBER, width=5)
    draw.ellipse([sx - 4, y0 + 20, sx + 4, y0 + 28], fill=AMBER, outline=INK)
    for px in (sx - 30, sx + 30):
        draw.line([(px, y0 + 28), (px - 9, y0 + 40)], fill=INK, width=2)
        draw.line([(px, y0 + 28), (px + 9, y0 + 40)], fill=INK, width=2)
        draw.arc([px - 11, y0 + 36, px + 11, y0 + 48], 0, 180, fill=INK, width=3)


def pic_deal(draw, box):
    x0, y0, x1, y1 = box
    # signed document
    draw.rectangle([x0 + 26, y0 + 6, x0 + 108, y1 - 6], fill=WHITE, outline=INK, width=2)
    for i in range(4):
        ly = y0 + 18 + i * 9
        draw.line([(x0 + 36, ly), (x0 + 98, ly)], fill=MUTED, width=2)
    draw.line([(x0 + 48, y1 - 24), (x0 + 62, y1 - 12), (x0 + 92, y1 - 30)],
              fill=TEAL, width=5)
    # circle of stars (EU) and a union flag block (UK)
    cx, cy, r = x1 - 52, (y0 + y1) // 2, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 60, 160), outline=INK, width=2)
    for i in range(8):
        a = 2 * math.pi * i / 8
        sx, sy = cx + 15 * math.cos(a), cy + 15 * math.sin(a)
        draw.polygon(star_points(sx, sy, 5, 2, spikes=5), fill=(250, 199, 44))
    draw.rectangle([x0 + 118, y0 + 12, x0 + 156, y0 + 34], fill=(160, 30, 44), outline=INK)
    draw.line([(x0 + 118, y0 + 23), (x0 + 156, y0 + 23)], fill=WHITE, width=4)
    draw.line([(x0 + 137, y0 + 12), (x0 + 137, y0 + 34)], fill=WHITE, width=4)
    draw.line([(x0 + 162, (y0 + y1) // 2), (cx - r - 6, (y0 + y1) // 2)],
              fill=TEAL, width=4)
    draw.polygon([(cx - r - 6, (y0 + y1) // 2 - 6), (cx - r - 6, (y0 + y1) // 2 + 6),
                  (cx - r + 4, (y0 + y1) // 2)], fill=TEAL)


def pic_market(draw, box):
    x0, y0, x1, y1 = box
    draw.line([(x0 + 14, y0 + 4), (x0 + 14, y1 - 10)], fill=INK, width=2)
    draw.line([(x0 + 14, y1 - 10), (x1 - 8, y1 - 10)], fill=INK, width=2)
    heights = [44, 36, 28, 18]
    for i, h in enumerate(heights):
        bx = x0 + 28 + i * 34
        draw.rectangle([bx, y1 - 10 - h, bx + 22, y1 - 10], fill=(120, 140, 170), outline=INK)
    pts = [(x0 + 24, y0 + 10), (x0 + 84, y0 + 22), (x0 + 140, y0 + 34), (x1 - 22, y1 - 18)]
    draw.line(pts, fill=RED, width=5)
    draw.polygon([(x1 - 22, y1 - 10), (x1 - 34, y1 - 24), (x1 - 12, y1 - 26)], fill=RED)
    draw.text((x1 - 62, y0 + 2), "-3.7%", font=font(SANS_BOLD, 20), fill=RED)


def pic_summit(draw, box):
    x0, y0, x1, y1 = box
    ty = y1 - 20
    seats = [(x0 + 62, (40, 90, 180), "USA"), ((x0 + x1) // 2, (200, 40, 44), "CHINA"),
             (x1 - 62, (90, 110, 160), "RUSSIA")]
    for sx, colour, label in seats:
        draw.ellipse([sx - 10, ty - 30, sx + 10, ty - 10], fill=(240, 205, 170), outline=INK)
        draw.rectangle([sx - 13, ty - 10, sx + 13, ty], fill=colour, outline=INK)
    draw.rectangle([x0 + 22, ty, x1 - 22, ty + 12], fill=(110, 78, 48), outline=INK)
    draw.rectangle([x0 + 34, ty + 12, x0 + 42, y1 - 1], fill=INK)
    draw.rectangle([x1 - 42, ty + 12, x1 - 34, y1 - 1], fill=INK)
    # name plates sit on the table front, clear of the heads
    for sx, _colour, label in seats:
        draw.rectangle([sx - 26, ty + 2, sx + 26, ty + 11], fill=WHITE, outline=INK)
        w = draw.textlength(label, font=font(SANS_BOLD, 8))
        draw.text((sx - w / 2, ty + 2), label, font=font(SANS_BOLD, 8), fill=INK)
    # empty speech bubble beside the middle seat: nothing agreed
    bcx = (x0 + x1) // 2 + 52
    bx0, by0, bx1, by1 = bcx - 22, y0 + 1, bcx + 22, y0 + 17
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=7, fill=WHITE, outline=MUTED, width=2)
    draw.text((bcx - 8, by0 + 1), "...", font=font(SANS_BOLD, 13), fill=MUTED)


def pic_cyclone(draw, box):
    x0, y0, x1, y1 = box
    cx, cy = x0 + 62, (y0 + y1) // 2
    for r in (26, 19, 12):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 330, fill=TEAL, width=5)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=TEAL)
    draw.text((cx - 24, y1 - 16), "AKVAN", font=font(SANS_BOLD, 12), fill=TEAL)
    # coastline and houses on the right
    draw.line([(x0 + 112, y0 + 6), (x0 + 150, y0 + 26), (x0 + 140, y0 + 44),
               (x0 + 172, y1 - 8)], fill=AMBER, width=4)
    for hx, hy in [(x0 + 178, y0 + 14), (x0 + 200, y0 + 30), (x0 + 182, y0 + 42)]:
        draw.rectangle([hx, hy, hx + 18, hy + 12], fill=WHITE, outline=INK)
        draw.polygon([(hx - 2, hy), (hx + 9, hy - 8), (hx + 20, hy)], fill=RED, outline=INK)
    for i in range(5):
        rx = x0 + 118 + i * 24
        draw.line([(rx, y0 + 8), (rx - 6, y0 + 20)], fill=(70, 120, 200), width=3)
    draw.line([(x0 + 150, y1 - 10), (x1 - 16, y1 - 10)], fill=RED, width=4)
    draw.polygon([(x1 - 16, y1 - 15), (x1 - 16, y1 - 5), (x1 - 4, y1 - 10)], fill=RED)


def pic_intercept(draw, box):
    x0, y0, x1, y1 = box
    # skyline, kept low so the RIYADH label stays readable above it
    base = y1 - 6
    towers = [(x0 + 16, 22), (x0 + 44, 32), (x0 + 76, 20), (x0 + 104, 36), (x0 + 140, 26)]
    for tx, th in towers:
        draw.rectangle([tx, base - th, tx + 22, base], fill=NAVY, outline=INK)
        draw.rectangle([tx + 5, base - th + 6, tx + 9, base - th + 11], fill=(250, 220, 120))
        draw.rectangle([tx + 13, base - th + 16, tx + 17, base - th + 21], fill=(250, 220, 120))
    draw.line([(x0 + 8, base), (x1 - 8, base)], fill=INK, width=3)
    # incoming missile and intercept burst
    draw.line(arc_points(x1 - 16, y0 + 8, x0 + 150, y0 + 26, 26), fill=RED, width=3)
    little_missile(draw, x1 - 34, y0 + 12, 195)
    bx, by = x0 + 150, y0 + 26
    draw.polygon(star_points(bx, by, 17, 7), fill=(250, 160, 50), outline=RED)
    draw.line([(x0 + 60, base - 6), (bx - 8, by + 8)], fill=TEAL, width=3)
    draw.text((x0 + 16, y0 + 2), "RIYADH", font=font(SANS_BOLD, 13), fill=NAVY)


# ------------------------------------------------------------------ panels

def panel(draw, box, accent):
    draw.rectangle(box, fill=CARD, outline=INK, width=2)
    x0, y0, x1, _ = box
    draw.rectangle([x0, y0, x1, y0 + 7], fill=accent)


def grid_cell(draw, box, kicker, accent, headline, caption, picture):
    panel(draw, box, accent)
    x0, y0, x1, y1 = box
    draw.text((x0 + 12, y0 + 13), kicker, font=font(SANS_BOLD, 13), fill=accent)
    text_block(draw, x0 + 12, y0 + 31, headline, font(SERIF_BOLD, 19), INK, x1 - x0 - 24, leading=22)
    picture(draw, (x0 + 12, y0 + 96, x1 - 12, y0 + 148))
    text_block(draw, x0 + 12, y0 + 154, caption, font(SANS, 15), (48, 52, 60), x1 - x0 - 24, leading=18)


def build():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([8, 8, CANVAS - 8, CANVAS - 8], outline=INK, width=3)

    # masthead (fixed rows so the tagline clears the rules below it)
    centred(draw, CANVAS // 2, 16, "THE WORLD IN ONE DAY", font(SERIF_BOLD, 50), NAVY)
    centred(draw, CANVAS // 2, 76, "SATURDAY, 21 NOVEMBER 2026", font(SANS_BOLD, 26), RED)
    centred(draw, CANVAS // 2, 108,
            "The day's world news on one front page — drawn, not photographed",
            font(SANS, 15), MUTED)
    draw.line([(EDGE, 130), (CANVAS - EDGE, 130)], fill=INK, width=4)
    draw.line([(EDGE, 135), (CANVAS - EDGE, 135)], fill=INK, width=1)

    # lead story
    lead = (EDGE, 144, CANVAS - EDGE, 452)
    panel(draw, lead, RED)
    draw.text((42, 158), "LEAD STORY  •  CONFLICT / EUROPE", font=font(SANS_BOLD, 15), fill=RED)
    hy = text_block(draw, 42, 180, "RUSSIAN MISSILES HIT POLAND",
                    font(SERIF_BOLD, 36), INK, 472, leading=40)
    sy = text_block(draw, 42, hy + 6,
                    "Two Russian missiles and a suspected drone came down in Poland.",
                    font(SANS_BOLD, 20), NAVY, 472, leading=24)
    draw.rectangle([42, sy + 8, 514, sy + 10], fill=RED)
    qy = text_block(draw, 42, sy + 18, "POLAND: “a deliberate provocation”",
                    font(SANS_BOLD, 19), INK, 472, leading=23)
    qy = text_block(draw, 42, qy + 2, "NATO: “a grave violation of its airspace”",
                    font(SANS_BOLD, 19), INK, 472, leading=23)
    text_block(draw, 42, qy + 10,
               "NATO airspace breached — Europe on alert.",
               font(SANS, 17), MUTED, 472, leading=21)
    draw_lead_map(draw, (540, 166, 982, 436))

    # six grid stories: 3 across, 2 down
    col_w = (CANVAS - 2 * EDGE - 2 * 12) // 3
    row_h = 196
    grid_top = 464
    cells = [
        ("JUSTICE  •  THE HAGUE", TEAL,
         "World Court: Myanmar committed genocide",
         "ICJ landmark ruling for the Rohingya people.",
         pic_courthouse),
        ("EUROPE  •  BRUSSELS", NAVY,
         "UK and EU sign food, carbon & youth deals",
         "PM Andy Burnham seals trade and mobility at summit.",
         pic_deal),
        ("ECONOMY  •  WALL STREET", RED,
         "Wall Street slumps into correction",
         "S&P 500 & Dow fall as AI stocks plunge about 3.7%.",
         pic_market),
        ("ASIA  •  SHENZHEN", AMBER,
         "Trump, Xi & Putin summit ends thin",
         "First trilateral summit: few concrete results.",
         pic_summit),
        ("WEATHER  •  INDIA", TEAL,
         "Cyclone Akvan hits Odisha–Andhra coast",
         "Near Gopalpur: ~300,000 evacuated, rescue under way.",
         pic_cyclone),
        ("MIDDLE EAST  •  SAUDI ARABIA", NAVY,
         "Missiles intercepted over Riyadh",
         "Saudi coalition stops Houthi missiles, strikes Hodeidah.",
         pic_intercept),
    ]
    for idx, (kicker, accent, headline, caption, picture) in enumerate(cells):
        col, row = idx % 3, idx // 3
        cx0 = EDGE + col * (col_w + 12)
        cy0 = grid_top + row * (row_h + 10)
        grid_cell(draw, (cx0, cy0, cx0 + col_w, cy0 + row_h),
                  kicker, accent, headline, caption, picture)

    # also-today strip (taller, so two-line items never touch the next row)
    strip = (EDGE, 878, CANVAS - EDGE, 1002)
    draw.rectangle(strip, fill=NAVY, outline=INK, width=2)
    draw.text((42, 888), "ALSO TODAY", font=font(SANS_BOLD, 20), fill=(250, 199, 44))
    also = [
        "Pill hailed as breakthrough for pancreatic cancer",
        "COP31 climate talks in Turkey enter crucial final stage",
        "LA jury convicts man of starting the Palisades Fire",
        "Indonesia fire losses could reach $30 billion",
    ]
    col_x = [42, 524]
    for i, item in enumerate(also):
        ix = col_x[i % 2]
        iy = 916 + (i // 2) * 42
        draw.ellipse([ix, iy + 5, ix + 9, iy + 14], fill=(250, 199, 44))
        text_block(draw, ix + 16, iy, item, font(SANS_BOLD, 15), WHITE, 438, leading=18)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True, compress_level=9)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
