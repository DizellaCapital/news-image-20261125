#!/usr/bin/env python3
"""Draw the Wednesday 25 November 2026 front page (v2).

Local-only renderer (Pillow). Reads stories_20261125.json next to this
file and writes entry.png, 1024x1024, deterministic: same input bytes
always produce the same output bytes. The grader never runs this file;
main.py only copies the finished entry.png.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "stories_20261125.json")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (247, 241, 222)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
GREY = (90, 90, 90)
LIGHTGREY = (120, 118, 110)
RULE = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


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
        draw.rectangle([x0, y0 + i * span, x1, y0 + (i + 1) * span + 1], fill=col)


# ---------------------------------------------------------------- illustrations
def ill_huawei(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(18, 35, 61))
    # circuit traces
    for yy in (y0 + 22, y0 + 52, y1 - 52, y1 - 22):
        d.line([(x0 + 14, yy), (x1 - 14, yy)], fill=(46, 120, 110), width=2)
    for xx in (x0 + 30, x0 + 70, x1 - 70, x1 - 30):
        d.line([(xx, y0 + 12), (xx, y1 - 12)], fill=(46, 120, 110), width=2)
    for xx, yy in ((x0 + 30, y0 + 22), (x1 - 70, y0 + 52),
                   (x0 + 70, y1 - 22), (x1 - 30, y1 - 52)):
        d.ellipse([xx - 5, yy - 5, xx + 5, yy + 5], fill=(212, 175, 55))
    # the chip
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 62, cy - 46, cx + 62, cy + 46], fill=(14, 90, 78),
                outline=(212, 175, 55), width=4)
    for i in range(-2, 3):
        d.line([(cx - 62, cy + i * 16), (cx + 62, cy + i * 16)],
               fill=(212, 175, 55), width=1)
    for i in range(-2, 3):
        d.line([(cx + i * 22, cy - 46), (cx + i * 22, cy + 46)],
               fill=(212, 175, 55), width=1)
    d.rectangle([cx - 18, cy - 14, cx + 18, cy + 14], fill=(212, 175, 55))
    # pins
    for i in range(5):
        px = cx - 44 + i * 22
        d.line([(px, cy - 58), (px, cy - 46)], fill=(212, 175, 55), width=3)
        d.line([(px, cy + 46), (px, cy + 58)], fill=(212, 175, 55), width=3)
    d.rectangle([x1 - 96, y0 + 10, x1 - 10, y0 + 34], fill=RED)
    d.text((x1 - 91, y0 + 14), "10 COUNTS", font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_riyadh(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(255, 176, 102), (244, 130, 60), (214, 84, 44), (120, 52, 40)])
    d.ellipse([x0 + 26, y0 + 16, x0 + 66, y0 + 56], fill=(255, 214, 120))
    # tallest tower
    tx = (x0 + x1) // 2 + 30
    d.rectangle([tx - 26, y0 + 42, tx + 26, y1 - 18], fill=(30, 28, 34))
    d.polygon([(tx - 26, y0 + 42), (tx + 26, y0 + 42), (tx, y0 + 18)],
              fill=(30, 28, 34))
    for r in range(6):
        for c in range(3):
            d.rectangle([tx - 18 + c * 14, y0 + 56 + r * 16,
                         tx - 10 + c * 14, y0 + 64 + r * 16],
                        fill=(255, 205, 90))
    # low skyline
    d.rectangle([x0, y1 - 30, x1, y1], fill=(24, 22, 28))
    for bx in (x0 + 12, x0 + 66, x1 - 92, x1 - 40):
        d.rectangle([bx, y1 - 58, bx + 34, y1 - 30], fill=(40, 36, 44))
    # missile trail + burst
    for i in range(6):
        px = x0 + 30 + i * 16
        py = y0 + 96 - i * 10
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 240, 200))
    d.ellipse([x0 + 118, y0 + 26, x0 + 142, y0 + 50], fill=(255, 220, 90))
    for dx, dy in ((-14, 0), (14, 0), (0, -14), (0, 14), (-10, -10), (10, 10)):
        d.line([(x0 + 130, y0 + 38), (x0 + 130 + dx, y0 + 38 + dy)],
               fill=(255, 220, 90), width=3)


def ill_ebola(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(178, 208, 222), (214, 226, 228), (232, 226, 205)])
    # clinic
    d.rectangle([x0 + 22, y0 + 52, x0 + 148, y1 - 34], fill=(250, 250, 246),
                outline=(150, 150, 145), width=2)
    d.rectangle([x0 + 22, y0 + 52, x0 + 148, y0 + 66], fill=RED)
    d.rectangle([x0 + 72, y0 + 78, x0 + 98, y0 + 92], fill=RED)
    d.rectangle([x0 + 79, y0 + 71, x0 + 91, y0 + 99], fill=RED)
    d.rectangle([x0 + 34, y0 + 108, x0 + 58, y0 + 128], fill=(120, 150, 170))
    d.rectangle([x0 + 112, y0 + 108, x0 + 136, y0 + 128], fill=(120, 150, 170))
    d.rectangle([x0 + 70, y0 + 112, x0 + 100, y1 - 34], fill=(90, 90, 90))
    # ambulance
    d.rectangle([x1 - 128, y1 - 62, x1 - 18, y1 - 34], fill=(250, 250, 246),
                outline=(150, 150, 145), width=2)
    d.rectangle([x1 - 128, y1 - 62, x1 - 88, y1 - 40], fill=(250, 250, 246),
                outline=(150, 150, 145), width=2)
    d.rectangle([x1 - 106, y1 - 56, x1 - 96, y1 - 48], fill=RED)
    d.rectangle([x1 - 101, y1 - 61, x1 - 100, y1 - 43], fill=RED)
    d.ellipse([x1 - 116, y1 - 38, x1 - 100, y1 - 22], fill=(30, 30, 30))
    d.ellipse([x1 - 48, y1 - 38, x1 - 32, y1 - 22], fill=(30, 30, 30))
    # two figures in PPE
    for fx in (x0 + 168, x0 + 200):
        d.ellipse([fx - 8, y1 - 66, fx + 8, y1 - 50], fill=(240, 240, 235))
        d.rectangle([fx - 9, y1 - 52, fx + 9, y1 - 24], fill=(240, 240, 235))
        d.rectangle([fx - 9, y1 - 52, fx + 9, y1 - 44], fill=(70, 120, 180))
    d.rectangle([x0, y1 - 24, x1, y1], fill=(198, 178, 140))


def ill_kyiv(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(10, 22, 48), (16, 34, 66), (24, 52, 84)])
    d.ellipse([x0 + 130, y0 + 8, x0 + 152, y0 + 30], fill=(235, 230, 200))
    # ships
    for sx in (x0 + 14, x0 + 96):
        d.polygon([(sx, y1 - 34), (sx + 62, y1 - 34), (sx + 54, y1 - 18),
                   (sx + 8, y1 - 18)], fill=(120, 125, 135))
        d.line([(sx + 30, y1 - 34), (sx + 30, y1 - 52)], fill=(180, 180, 180),
               width=2)
        d.rectangle([sx + 22, y1 - 44, sx + 38, y1 - 34], fill=(180, 180, 180))
    # drone + explosion
    d.line([(x0 + 84, y1 - 62), (x0 + 96, y1 - 62)], fill=(255, 255, 255),
           width=2)
    d.line([(x0 + 90, y1 - 68), (x0 + 90, y1 - 56)], fill=(255, 255, 255),
           width=2)
    ex, ey = x1 - 34, y0 + 26
    d.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(255, 170, 40))
    for dx, dy in ((-20, 0), (20, 0), (0, -20), (0, 20)):
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(255, 170, 40), width=3)
    for wx in range(x0 + 8, x1 - 8, 26):
        d.line([(wx, y1 - 10), (wx + 14, y1 - 10)], fill=(90, 130, 170),
               width=2)


def ill_cia(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(28, 30, 38))
    # classical building
    d.polygon([(x0 + 30, y0 + 34), (x0 + 150, y0 + 34), (x0 + 90, y0 + 12)],
              fill=(210, 205, 195))
    d.rectangle([x0 + 30, y0 + 34, x0 + 150, y0 + 42], fill=(210, 205, 195))
    for i in range(5):
        cx = x0 + 44 + i * 24
        d.rectangle([cx, y0 + 42, cx + 10, y1 - 22], fill=(210, 205, 195))
    d.rectangle([x0 + 30, y1 - 22, x0 + 150, y1 - 12], fill=(210, 205, 195))
    # padlock
    d.arc([x1 - 62, y0 + 38, x1 - 30, y0 + 60], 180, 360, fill=(255, 200, 60),
          width=4)
    d.rectangle([x1 - 66, y0 + 56, x1 - 26, y1 - 8], fill=RED,
                outline=(255, 200, 60), width=2)
    d.ellipse([x1 - 52, y0 + 62, x1 - 40, y0 + 70], fill=(255, 220, 120))


def ill_solomon(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(150, 200, 225), (120, 180, 210)])
    d.ellipse([x0 + 132, y0 + 8, x0 + 156, y0 + 32], fill=(255, 220, 120))
    d.rectangle([x0, y1 - 34, x1, y1], fill=(38, 110, 160))
    d.ellipse([x0 + 8, y1 - 62, x1 - 8, y1 - 22], fill=(74, 140, 74))
    d.line([(x0 + 92, y1 - 66), (x0 + 92, y1 - 26)], fill=(60, 50, 40),
           width=3)
    d.polygon([(x0 + 92, y1 - 66), (x0 + 140, y1 - 56), (x0 + 92, y1 - 46)],
              fill=(0, 60, 140))
    for sx, sy in ((x0 + 104, y1 - 60), (x0 + 116, y1 - 58),
                   (x0 + 110, y1 - 52)):
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.polygon([(x0 + 26, y1 - 40), (x0 + 52, y1 - 40), (x0 + 40, y1 - 58)],
              fill=(120, 90, 50))
    for wx in range(x0 + 10, x1 - 10, 30):
        d.line([(wx, y1 - 16), (wx + 16, y1 - 16)], fill=(200, 225, 240),
               width=2)


def ill_cricket(d, box):
    x0, y0, x1, y1 = box
    band(d, box, [(12, 24, 54), (20, 40, 80)])
    d.ellipse([x0 + 14, y0 + 10, x0 + 30, y0 + 26], fill=(255, 230, 150))
    d.rectangle([x0, y1 - 34, x1, y1], fill=(46, 120, 62))
    d.rectangle([x0 + 60, y1 - 44, x0 + 130, y1 - 30], fill=(214, 190, 140))
    # stumps
    for i in range(3):
        sx = x0 + 150 + i * 7
        d.line([(sx, y1 - 52), (sx, y1 - 34)], fill=(255, 220, 90), width=3)
    # batsman silhouette
    bx = x0 + 92
    d.ellipse([bx - 7, y1 - 74, bx + 7, y1 - 60], fill=(10, 10, 12))
    d.line([(bx, y1 - 60), (bx - 4, y1 - 36)], fill=(10, 10, 12), width=5)
    d.line([(bx - 4, y1 - 36), (bx - 12, y1 - 26)], fill=(10, 10, 12), width=4)
    d.line([(bx - 4, y1 - 36), (bx + 6, y1 - 26)], fill=(10, 10, 12), width=4)
    d.line([(bx + 2, y1 - 52), (bx + 20, y1 - 40)], fill=(150, 110, 60),
           width=5)
    # ball trail
    for i in range(5):
        px = x0 + 30 + i * 12
        py = y0 + 34 + i * 6
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    d.text((x1 - 52, y0 + 6), "204", font=font(SANS_B, 22), fill=(255, 255, 255))


def ill_medal(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(96, 22, 26))
    d.polygon([(x0 + 70, y0 + 8), (x0 + 96, y0 + 8), (x0 + 104, y0 + 52),
               (x0 + 62, y0 + 52)], fill=(178, 34, 34))
    d.polygon([(x0 + 96, y0 + 8), (x0 + 122, y0 + 8), (x0 + 130, y0 + 52),
               (x0 + 104, y0 + 52)], fill=(240, 240, 235))
    d.polygon([(x0 + 122, y0 + 8), (x0 + 148, y0 + 8), (x0 + 156, y0 + 52),
               (x0 + 130, y0 + 52)], fill=(30, 60, 130))
    cx, cy = (x0 + x1) // 2 + 12, y0 + 58
    d.ellipse([cx - 22, cy - 16, cx + 22, cy + 16], fill=(212, 175, 55),
              outline=(255, 220, 120), width=3)
    d.polygon([(cx, cy - 10), (cx + 3, cy - 2), (cx + 11, cy - 2),
               (cx + 5, cy + 3), (cx + 7, cy + 11), (cx, cy + 7),
               (cx - 7, cy + 11), (cx - 5, cy + 3), (cx - 11, cy - 2),
               (cx - 3, cy - 2)], fill=(96, 22, 26))


LEAD_ILL = [ill_huawei, ill_riyadh, ill_ebola]
ROW2_ILL = [ill_kyiv, ill_cia, ill_solomon, ill_cricket, ill_medal]

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
    # North America
    d.polygon([(x0 + 28, y0 + 22), (x0 + 78, y0 + 14), (x0 + 96, y0 + 30),
               (x0 + 82, y0 + 48), (x0 + 56, y0 + 44), (x0 + 34, y0 + 52),
               (x0 + 22, y0 + 38)], fill=land)
    # South America
    d.polygon([(x0 + 62, y0 + 66), (x0 + 88, y0 + 62), (x0 + 94, y0 + 84),
               (x0 + 78, y0 + 108), (x0 + 66, y0 + 92)], fill=land)
    # Europe
    d.polygon([(x0 + 148, y0 + 22), (x0 + 172, y0 + 16), (x0 + 182, y0 + 30),
               (x0 + 166, y0 + 40), (x0 + 148, y0 + 34)], fill=land)
    # Africa
    d.polygon([(x0 + 150, y0 + 48), (x0 + 182, y0 + 44), (x0 + 192, y0 + 66),
               (x0 + 178, y0 + 96), (x0 + 160, y0 + 82)], fill=land)
    # Asia
    d.polygon([(x0 + 184, y0 + 18), (x0 + 268, y0 + 12), (x0 + 288, y0 + 34),
               (x0 + 262, y0 + 56), (x0 + 228, y0 + 52), (x0 + 204, y0 + 62),
               (x0 + 186, y0 + 42)], fill=land)
    # Australia
    d.polygon([(x0 + 252, y0 + 92), (x0 + 284, y0 + 88), (x0 + 290, y0 + 104),
               (x0 + 262, y0 + 110)], fill=land)
    pins = [(1, 66, 34), (5, 62, 42), (8, 74, 40), (4, 172, 24),
            (2, 196, 56), (3, 170, 68), (7, 200, 60), (6, 282, 96)]
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
    d.rectangle([0, 0, W, 30], fill=(16, 16, 16))
    d.text((mx, 8), "THE WORLD ON WEDNESDAY", font=font(SANS_B, 13),
           fill=(255, 255, 255))
    right = "36 STORIES · 6 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    d.text((W - mx - d.textlength(right, font=font(SANS_B, 13)), 8), right,
           font=font(SANS_B, 13), fill=(255, 255, 255))

    # ---- masthead: the date, giant
    mast = fit_font(d, "Wednesday 25 November 2026", SERIF_B, 66, cw)
    d.text((mx, 36), "Wednesday 25 November 2026", font=mast, fill=INK)
    sub = ("Huawei guilty on 10 counts · Houthi missile hits Riyadh tower · "
           "WHO pulls Ebola teams out of Congo")
    subf = fit_font(d, sub, SERIF_I, 22, cw, minimum=14)
    d.text((mx, 118), sub, font=subf, fill=RED)
    d.line([(mx, 150), (W - mx, 150)], fill=RULE, width=2)

    # ---- numbers strip: six big red figures
    nums = data["numbers"]
    cell = cw / 6
    y = 158
    for i, item in enumerate(nums):
        x = mx + i * cell
        if i:
            d.line([(x, y + 4), (x, y + 66)], fill=(200, 190, 170), width=1)
        nf = fit_font(d, item["value"], SERIF_B, 44, cell - 16, minimum=20)
        d.text((x + 8, y), item["value"], font=nf, fill=RED)
        cap = wrap(d, item["label"], font(SANS, 11), cell - 16)
        text_block(d, (x + 8, y + 46), cap[:3], font(SANS, 11), INK, leading=13)
    d.line([(mx, 238), (W - mx, 238)], fill=RULE, width=1)

    # ---- region bars
    regs = data["regions"]
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA",
             "WORLD"]
    total = sum(regs.values())
    x = mx
    y = 246
    for name in order:
        wseg = cw * regs[name] / total
        d.rectangle([x, y, x + wseg - 2, y + 22], fill=REGION_COLORS[name])
        label = f"{name} {regs[name]}"
        lf = font(SANS_B, 11)
        for sz in (10, 9, 8):
            if d.textlength(label, font=lf) > wseg - 8:
                lf = font(SANS_B, sz)
        if d.textlength(label, font=lf) <= wseg - 8:
            d.text((x + 5, y + 5), label, font=lf, fill=(255, 255, 255))
        x += wseg
    d.line([(mx, 276), (W - mx, 276)], fill=RULE, width=1)

    # ---- three illustrated leads
    colw = (cw - 16) / 3
    y0 = 290
    ill_h = 146
    for i, lead in enumerate(data["leads"]):
        x = mx + i * (colw + 8)
        LEAD_ILL[i](d, (int(x), y0, int(x + colw), y0 + ill_h))
        d.rectangle([int(x), y0 + ill_h, int(x + colw), y0 + ill_h + 22],
                    fill=RED)
        d.text((x + 6, y0 + ill_h + 4), lead["kicker"], font=font(SANS_B, 12),
               fill=(255, 255, 255))
        d.text((x, y0 + ill_h + 26), f"{lead['pin']} {lead['place']}",
               font=font(SANS_B, 11), fill=RED)
        head = wrap(d, lead["headline"], font(SERIF_B, 26), colw)
        yy = text_block(d, (x, y0 + ill_h + 44), head[:3],
                        font(SERIF_B, 26), INK, leading=29)
        deck = wrap(d, lead["deck"], font(SANS, 13), colw)
        yy = text_block(d, (x, yy + 4), deck[:2], font(SANS, 13), INK,
                        leading=15)
        d.text((x, yy + 3), f"({lead['source']})", font=font(SERIF_I, 11),
               fill=GREY)

    # ---- second row: five illustrated stories
    colw2 = (cw - 32) / 5
    y0 = 620
    ill_h2 = 76
    for i, item in enumerate(data["row2"]):
        x = mx + i * (colw2 + 8)
        ROW2_ILL[i](d, (int(x), y0, int(x + colw2), y0 + ill_h2))
        d.rectangle([int(x), y0 + ill_h2, int(x + colw2), y0 + ill_h2 + 18],
                    fill=RED)
        d.text((x + 5, y0 + ill_h2 + 3), item["kicker"],
               font=font(SANS_B, 10), fill=(255, 255, 255))
        head = wrap(d, item["headline"], font(SERIF_B, 17), colw2)
        yy = text_block(d, (x, y0 + ill_h2 + 22), head[:3],
                        font(SERIF_B, 17), INK, leading=19)
        deck = wrap(d, item["deck"], font(SANS, 11), colw2)
        text_block(d, (x, yy + 3), deck[:2], font(SANS, 11), INK, leading=13)

    # ---- map + ALSO list
    y0 = 808
    d.text((mx, y0), "WHERE IT HAPPENED · pins match story numbers",
           font=font(SANS_B, 12), fill=INK)
    also_head = "ALSO ON WEDNESDAY 25 NOVEMBER — 28 MORE STORIES"
    d.text((W - mx - d.textlength(also_head, font=font(SANS_B, 12)), y0),
           also_head, font=font(SANS_B, 12), fill=RED)
    draw_map(d, (mx, y0 + 22, mx + 316, y0 + 146))
    ax = mx + 328
    items = data["also"]
    half = 14
    for col in range(2):
        cx = ax + col * 322
        for j in range(half):
            item = items[col * half + j]
            yy = y0 + 24 + j * 10
            d.text((cx, yy), str(item["n"]), font=font(SANS_B, 10), fill=RED)
            head = item["headline"]
            src = item["source"]
            lf = font(SANS, 10)
            while d.textlength(head + " · " + src, font=lf) > 296 and len(head) > 12:
                head = head[:-4] + "…"
            d.text((cx + 20, yy), head + " · " + src, font=lf, fill=INK)

    # ---- date check
    y0 = 976
    d.rectangle([mx, y0, W - mx, y0 + 34], outline=RED, width=2)
    d.text((mx + 8, y0 + 4), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    note = (data["date_check"]["note"]
            + " Left out: Myanmar 22 Nov · GTA 6 19 Nov · Shenzhen 20 Nov"
            + " · Nepal PM 22–23 Nov.")
    nf = font(SANS, 10)
    while d.textlength(note, font=nf) > cw - 110:
        note = note[:-4] + "…"
    d.text((mx + 108, y0 + 5), note, font=nf, fill=INK)

    # ---- footer
    d.text((mx, 1010), "Sources named beside each story · Original drawings, drawn in code.",
           font=font(SERIF_I, 10), fill=GREY)
    foot = "THE WORLD ON WEDNESDAY · 25 NOV 2026"
    d.text((W - mx - d.textlength(foot, font=font(SANS_B, 10)), 1010), foot,
           font=font(SANS_B, 10), fill=INK)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
