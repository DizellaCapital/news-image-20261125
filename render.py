#!/usr/bin/env python3
"""Draw the Wednesday 25 November 2026 front page (v3).

Local-only renderer (Pillow). Reads stories_20261125-v3.json next to
this file and writes entry.png, 1024x1024, deterministic: the same
input bytes always produce the same output bytes. The grader never
runs this file; main.py only copies the finished entry.png.

v3 lever (freshness fix + 13 scenes + UTC strip): the two stale
Tuesday leads are gone; Wednesday's Kospi crash, the Tiangong
docking and the US tariff plan lead; 13 stories carry pictures
(3 leads + 10 grid); a "THE DAY IN UTC" strip times the day.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "stories_20261125-v3.json")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (247, 241, 222)
INK = (26, 26, 26)
RED = (178, 34, 34)
GREY = (90, 90, 90)
RULE = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(SERIF, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, start, max_w, minimum=10):
    size = start
    while size > minimum:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, minimum)


def text_block(draw, xy, lines, fnt, fill, leading=None):
    x, y = xy
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def band(draw, box, colors):
    """Vertical gradient bands across box (deterministic)."""
    x0, y0, x1, y1 = box
    n = len(colors)
    span = (y1 - y0) / n
    for i, col in enumerate(colors):
        draw.rectangle([x0, y0 + i * span, x1, y0 + (i + 1) * span + 1],
                       fill=col)


# ---------------------------------------------------------------- lead pictures
def pic_kospi(d, box):
    """Falling chip-market chart on a dark board."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 18, 30))
    for gy in range(y0 + 18, y1 - 8, 18):
        d.line([(x0 + 8, gy), (x1 - 8, gy)], fill=(32, 40, 58), width=1)
    pts = []
    n = 16
    for i in range(n):
        px = x0 + 14 + i * (x1 - x0 - 28) // (n - 1)
        py = y0 + 22 + int((i * i) * (y1 - y0 - 48) / ((n - 1) * (n - 1))) \
            + (i % 3) * 2
        pts.append((px, py))
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=(235, 70, 60), width=3)
    d.polygon([(pts[-1][0] - 8, pts[-1][1] - 12), (pts[-1][0] + 8, pts[-1][1]),
               (pts[-1][0] - 8, pts[-1][1] + 2)], fill=(235, 70, 60))
    # chip
    cx, cy = x0 + 58, y0 + 34
    d.rectangle([cx - 20, cy - 14, cx + 20, cy + 14], fill=(20, 90, 78),
                outline=(212, 175, 55), width=2)
    d.rectangle([cx - 6, cy - 5, cx + 6, cy + 5], fill=(212, 175, 55))
    for i in range(3):
        px = cx - 12 + i * 12
        d.line([(px, cy - 20), (px, cy - 14)], fill=(212, 175, 55), width=2)
        d.line([(px, cy + 14), (px, cy + 20)], fill=(212, 175, 55), width=2)
    d.rectangle([x1 - 92, y0 + 8, x1 - 8, y0 + 30], fill=RED)
    d.text((x1 - 87, y0 + 11), "−6.2%", font=font(SANS_B, 14),
           fill=(255, 255, 255))
    d.text((x0 + 10, y1 - 18), "KOSPI · WED CLOSE",
           font=font(SANS_B, 10), fill=(160, 170, 190))


def pic_tiangong(d, box):
    """Night launch: rocket rising to a station, two small flags."""
    x0, y0, x1, y1 = box
    band(d, box, [(8, 12, 38), (16, 26, 60), (30, 44, 78)])
    for sx, sy in ((x0 + 22, y0 + 14), (x0 + 90, y0 + 26), (x0 + 160, y0 + 12),
                   (x0 + 210, y0 + 34), (x0 + 260, y0 + 18), (x0 + 130, y0 + 44)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # station
    sx, sy = x1 - 96, y0 + 22
    d.rectangle([sx - 34, sy - 6, sx + 34, sy + 6], fill=(200, 205, 215))
    d.rectangle([sx - 52, sy - 10, sx - 34, sy + 10], fill=(60, 90, 160))
    d.rectangle([sx + 34, sy - 10, sx + 52, sy + 10], fill=(60, 90, 160))
    d.rectangle([sx - 8, sy - 14, sx + 8, sy + 14], fill=(220, 225, 235))
    # rocket
    rx = x0 + 56
    d.polygon([(rx - 12, y0 + 62), (rx + 12, y0 + 62), (rx, y0 + 34)],
              fill=(235, 235, 230))
    d.rectangle([rx - 12, y0 + 62, rx + 12, y1 - 46], fill=(235, 235, 230))
    d.polygon([(rx - 12, y1 - 46), (rx - 22, y1 - 30), (rx - 12, y1 - 34)],
              fill=(178, 34, 34))
    d.polygon([(rx + 12, y1 - 46), (rx + 22, y1 - 30), (rx + 12, y1 - 34)],
              fill=(178, 34, 34))
    d.ellipse([rx - 8, y1 - 30, rx + 8, y1 - 12], fill=(255, 170, 40))
    d.ellipse([rx - 5, y1 - 24, rx + 5, y1 - 10], fill=(255, 220, 90))
    # ground + flags
    d.rectangle([x0, y1 - 26, x1, y1], fill=(52, 44, 36))
    d.line([(x0 + 150, y1 - 52), (x0 + 150, y1 - 26)], fill=(220, 220, 220),
           width=2)
    d.rectangle([x0 + 150, y1 - 52, x0 + 174, y1 - 40], fill=(20, 120, 60))
    d.rectangle([x0 + 182, y1 - 52, x0 + 206, y1 - 40], fill=(220, 40, 40))
    d.text((x1 - 108, y1 - 20), "SHENZHOU-24", font=font(SANS_B, 10),
           fill=(200, 210, 225))


def pic_tariff(d, box):
    """Container ship with a red UP TO 20% stamp, top left."""
    x0, y0, x1, y1 = box
    band(d, box, [(150, 200, 225), (120, 180, 210), (90, 150, 190)])
    d.rectangle([x0, y1 - 34, x1, y1], fill=(28, 70, 120))
    for wx in range(x0 + 10, x1 - 10, 30):
        d.line([(wx, y1 - 16), (wx + 16, y1 - 16)], fill=(200, 225, 240),
               width=2)
    # hull + containers, shifted right to leave the stamp clear
    d.polygon([(x0 + 22, y1 - 34), (x1 - 22, y1 - 34), (x1 - 44, y1 - 16),
               (x0 + 44, y1 - 16)], fill=(30, 30, 36))
    cols = [(220, 60, 50), (40, 110, 180), (240, 200, 60), (60, 160, 90)]
    for i, col in enumerate(cols):
        cx = x0 + 112 + i * 42
        d.rectangle([cx, y1 - 66, cx + 38, y1 - 36], fill=col,
                    outline=(255, 255, 255), width=1)
        d.rectangle([cx, y1 - 92, cx + 38, y1 - 68], fill=cols[(i + 2) % 4],
                    outline=(255, 255, 255), width=1)
    # bridge
    d.rectangle([x1 - 58, y1 - 92, x1 - 28, y1 - 34], fill=(240, 240, 235))
    for r in range(3):
        d.rectangle([x1 - 54, y1 - 88 + r * 12, x1 - 32, y1 - 80 + r * 12],
                    fill=(40, 90, 140))
    # stamp, top left in clear sky
    d.ellipse([x0 + 10, y0 + 8, x0 + 100, y0 + 62], outline=RED, width=4)
    d.ellipse([x0 + 18, y0 + 16, x0 + 92, y0 + 54], outline=RED, width=2)
    d.text((x0 + 30, y0 + 22), "UP TO", font=font(SANS_B, 12), fill=RED)
    d.text((x0 + 30, y0 + 36), "20%", font=font(SANS_B, 17), fill=RED)


# ---------------------------------------------------------------- grid pictures
def pic_hormuz(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(250, 180, 110), (235, 140, 70), (200, 110, 60)])
    d.rectangle([x0, y1 - 22, x1, y1], fill=(24, 70, 110))
    d.rectangle([x0 + 30, y1 - 40, x0 + 130, y1 - 22], fill=(40, 40, 46))
    d.rectangle([x0 + 52, y1 - 52, x0 + 70, y1 - 40], fill=(40, 40, 46))
    d.ellipse([x0 + 76, y0 + 6, x0 + 104, y0 + 30], fill=(255, 170, 40))
    for dx, dy in ((-14, 0), (14, 0), (0, -12), (0, 12)):
        d.line([(x0 + 90, y0 + 18), (x0 + 90 + dx, y0 + 18 + dy)],
               fill=(255, 170, 40), width=3)
    d.ellipse([x1 - 40, y0 + 14, x1 - 22, y0 + 30], fill=(90, 90, 95))
    d.ellipse([x1 - 52, y0 + 6, x1 - 36, y0 + 20], fill=(110, 110, 115))
    d.text((x1 - 62, y1 - 20), "2 TANKERS", font=font(SANS_B, 10),
           fill=(255, 255, 255))


def pic_solomon(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(150, 200, 225), (120, 180, 210)])
    d.ellipse([x0 + 132, y0 + 6, x0 + 152, y0 + 26], fill=(255, 220, 120))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(38, 110, 160))
    d.ellipse([x0 + 8, y1 - 44, x1 - 8, y1 - 16], fill=(74, 140, 74))
    d.line([(x0 + 92, y1 - 48), (x0 + 92, y1 - 18)], fill=(60, 50, 40),
           width=3)
    d.polygon([(x0 + 92, y1 - 48), (x0 + 134, y1 - 40), (x0 + 92, y1 - 32)],
              fill=(0, 60, 140))
    d.polygon([(x0 + 26, y1 - 28), (x0 + 48, y1 - 28), (x0 + 38, y1 - 42)],
              fill=(120, 90, 50))
    d.text((x1 - 66, y0 + 4), "TREATY", font=font(SANS_B, 10),
           fill=(255, 255, 255))


def pic_energy(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 226, 205))
    d.polygon([(x0 + 30, y0 + 26), (x0 + 78, y0 + 8), (x0 + 126, y0 + 26)],
              fill=(120, 40, 40))
    d.rectangle([x0 + 38, y0 + 26, x0 + 118, y1 - 8], fill=(250, 246, 235),
                outline=(120, 40, 40), width=2)
    d.ellipse([x0 + 66, y0 + 34, x0 + 90, y0 + 52], fill=(255, 170, 40))
    d.polygon([(x0 + 78, y0 + 32), (x0 + 86, y0 + 44), (x0 + 78, y0 + 50),
               (x0 + 70, y0 + 44)], fill=(235, 90, 30))
    d.text((x1 - 62, y0 + 8), "+26%", font=font(SANS_B, 18), fill=RED)
    d.text((x1 - 62, y0 + 30), "£2,166", font=font(SANS_B, 11), fill=INK)


def pic_mine(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(200, 170, 120), (170, 130, 80)])
    d.polygon([(x0 + 20, y0 + 10), (x0 + 120, y0 + 10), (x0 + 96, y1 - 8),
               (x0 + 44, y1 - 8)], fill=(90, 60, 30))
    d.rectangle([x0 + 52, y1 - 26, x0 + 88, y1 - 8], fill=(40, 90, 140))
    for wx in range(x0 + 8, x1 - 8, 22):
        d.line([(wx, y0 + 34), (wx + 12, y0 + 34)], fill=(140, 110, 70),
               width=2)
    d.rectangle([x1 - 52, y0 + 6, x1 - 8, y0 + 24], fill=RED)
    d.text((x1 - 48, y0 + 9), "26", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    d.text((x0 + 8, y1 - 16), "100 m DOWN", font=font(SANS_B, 9),
           fill=(255, 255, 255))


def pic_gaza(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(240, 200, 140), (220, 170, 110)])
    d.ellipse([x0 + 14, y0 + 8, x0 + 34, y0 + 28], fill=(255, 220, 120))
    for bx, bh in ((x0 + 16, 26), (x0 + 52, 38), (x0 + 92, 30),
                   (x0 + 128, 42)):
        d.rectangle([bx, y1 - bh, bx + 30, y1], fill=(70, 62, 58))
    d.ellipse([x1 - 52, y0 + 8, x1 - 30, y0 + 26], fill=(90, 90, 95))
    d.ellipse([x1 - 64, y0 + 18, x1 - 44, y0 + 34], fill=(110, 110, 115))
    d.ellipse([x1 - 40, y0 + 26, x1 - 22, y0 + 40], fill=(130, 130, 135))


def pic_cia(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(28, 30, 38))
    d.polygon([(x0 + 22, y0 + 22), (x0 + 108, y0 + 22), (x0 + 65, y0 + 8)],
              fill=(210, 205, 195))
    d.rectangle([x0 + 22, y0 + 22, x0 + 108, y0 + 28], fill=(210, 205, 195))
    for i in range(4):
        cx = x0 + 32 + i * 20
        d.rectangle([cx, y0 + 28, cx + 8, y1 - 8], fill=(210, 205, 195))
    d.rectangle([x0 + 22, y1 - 8, x0 + 108, y1 - 2], fill=(210, 205, 195))
    d.arc([x1 - 52, y0 + 14, x1 - 26, y0 + 32], 180, 360,
          fill=(255, 200, 60), width=3)
    d.rectangle([x1 - 55, y0 + 30, x1 - 23, y1 - 8], fill=RED,
                outline=(255, 200, 60), width=2)
    d.ellipse([x1 - 44, y0 + 36, x1 - 34, y0 + 44], fill=(255, 220, 120))


def pic_hodeidah(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(200, 220, 235), (170, 200, 220)])
    d.rectangle([x0, y1 - 18, x1, y1], fill=(30, 80, 120))
    for cx in (x0 + 24, x0 + 78):
        d.line([(cx, y0 + 10), (cx, y1 - 18)], fill=(50, 50, 55), width=4)
        d.line([(cx, y0 + 10), (cx + 34, y0 + 22)], fill=(50, 50, 55),
               width=3)
        d.line([(cx + 34, y0 + 22), (cx + 34, y1 - 18)], fill=(50, 50, 55),
               width=2)
    d.rectangle([x0 + 118, y1 - 34, x0 + 168, y1 - 18], fill=(40, 40, 46))
    ex, ey = x1 - 34, y0 + 20
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 170, 40))
    for dx, dy in ((-16, 0), (16, 0), (0, -16), (0, 16)):
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(255, 170, 40), width=3)
    d.text((x0 + 8, y0 + 4), "PORT", font=font(SANS_B, 10), fill=(30, 60, 90))


def pic_garment(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(240, 235, 215))
    d.rectangle([x0 + 14, y0 + 22, x0 + 108, y1 - 8], fill=(120, 60, 60))
    d.polygon([(x0 + 14, y0 + 22), (x0 + 108, y0 + 22), (x0 + 96, y0 + 10),
               (x0 + 26, y0 + 10)], fill=(90, 40, 40))
    for i in range(3):
        wx = x0 + 26 + i * 28
        d.rectangle([wx, y0 + 32, wx + 18, y0 + 44], fill=(255, 220, 120))
    d.rectangle([x0 + 118, y0 + 8, x0 + 172, y0 + 32], fill=(20, 120, 80))
    d.text((x0 + 122, y0 + 12), "+36%", font=font(SANS_B, 14),
           fill=(255, 255, 255))
    d.text((x0 + 118, y0 + 38), "17,500 tk", font=font(SANS_B, 10), fill=INK)


def pic_cpi(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 228, 245))
    bars = [(14, 18), (22, 26), (30, 34), (44, 46)]
    for i, (h0, h1) in enumerate(bars):
        bx = x0 + 16 + i * 26
        d.rectangle([bx, y1 - 12 - h1, bx + 18, y1 - 12], fill=(31, 78, 121))
    d.line([(x0 + 10, y1 - 30), (x1 - 12, y1 - 52)], fill=RED, width=3)
    d.polygon([(x1 - 12, y1 - 52), (x1 - 24, y1 - 52), (x1 - 14, y1 - 42)],
              fill=RED)
    d.text((x1 - 58, y0 + 6), "4.9%", font=font(SANS_B, 16), fill=RED)


def pic_ebola(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(178, 208, 222), (214, 226, 228), (232, 226, 205)])
    # clinic tent
    d.polygon([(x0 + 18, y1 - 10), (x0 + 60, y0 + 10), (x0 + 102, y1 - 10)],
              fill=(250, 250, 246), outline=(150, 150, 145))
    d.rectangle([x0 + 54, y0 + 22, x0 + 66, y0 + 30], fill=RED)
    d.rectangle([x0 + 58, y0 + 18, x0 + 62, y0 + 34], fill=RED)
    d.rectangle([x0 + 116, y1 - 30, x0 + 172, y1 - 12], fill=(250, 250, 246),
                outline=(150, 150, 145), width=2)
    d.rectangle([x0 + 138, y1 - 26, x0 + 146, y1 - 18], fill=RED)
    d.rectangle([x0 + 141, y1 - 29, x0 + 143, y1 - 15], fill=RED)
    d.ellipse([x0 + 122, y1 - 14, x0 + 132, y1 - 4], fill=(30, 30, 30))
    d.ellipse([x0 + 156, y1 - 14, x0 + 166, y1 - 4], fill=(30, 30, 30))
    # figure in PPE
    fx = x1 - 16
    d.ellipse([fx - 6, y0 + 14, fx + 6, y0 + 26], fill=(240, 240, 235))
    d.rectangle([fx - 7, y0 + 26, fx + 7, y1 - 10], fill=(240, 240, 235))
    d.rectangle([fx - 7, y0 + 26, fx + 7, y0 + 32], fill=(70, 120, 180))
    d.rectangle([x0, y1 - 8, x1, y1], fill=(198, 178, 140))


LEAD_PIC = {1: pic_kospi, 2: pic_tiangong, 3: pic_tariff}
GRID_PIC = {4: pic_hormuz, 5: pic_solomon, 6: pic_energy, 7: pic_mine,
            8: pic_gaza, 9: pic_cia, 10: pic_hodeidah, 11: pic_garment,
            12: pic_cpi, 13: pic_ebola}

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "AMERICAS": (106, 61, 154),
    "ASIA-PACIFIC": (14, 122, 107),
    "MIDDLE EAST": (176, 124, 12),
    "AFRICA": (196, 94, 26),
    "WORLD": (85, 85, 85),
}


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(220, 235, 245), outline=(150, 160, 165), width=1)
    land = (232, 217, 168)
    d.polygon([(x0 + 28, y0 + 22), (x0 + 78, y0 + 14), (x0 + 96, y0 + 30),
               (x0 + 82, y0 + 48), (x0 + 56, y0 + 44), (x0 + 34, y0 + 52),
               (x0 + 22, y0 + 38)], fill=land)
    d.polygon([(x0 + 62, y0 + 66), (x0 + 88, y0 + 62), (x0 + 94, y0 + 84),
               (x0 + 78, y0 + 108), (x0 + 66, y0 + 92)], fill=land)
    d.polygon([(x0 + 148, y0 + 22), (x0 + 172, y0 + 16), (x0 + 182, y0 + 30),
               (x0 + 166, y0 + 40), (x0 + 148, y0 + 34)], fill=land)
    d.polygon([(x0 + 150, y0 + 48), (x0 + 182, y0 + 44), (x0 + 192, y0 + 66),
               (x0 + 178, y0 + 96), (x0 + 160, y0 + 82)], fill=land)
    d.polygon([(x0 + 184, y0 + 18), (x0 + 268, y0 + 12), (x0 + 288, y0 + 34),
               (x0 + 262, y0 + 56), (x0 + 228, y0 + 52), (x0 + 204, y0 + 62),
               (x0 + 186, y0 + 42)], fill=land)
    d.polygon([(x0 + 252, y0 + 92), (x0 + 284, y0 + 88), (x0 + 290, y0 + 104),
               (x0 + 262, y0 + 110)], fill=land)
    pins = [(1, 262, 34), (2, 238, 30), (3, 44, 38), (4, 178, 58),
            (5, 288, 100), (6, 138, 24), (7, 246, 82), (8, 164, 50),
            (9, 66, 50), (10, 168, 66), (11, 222, 52), (12, 292, 108),
            (13, 152, 76)]
    for n, px, py in pins:
        d.ellipse([x0 + px - 8, y0 + py - 8, x0 + px + 8, y0 + py + 8],
                  fill=RED, outline=(255, 255, 255), width=1)
        d.text((x0 + px - 3, y0 + py - 6), str(n), font=font(SANS_B, 10),
               fill=(255, 255, 255))


def main():
    with open(DATA, encoding="utf-8") as fh:
        data = json.load(fh)
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 24
    cw = W - 2 * mx

    # ---- top black bar
    d.rectangle([0, 0, W, 28], fill=(16, 16, 16))
    d.text((mx, 7), "THE WORLD ON WEDNESDAY", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    right = "36 STORIES · 6 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - mx - d.textlength(right, font=font(SANS_B, 13)), 7), right,
           font=font(SANS_B, 13), fill=(255, 255, 255))

    # ---- masthead: the date, giant
    mast = fit_font(d, "Wednesday 25 November 2026", SERIF_B, 58, cw)
    d.text((mx, 32), "Wednesday 25 November 2026", font=mast, fill=INK)
    sub = ("Kospi crashes -6.2% · Pakistan's first astronaut docks at Tiangong "
           "· US proposes tariffs of up to 20%")
    subf = fit_font(d, sub, SERIF_I, 18, cw, minimum=13)
    d.text((mx, 100), sub, font=subf, fill=RED)
    d.line([(mx, 124), (W - mx, 124)], fill=RULE, width=2)

    # ---- numbers strip: six big red figures
    nums = data["numbers"]
    cell = cw / 6
    y = 130
    for i, item in enumerate(nums):
        x = mx + i * cell
        if i:
            d.line([(x, y + 4), (x, y + 50)], fill=(200, 190, 170), width=1)
        nf = fit_font(d, item["value"], SERIF_B, 34, cell - 16, minimum=18)
        d.text((x + 8, y), item["value"], font=nf, fill=RED)
        cap = wrap(d, item["label"], font(SANS, 10), cell - 16)
        text_block(d, (x + 8, y + 38), cap[:1], font(SANS, 10), INK,
                   leading=12)
    d.line([(mx, 186), (W - mx, 186)], fill=RULE, width=1)

    # ---- the day in UTC
    d.rectangle([mx, 190, W - mx, 212], fill=(16, 16, 16))
    d.text((mx + 8, 195), "THE DAY IN UTC", font=font(SANS_B, 12),
           fill=(255, 200, 60))
    parts = []
    for item in data["utc"]:
        parts.append(f"{item['time']} {item['event']}")
    strip = "   ·   ".join(parts)
    sf = fit_font(d, strip, SANS_B, 12, cw - 150, minimum=9)
    d.text((mx + 132, 195), strip, font=sf, fill=(255, 255, 255))

    # ---- region bars
    regs = data["regions"]
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA",
             "WORLD"]
    total = sum(regs.values())
    x = mx
    y = 216
    for name in order:
        wseg = cw * regs[name] / total
        d.rectangle([x, y, x + wseg - 2, y + 18], fill=REGION_COLORS[name])
        label = f"{name} {regs[name]}"
        lf = font(SANS_B, 10)
        if d.textlength(label, font=lf) <= wseg - 8:
            d.text((x + 5, y + 4), label, font=lf, fill=(255, 255, 255))
        x += wseg
    d.line([(mx, 238), (W - mx, 238)], fill=RULE, width=1)

    # ---- three illustrated leads
    colw = (cw - 16) / 3
    y0 = 246
    ill_h = 110
    for i, lead in enumerate(data["leads"]):
        x = mx + i * (colw + 8)
        LEAD_PIC[lead["pin"]](d, (int(x), y0, int(x + colw), y0 + ill_h))
        d.rectangle([int(x), y0 + ill_h, int(x + colw), y0 + ill_h + 18],
                    fill=RED)
        d.text((x + 6, y0 + ill_h + 3), lead["kicker"], font=font(SANS_B, 11),
               fill=(255, 255, 255))
        d.text((x, y0 + ill_h + 22), f"{lead['pin']} {lead['place']}",
               font=font(SANS_B, 10), fill=RED)
        head = wrap(d, lead["headline"], font(SERIF_B, 24), colw)
        yy = text_block(d, (x, y0 + ill_h + 36), head[:2],
                        font(SERIF_B, 24), INK, leading=27)
        deck = wrap(d, lead["deck"], font(SANS, 12), colw)
        yy = text_block(d, (x, yy + 3), deck[:2], font(SANS, 12), INK,
                        leading=14)
        d.text((x, yy + 2), f"({lead['source']})", font=font(SERIF_I, 10),
               fill=GREY)

    # ---- grid: ten illustrated stories, two rows of five
    grid = sorted(data["grid"], key=lambda g: g["pin"])
    colw2 = (cw - 32) / 5
    for row in range(2):
        y0 = 494 + row * 140
        ill_h2 = 58
        for i in range(5):
            item = grid[row * 5 + i]
            x = mx + i * (colw2 + 8)
            GRID_PIC[item["pin"]](d, (int(x), y0, int(x + colw2), y0 + ill_h2))
            d.rectangle([int(x), y0 + ill_h2, int(x + colw2),
                         y0 + ill_h2 + 15], fill=RED)
            d.text((x + 5, y0 + ill_h2 + 2), item["kicker"],
                   font=font(SANS_B, 9), fill=(255, 255, 255))
            head = wrap(d, item["headline"], font(SERIF_B, 15), colw2)
            yy = text_block(d, (x, y0 + ill_h2 + 19), head[:2],
                            font(SERIF_B, 15), INK, leading=17)
            deck = wrap(d, item["deck"], font(SANS, 10), colw2)
            text_block(d, (x, yy + 2), deck[:2], font(SANS, 10), INK,
                       leading=12)

    # ---- map + ALSO list
    y0 = 782
    d.text((mx, y0), "WHERE IT HAPPENED · pins match story numbers",
           font=font(SANS_B, 11), fill=INK)
    also_head = "ALSO ON WEDNESDAY 25 NOVEMBER — 23 MORE STORIES"
    d.text((W - mx - d.textlength(also_head, font=font(SANS_B, 11)), y0),
           also_head, font=font(SANS_B, 11), fill=RED)
    draw_map(d, (mx, y0 + 20, mx + 316, y0 + 140))
    ax = mx + 328
    items = data["also"]
    per_col = 12
    for col in range(2):
        cx = ax + col * 322
        for j in range(per_col):
            idx = col * per_col + j
            if idx >= len(items):
                break
            item = items[idx]
            yy = y0 + 22 + j * 10
            d.text((cx, yy), str(item["n"]), font=font(SANS_B, 10), fill=RED)
            head = item["headline"]
            src = item["source"]
            lf = font(SANS, 10)
            while d.textlength(head + " · " + src, font=lf) > 296 \
                    and len(head) > 12:
                head = head[:-4] + "…"
            d.text((cx + 20, yy), head + " · " + src, font=lf, fill=INK)

    # ---- date check
    y0 = 934
    d.rectangle([mx, y0, W - mx, y0 + 52], outline=RED, width=2)
    d.text((mx + 8, y0 + 4), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    note = (data["date_check"]["note"] + " "
            + data["date_check"]["left_out"])
    nf = font(SANS, 10)
    lines = wrap(d, note, nf, cw - 16)
    text_block(d, (mx + 8, y0 + 20), lines[:2], nf, INK, leading=13)

    # ---- footer
    d.text((mx, 996), "Sources named beside each story · Original drawings, drawn in code.",
           font=font(SERIF_I, 10), fill=GREY)
    foot = "THE WORLD ON WEDNESDAY · 25 NOV 2026"
    d.text((W - mx - d.textlength(foot, font=font(SANS_B, 10)), 996), foot,
           font=font(SANS_B, 10), fill=INK)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
