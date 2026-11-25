#!/usr/bin/env python3
"""Render the Wednesday 25 November 2026 front page (v3) as a 1024x1024 PNG.

Architecture: a tiny flow engine. The page is a list of section callables
(SECTIONS), each receiving a Page object that carries the canvas, the
cursor and the story data. Illustrations live in a SCENES registry keyed
by story number, so the layout code never knows how a scene is drawn.
Everything is drawn with Pillow only; no network, no randomness.
Run:  python3 render.py  ->  writes entry.png next to this file.
"""

import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 22
CW = W - 2 * MARGIN  # content width

# ---------------------------------------------------------------- palette
INK = (26, 22, 18)
PAPER = (250, 244, 228)
RED = (178, 30, 26)
DARKRED = (140, 20, 18)
BLACK = (12, 12, 14)
NAVY = (16, 24, 52)
SKY = (168, 208, 232)
TAN = (232, 214, 170)
GREY = (120, 118, 112)
MIDGREY = (90, 88, 84)

REGION_FILL = {
    "EUROPE": (28, 62, 122),
    "AMERICAS": (104, 52, 150),
    "ASIA-PACIFIC": (16, 130, 118),
    "MIDDLE EAST": (198, 148, 32),
    "AFRICA": (214, 96, 28),
    "WORLD": (120, 118, 112),
}

# ---------------------------------------------------------------- fonts
_FDIR = "/usr/share/fonts/truetype/liberation"


def face(kind, size):
    """Load a Liberation face; kind is one of serif/serif-b/serif-i/sans/..."""
    names = {
        "serif": "LiberationSerif-Regular.ttf",
        "serif-b": "LiberationSerif-Bold.ttf",
        "serif-i": "LiberationSerif-Italic.ttf",
        "serif-bi": "LiberationSerif-BoldItalic.ttf",
        "sans": "LiberationSans-Regular.ttf",
        "sans-b": "LiberationSans-Bold.ttf",
        "sans-i": "LiberationSans-Italic.ttf",
    }
    path = os.path.join(_FDIR, names[kind])
    return ImageFont.truetype(path, size)


def fit(font, text, max_w):
    """Split text into lines that fit max_w, word by word."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Page:
    """Canvas + vertical cursor + small drawing helpers."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 0

    # -- primitives ------------------------------------------------------
    def bar(self, h, fill):
        self.d.rectangle([0, self.y, W, self.y + h - 1], fill=fill)
        self.y += h

    def rule(self, weight=1, color=INK, gap=0):
        self.d.line([(MARGIN, self.y), (W - MARGIN, self.y)], fill=color,
                    width=weight)
        self.y += weight + gap

    def text(self, x, y, s, font, fill=INK, anchor="la"):
        self.d.text((x, y), s, font=font, fill=fill, anchor=anchor)

    def para(self, x, y, s, font, max_w, fill=INK, leading=None):
        """Word-wrapped paragraph; returns y just below the last line."""
        lh = leading or int(font.size * 1.18)
        for line in fit(font, s, max_w):
            self.d.text((x, y), line, font=font, fill=fill)
            y += lh
        return y

    def centred(self, cx, y, s, font, fill=INK):
        self.d.text((cx, y), s, font=font, fill=fill, anchor="ma")

    # -- shared blocks ---------------------------------------------------
    def kicker_strip(self, x, y, w, label, fill=RED):
        """Red strip with white bold sans label (story kicker)."""
        self.d.rectangle([x, y, x + w - 1, y + 15], fill=fill)
        self.d.text((x + 6, y + 2), label, font=face("sans-b", 10),
                    fill=(255, 255, 255))
        return y + 16

    def caption_bar(self, x, y, w, label, fill=BLACK):
        self.d.rectangle([x, y, x + w - 1, y + 15], fill=fill)
        self.d.text((x + 6, y + 2), label, font=face("sans-b", 10),
                    fill=(255, 255, 255))
        return y + 16


def load_data(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def by_number(data, n):
    for pool in (data["leads"], data["grid"]):
        for story in pool:
            if story["pin"] == n:
                return story
    return None

# ---------------------------------------------------------------- scenes
# Each painter receives (draw, x, y, w, h) and draws one flat illustration.
# Numbers match the story pins; the registry is the only place scenes live.

def _stars(d, x, y, w, h, n=14, seed=7):
    import random
    rng = random.Random(seed)
    for _ in range(n):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 18)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))


def scene_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    # chip
    cx, cy = x + 26, y + 18
    d.rectangle([cx, cy, cx + 44, cy + 34], fill=(18, 120, 90))
    d.rectangle([cx + 12, cy + 9, cx + 32, cy + 25], fill=(232, 190, 60))
    for i in range(3):
        d.line([(cx + 6 + i * 14, cy - 5), (cx + 6 + i * 14, cy)], fill=(200, 200, 200), width=2)
        d.line([(cx + 6 + i * 14, cy + 34), (cx + 6 + i * 14, cy + 39)], fill=(200, 200, 200), width=2)
    # falling line
    pts = [(x + 92, y + 22), (x + 150, y + 30), (x + 195, y + 26),
           (x + 235, y + 48), (x + 265, y + 66), (x + 292, y + 82)]
    d.line(pts, fill=(235, 70, 60), width=3)
    d.polygon([(x + 292, y + 82), (x + 282, y + 78), (x + 290, y + 92)],
              fill=(235, 70, 60))
    # red badge
    d.rectangle([x + w - 88, y + 10, x + w - 12, y + 32], fill=RED)
    d.text((x + w - 50, y + 14), "−6.2%", font=face("sans-b", 15),
           fill=(255, 255, 255), anchor="ma")


def scene_space(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(10, 16, 44))
    _stars(d, x, y, w, h, n=16, seed=11)
    # rocket
    rx, ry = x + 62, y + 34
    d.polygon([(rx, ry), (rx - 16, ry + 44), (rx + 16, ry + 44)], fill=(240, 240, 240))
    d.polygon([(rx - 16, ry + 44), (rx - 26, ry + 58), (rx - 10, ry + 50)], fill=RED)
    d.polygon([(rx + 16, ry + 44), (rx + 26, ry + 58), (rx + 10, ry + 50)], fill=RED)
    d.rectangle([rx - 4, ry + 44, rx + 4, ry + 58], fill=(250, 180, 60))
    # station
    sx, sy = x + 180, y + 26
    d.rectangle([sx, sy, sx + 96, sy + 12], fill=(200, 205, 215))
    d.rectangle([sx + 18, sy - 8, sx + 40, sy + 20], fill=(150, 158, 175))
    d.rectangle([sx + 56, sy - 8, sx + 78, sy + 20], fill=(150, 158, 175))
    d.rectangle([sx - 26, sy + 2, sx, sy + 10], fill=(60, 110, 190))
    d.rectangle([sx + 96, sy + 2, sx + 122, sy + 10], fill=(60, 110, 190))
    # ground flags
    d.rectangle([x + 150, y + h - 26, x + 170, y + h - 14], fill=(20, 120, 70))
    d.rectangle([x + 176, y + h - 26, x + 196, y + h - 14], fill=RED)


def scene_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    d.rectangle([x, y + h - 26, x + w - 1, y + h - 1], fill=(24, 60, 120))
    # containers, one row sitting on the deck
    cols = [(232, 190, 60), (40, 140, 90), (210, 60, 50), (60, 110, 190),
            (240, 120, 40)]
    cw = 40
    for i, c in enumerate(cols):
        bx = x + 16 + i * (cw + 4)
        by = y + 36
        d.rectangle([bx, by, bx + cw, by + 26], fill=c)
        d.line([(bx + cw // 2, by), (bx + cw // 2, by + 26)], fill=(0, 0, 0), width=1)
    # hull
    d.polygon([(x + 8, y + 62), (x + w - 8, y + 62),
               (x + w - 26, y + h - 8), (x + 26, y + h - 8)], fill=(20, 20, 26))
    # bridge, right end
    d.rectangle([x + w - 52, y + 30, x + w - 16, y + 62], fill=(240, 240, 240))
    for i in range(3):
        d.rectangle([x + w - 46, y + 36 + i * 9, x + w - 22, y + 42 + i * 9],
                    fill=(60, 110, 190))
    # stamp, top left, clear of the containers
    d.ellipse([x + 8, y + 4, x + 80, y + 30], outline=RED, width=3)
    d.text((x + 44, y + 7), "UP TO", font=face("sans-b", 11),
           fill=RED, anchor="ma")
    d.text((x + 44, y + 18), "20%", font=face("sans-b", 13),
           fill=RED, anchor="ma")


def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(250, 200, 110))
    d.ellipse([x + 22, y + 8, x + 62, y + 48], fill=(245, 160, 40))
    d.rectangle([x, y + h - 30, x + w - 1, y + h - 1], fill=(20, 70, 110))
    for bx in (x + 14, x + 96):
        d.rectangle([bx, y + 40, bx + 66, y + 52], fill=(40, 40, 48))
        d.rectangle([bx + 52, y + 28, bx + 62, y + 40], fill=(40, 40, 48))
        d.polygon([(bx + 8, y + 40), (bx + 16, y + 30), (bx + 24, y + 40)],
                  fill=(235, 90, 40))
    d.text((x + w - 8, y + h - 26), "2 TANKERS", font=face("sans-b", 11),
           fill=(255, 255, 255), anchor="ra")


def scene_solomon(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(150, 205, 235))
    d.ellipse([x + w - 46, y + 6, x + w - 10, y + 42], fill=(250, 220, 90))
    d.polygon([(x, y + h - 1), (x + 60, y + 34), (x + w, y + 52),
               (x + w, y + h - 1)], fill=(40, 140, 80))
    d.polygon([(x + 96, y + 52), (x + 108, y + 22), (x + 120, y + 52)],
              fill=(24, 90, 50))
    d.rectangle([x + 116, y + 52, x + 120, y + 66], fill=(120, 80, 40))
    # flag
    d.rectangle([x + 130, y + 18, x + 132, y + 52], fill=(60, 60, 60))
    d.polygon([(x + 132, y + 18), (x + 162, y + 25), (x + 132, y + 32)],
              fill=(30, 60, 160))
    d.text((x + 8, y + 6), "TREATY", font=face("sans-b", 11), fill=INK)


def scene_energy(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(30, 30, 40))
    d.polygon([(x + 30, y + 52), (x + 52, y + 14), (x + 74, y + 52)],
              fill=(245, 150, 40))
    d.polygon([(x + 40, y + 52), (x + 52, y + 30), (x + 64, y + 52)],
              fill=(250, 210, 60))
    d.rectangle([x + w - 92, y + 12, x + w - 12, y + 38], fill=RED)
    d.text((x + w - 52, y + 16), "+26%", font=face("sans-b", 16),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + w - 52, y + 44), "£2,166", font=face("sans-b", 14),
           fill=(255, 255, 255), anchor="ma")


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(214, 186, 140))
    d.polygon([(x + 10, y + 12), (x + w - 10, y + 12), (x + w // 2, y + h - 8)],
              fill=(120, 82, 48))
    d.polygon([(x + 60, y + 12), (x + w - 60, y + 12), (x + w // 2, y + h - 26)],
              fill=(70, 48, 28))
    d.rectangle([x + w - 62, y + 10, x + w - 12, y + 34], fill=RED)
    d.text((x + w - 37, y + 13), "26", font=face("sans-b", 15),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + 8, y + h - 20), "100 m DOWN", font=face("sans-b", 11),
           fill=(255, 255, 255))


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(222, 210, 190))
    for bx, bh in ((x + 8, 46), (x + 52, 58), (x + 104, 40), (x + 142, 52)):
        d.rectangle([bx, y + h - 18 - bh, bx + 40, y + h - 18], fill=(110, 104, 96))
        for wy in range(2):
            d.rectangle([bx + 6, y + h - 14 - bh + wy * 16, bx + 14,
                         y + h - 6 - bh + wy * 16], fill=(60, 58, 54))
    d.ellipse([x + 120, y + 6, x + 150, y + 30], fill=(150, 146, 140))
    d.ellipse([x + 140, y + 2, x + 172, y + 26], fill=(170, 166, 160))
    d.rectangle([x, y + h - 18, x + w - 1, y + h - 1], fill=(90, 86, 80))


def scene_cia(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(18, 22, 38))
    # capitol-ish building
    d.rectangle([x + 18, y + 30, x + 84, y + h - 14], fill=(235, 232, 225))
    d.polygon([(x + 14, y + 30), (x + 51, y + 12), (x + 88, y + 30)],
              fill=(235, 232, 225))
    for i in range(4):
        d.rectangle([x + 24 + i * 16, y + 38, x + 32 + i * 16, y + h - 14],
                    fill=(180, 176, 168))
    # padlock
    lx, ly = x + 118, y + 26
    d.rectangle([lx + 4, ly + 14, lx + 36, ly + 42], fill=RED)
    d.arc([lx + 8, ly, lx + 32, ly + 20], 180, 360, fill=(255, 220, 60), width=4)
    d.ellipse([lx + 17, ly + 24, lx + 23, ly + 30], fill=(255, 220, 60))


def scene_port(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 220, 170))
    d.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(250, 190, 60))
    d.rectangle([x, y + h - 16, x + w - 1, y + h - 1], fill=(40, 90, 130))
    for cx in (x + 20, x + 86):
        d.line([(cx, y + h - 16), (cx, y + 14)], fill=(60, 60, 60), width=3)
        d.line([(cx, y + 14), (cx + 44, y + 14)], fill=(60, 60, 60), width=3)
        d.line([(cx + 44, y + 14), (cx + 36, y + h - 16)], fill=(60, 60, 60), width=2)
    d.text((x + 8, y + 6), "PORT", font=face("sans-b", 11), fill=INK)


def scene_garment(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(250, 230, 150))
    d.rectangle([x + 16, y + 26, x + 116, y + h - 12], fill=(230, 190, 80))
    for i in range(4):
        d.rectangle([x + 24 + i * 24, y + 34, x + 40 + i * 24, y + 48],
                    fill=(120, 80, 30))
    d.polygon([(x + 12, y + 26), (x + 66, y + 8), (x + 120, y + 26)],
              fill=(180, 60, 50))
    d.rectangle([x + w - 78, y + 8, x + w - 10, y + 32], fill=(20, 130, 70))
    d.text((x + w - 44, y + 11), "+36%", font=face("sans-b", 14),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + w - 44, y + 38), "17,500 tk", font=face("sans-b", 11),
           fill=INK, anchor="ma")


def scene_inflation(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 235, 250))
    for i in range(5):
        gy = y + 12 + i * 12
        d.line([(x + 10, gy), (x + w - 10, gy)], fill=(210, 205, 220), width=1)
    pts = [(x + 16, y + h - 18), (x + 56, y + h - 26), (x + 96, y + h - 34),
           (x + 136, y + h - 48), (x + w - 16, y + 14)]
    d.line(pts, fill=(140, 40, 160), width=3)
    d.ellipse([x + w - 22, y + 8, x + w - 10, y + 20], fill=(140, 40, 160))
    d.text((x + 10, y + 6), "4.9%", font=face("sans-b", 16), fill=RED)


def scene_ebola(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(215, 232, 240))
    d.polygon([(x + 16, y + h - 18), (x + 66, y + 18), (x + 116, y + h - 18)],
              fill=(245, 245, 240))
    d.rectangle([x + 60, y + 34, x + 72, y + 58], fill=RED)
    d.rectangle([x + 52, y + 42, x + 80, y + 50], fill=RED)
    # ambulance
    ax, ay = x + 118, y + h - 40
    d.rectangle([ax, ay, ax + 62, ay + 26], fill=(255, 255, 255))
    d.rectangle([ax + 44, ay + 4, ax + 62, ay + 26], fill=(240, 240, 240))
    d.rectangle([ax + 26, ay + 8, ax + 34, ay + 18], fill=RED)
    d.rectangle([ax + 36, ay + 8, ax + 42, ay + 18], fill=RED)
    d.ellipse([ax + 10, ay + 22, ax + 20, ay + 32], fill=(30, 30, 30))
    d.ellipse([ax + 44, ay + 22, ax + 54, ay + 32], fill=(30, 30, 30))


SCENES = {
    1: scene_kospi, 2: scene_space, 3: scene_tariffs, 4: scene_hormuz,
    5: scene_solomon, 6: scene_energy, 7: scene_mine, 8: scene_gaza,
    9: scene_cia, 10: scene_port, 11: scene_garment, 12: scene_inflation,
    13: scene_ebola,
}

# ---------------------------------------------------------------- sections

def sec_topbar(p, data):
    p.bar(26, BLACK)
    p.d.text((MARGIN, 5), data["paper"].upper(), font=face("sans-b", 12),
             fill=(255, 255, 255))
    right = "36 STORIES · 6 REGIONS · EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026"
    p.d.text((W - MARGIN, 5), right, font=face("sans-b", 12),
             fill=(255, 255, 255), anchor="ra")
    p.y += 4


def sec_masthead(p, data):
    p.d.text((MARGIN, p.y), "Wednesday 25 November 2026",
             font=face("serif-b", 54), fill=INK)
    p.y += 66
    sub = ("Kospi crashes −6.2% · Pakistan's first astronaut docks at "
           "Tiangong · US proposes tariffs of up to 20%")
    p.d.text((MARGIN, p.y), sub, font=face("serif-i", 19), fill=RED)
    p.y += 24


def sec_numbers(p, data):
    p.rule(2, INK, gap=6)
    cols = 6
    cell = CW // cols
    top = p.y
    for i, item in enumerate(data["numbers"]):
        x = MARGIN + i * cell
        if i:
            p.d.line([(x, top + 2), (x, top + 42)], fill=GREY, width=1)
        p.d.text((x + 8, top), item["value"], font=face("serif-b", 28),
                 fill=RED)
        p.d.text((x + 8, top + 32), item["label"], font=face("sans", 10),
                 fill=INK)
    p.y = top + 46
    p.rule(1, INK, gap=6)


def sec_utc(p, data):
    p.bar(20, BLACK)
    p.d.text((MARGIN, p.y - 20 + 3), "THE DAY IN UTC", font=face("sans-b", 11),
             fill=(255, 200, 60))
    bits, x = [], MARGIN + 118
    for ev in data["utc"]:
        bits.append((x, ev))
        x += int(face("sans", 10).getlength(ev["time"] + "  " + ev["event"] + "   ·   "))
    for x0, ev in bits:
        p.d.text((x0, p.y - 20 + 4), ev["time"], font=face("sans-b", 10),
                 fill=(255, 255, 255))
        w = face("sans-b", 10).getlength(ev["time"] + " ")
        p.d.text((x0 + w, p.y - 20 + 4), ev["event"], font=face("sans", 10),
                 fill=(220, 220, 220))
    p.y += 5


def sec_regions(p, data):
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDDLE EAST", "AFRICA",
             "WORLD"]
    total = sum(data["regions"].values())
    x = MARGIN
    for name in order:
        w = int(CW * data["regions"][name] / total)
        p.d.rectangle([x, p.y, x + w - 1, p.y + 15], fill=REGION_FILL[name])
        p.d.text((x + 5, p.y + 2), "%s %d" % (name, data["regions"][name]),
                 font=face("sans-b", 9), fill=(255, 255, 255))
        x += w
    p.y += 19


def _story_block(p, story, x, y, w, img_h, head_size, deck_size):
    """Illustration + kicker + place + headline + deck + source."""
    d = p.d
    SCENES[story["pin"]](d, x, y, w, img_h)
    y += img_h
    y = p.kicker_strip(x, y, w, story["kicker"])
    y += 3
    d.text((x, y), story["place"], font=face("sans-b", 11), fill=RED)
    y += 14
    y = p.para(x, y, story["headline"], face("serif-b", head_size), w,
               leading=head_size + 3)
    y += 2
    y = p.para(x, y, story["deck"], face("serif", deck_size), w,
               leading=deck_size + 3)
    y += 2
    d.text((x, y), "(%s)" % story["source"], font=face("serif-i", 10),
           fill=MIDGREY)
    return y + 12


def sec_leads(p, data):
    gap, cols = 14, 3
    cell = (CW - gap * (cols - 1)) // cols
    top = p.y
    bottom = top
    for i, story in enumerate(data["leads"]):
        x = MARGIN + i * (cell + gap)
        end = _story_block(p, story, x, top, cell, 92, 24, 12)
        bottom = max(bottom, end)
    p.y = bottom + 2


def sec_grid(p, data, rows):
    gap, cols = 12, 5
    cell = (CW - gap * (cols - 1)) // cols
    for row in rows:
        top = p.y
        bottom = top
        for j, story in enumerate(row):
            x = MARGIN + j * (cell + gap)
            end = _story_block(p, story, x, top, cell, 58, 14, 10)
            bottom = max(bottom, end)
        p.y = bottom + 2


def _pin_xy(bx, by, bw, bh, lon, lat):
    return (bx + (lon + 180.0) / 360.0 * bw,
            by + (90.0 - lat) / 180.0 * bh)


def sec_map_also(p, data):
    p.d.text((MARGIN, p.y), "WHERE IT HAPPENED · pins match story numbers",
             font=face("sans-b", 11), fill=INK)
    p.d.text((W - MARGIN, p.y), "ALSO ON WEDNESDAY 25 NOVEMBER — 23 MORE STORIES",
             font=face("sans-b", 11), fill=RED, anchor="ra")
    p.y += 16
    top = p.y
    map_w, map_h = 330, 112
    d = p.d
    d.rectangle([MARGIN, top, MARGIN + map_w - 1, top + map_h - 1],
                fill=(205, 225, 240))
    # rough continents, tan on pale blue
    continents = [
        [(14, 26), (58, 8), (96, 16), (88, 52), (52, 66), (20, 52)],
        [(72, 72), (96, 70), (104, 96), (82, 110), (68, 92)],
        [(168, 22), (196, 12), (214, 26), (200, 46), (176, 40)],
        [(176, 52), (206, 50), (216, 78), (196, 104), (180, 82)],
        [(222, 20), (300, 10), (322, 34), (296, 58), (262, 66), (228, 48)],
        [(292, 92), (318, 88), (324, 104), (300, 110)],
    ]
    for poly in continents:
        d.polygon([(MARGIN + px, top + py) for px, py in poly], fill=TAN)
    pins = {1: (127, 38), 2: (99, 40), 3: (-77, 39), 4: (56, 26),
            5: (160, -9), 6: (0, 51), 7: (107, -7), 8: (34, 31),
            9: (-95, 32), 10: (43, 15), 11: (90, 24), 12: (151, -34),
            13: (29, 1)}
    for n, (lon, lat) in pins.items():
        px, py = _pin_xy(MARGIN, top, map_w, map_h, lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py - 5), str(n), font=face("sans-b", 8),
               fill=(255, 255, 255), anchor="ma")
    # ALSO list, two columns
    also = data["also"]
    col_x = [MARGIN + map_w + 16, MARGIN + map_w + 16 + 300]
    col_w = 292
    half = 12
    for ci, chunk in enumerate((also[:half], also[half:])):
        y = top + 1
        for item in chunk:
            num = "%d " % item["n"]
            d.text((col_x[ci], y), num, font=face("sans-b", 9), fill=RED)
            nw = face("sans-b", 9).getlength(num)
            head = item["headline"]
            if face("sans", 9).getlength(head) > col_w - nw - 62:
                while face("sans", 9).getlength(head + "…") > col_w - nw - 62:
                    head = head[:-1]
                head += "…"
            d.text((col_x[ci] + nw, y), head, font=face("sans", 9), fill=INK)
            sw = face("sans", 9).getlength(head)
            d.text((col_x[ci] + nw + sw + 4, y), "· " + item["source"],
                   font=face("sans-i", 8), fill=MIDGREY)
            y += 9
    p.y = top + map_h + 6


def sec_datecheck(p, data):
    top = p.y
    d = p.d
    d.rectangle([MARGIN, top, W - MARGIN - 1, top + 58], outline=RED, width=2)
    d.text((MARGIN + 8, top + 4), "DATE CHECK", font=face("sans-b", 11),
           fill=RED)
    y = p.para(MARGIN + 8, top + 18, data["date_check"]["note"],
               face("sans", 10), CW - 16, leading=12)
    y = p.para(MARGIN + 8, y, data["date_check"]["left_out"],
               face("sans", 10), CW - 16, leading=12)
    p.y = top + 60


def sec_footer(p, data):
    p.d.text((MARGIN, p.y), "Sources named beside each story · Original "
             "drawings, drawn in code.", font=face("sans-i", 10),
             fill=MIDGREY)
    p.d.text((W - MARGIN, p.y), "THE WORLD ON WEDNESDAY · 25 NOV 2026",
             font=face("sans-b", 10), fill=INK, anchor="ra")
    p.y += 14


SECTIONS = [
    sec_topbar, sec_masthead, sec_numbers, sec_utc, sec_regions,
    sec_leads,
    lambda p, data: sec_grid(p, data, [sorted(data["grid"],
                                              key=lambda s: s["pin"])[:5]]),
    lambda p, data: sec_grid(p, data, [sorted(data["grid"],
                                              key=lambda s: s["pin"])[5:]]),
    sec_map_also, sec_datecheck, sec_footer,
]


def build(data_path, out_path):
    data = load_data(data_path)
    p = Page()
    for section in SECTIONS:
        section(p, data)
    print("final cursor y =", p.y, "(canvas height", H, ")")
    assert p.y <= H, "layout overflow: %d > %d" % (p.y, H)
    p.img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "stories_20261125-v3.json"),
          os.path.join(here, "entry.png"))
