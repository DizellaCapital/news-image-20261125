#!/usr/bin/env python3
"""THE WEDNESDAY LEDGER — Wednesday 25 November 2026 front page.

Fresh renderer written in this session. Draws one 1024x1024 PNG that sums
up the world's news of Wednesday 25 November 2026 as a newspaper front
page: masthead, key-numbers strip, one hero story with a drawn sea scene,
two leads with drawn illustrations, four medium cards, a six-moment
timeline, a dotted world map with numbered pins, a 29-item ALSO list in
which every item carries a region tag and a source, and a DATE CHECK box
naming the stories deliberately left out.

All 36 stories are dated 25 November 2026 (happened or first reported
that day), verified against Reuters, RFE/RL, WH News, BBC and
BusinessWorld reporting crawled on 25 November 2026. Story data lives in
stories_20261125.json; this file only lays it out.

Deterministic: two runs must be byte-identical (no timestamps, no random
input, fixed font files, PNG written with fixed settings).
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "stories_20261125.json")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
BG = (247, 242, 230)       # warm cream paper
PAPER2 = (238, 231, 214)   # slightly darker cream for panels
INK = (24, 24, 24)         # near-black text
NAVY = (20, 28, 54)        # masthead / night sea
NAVY2 = (34, 48, 88)       # lighter navy
SEA = (16, 38, 74)         # hero sea
RED = (164, 22, 34)        # accent red
GOLD = (198, 158, 38)      # gold accent
GREY = (96, 94, 88)        # secondary text
LINE = (120, 110, 90)      # hairline rules
WHITE = (250, 248, 242)

REGION_FILL = {
    "EUROPE": (15, 118, 110),
    "MIDDLE EAST": (185, 28, 28),
    "ASIA-PACIFIC": (21, 128, 61),
    "AMERICAS": (124, 58, 237),
    "AFRICA": (194, 65, 12),
    "OCEANIA": (3, 105, 161),
    "WORLD": (87, 83, 78),
}

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(path, size):
    return ImageFont.truetype(path, size)


def serif_b(size):
    return font(f"{FD}/DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font(f"{FD}/DejaVuSerif.ttf", size)


def sans_b(size):
    return font(f"{FD}/DejaVuSans-Bold.ttf", size)


def sans(size):
    return font(f"{FD}/DejaVuSans.ttf", size)


def sans_i(size):
    return font(f"{FL}/LiberationSans-Italic.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, lh=None):
    """Draw wrapped text; returns y just below the last line."""
    if lh is None:
        lh = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def trunc(draw, text, fnt, max_w):
    """Truncate with an ellipsis so the text fits max_w."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text[:-1]
    return text + "…"


def rule(draw, x0, y, x1, fill=LINE, w=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def pin(draw, cx, cy, n, r=8):
    """Numbered map pin: red disc, white ring, white number."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                 outline=WHITE, width=2)
    t = str(n)
    f = sans_b(10 if n < 10 else 9)
    tw = draw.textlength(t, font=f)
    draw.text((cx - tw / 2, cy - r + 2), t, font=f, fill=WHITE)


# --- dotted world map: 56 cols x 12 rows, hand-drawn rough continents ---
MAP_GRID = [
    "..########################.#######..####################",
    "..##################......#########.#####################",
    "..#################.......#########.#####################",
    "...###############.......############.##################.",
    "....############.........############.##################.",
    "......########...........#############..###############.",
    ".........####...#######...###########.#############.....",
    "................#######....#########...##########.......",
    "................######......######............######....",
    ".................####........####............########...",
    ".................###..........##..............######....",
    "..................##....................................",
]


def map_xy(col, row, ox, oy, cell):
    return ox + col * cell + cell / 2, oy + row * cell + cell / 2


def draw_map(draw, ox, oy, cell, pins):
    for r, row in enumerate(MAP_GRID):
        for c, ch in enumerate(row):
            if ch == "#":
                cx, cy = map_xy(c, r, ox, oy, cell)
                draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=NAVY2)
    for (col, row, n) in pins:
        cx, cy = map_xy(col, row, ox, oy, cell)
        pin(draw, cx, cy, n, r=8)


def draw_sea_scene(draw, x, y, w, h):
    """Hero illustration: night sea, two ships, a drone, a burst."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx, sy in [(30, 12), (90, 26), (150, 10), (210, 22), (260, 14),
                   (330, 26), (390, 12), (450, 24), (520, 14), (580, 26),
                   (120, 40), (300, 44), (470, 42)]:
        draw.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                     fill=WHITE)
    # moon
    draw.ellipse([x + w - 70, y + 14, x + w - 34, y + 50], fill=(235, 225, 190))
    # sea
    draw.rectangle([x, y + h - 58, x + w, y + h], fill=SEA)
    draw.line([x, y + h - 58, x + w, y + h - 58], fill=GOLD, width=2)
    # moonlight shimmer (three short strokes, no ladder)
    for i, ww in enumerate((46, 34, 52)):
        yy = y + h - 48 + i * 9
        draw.line([x + w - 126, yy, x + w - 126 + ww, yy],
                  fill=(120, 130, 170), width=2)
    # ship 1 (cargo, left): hull sits IN the sea, below the waterline,
    # superstructure above it; light steel so it reads against the dark sea
    hx, hy = x + 40, y + h - 58
    draw.polygon([(hx, hy), (hx + 150, hy), (hx + 140, hy + 16),
                  (hx + 10, hy + 16)], fill=(74, 86, 118))
    draw.line([hx, hy, hx + 150, hy], fill=WHITE, width=2)
    draw.rectangle([hx + 30, hy - 16, hx + 70, hy], fill=(74, 86, 118))
    draw.rectangle([hx + 78, hy - 12, hx + 118, hy], fill=(74, 86, 118))
    for wx in range(hx + 36, hx + 66, 10):
        draw.rectangle([wx, hy - 12, wx + 5, hy - 6], fill=GOLD)
    # ship 2 (warship, right) with burst above it
    hx2, hy2 = x + w - 210, y + h - 58
    draw.polygon([(hx2, hy2), (hx2 + 150, hy2), (hx2 + 140, hy2 + 16),
                  (hx2 + 10, hy2 + 16)], fill=(74, 86, 118))
    draw.line([hx2, hy2, hx2 + 150, hy2], fill=WHITE, width=2)
    draw.polygon([(hx2 + 96, hy2), (hx2 + 118, hy2),
                  (hx2 + 108, hy2 - 26)], fill=(74, 86, 118))
    # explosion burst over ship 2 (kept inside the scene: centre 22 px
    # above the waterline, radii <= 11, so nothing pokes above the top)
    bx, by = hx2 + 108, hy2 - 22
    for (dx, dy, r) in [(0, 0, 11), (-11, 4, 7), (10, 5, 8),
                        (-4, -10, 6), (7, -9, 6), (0, 10, 5)]:
        draw.ellipse([bx + dx - r, by + dy - r, bx + dx + r, by + dy + r],
                     fill=(232, 150, 40))
    draw.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 220, 120))
    # drone (small quad-copter, upper left of burst)
    dx, dy = x + 250, y + 34
    draw.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(200, 200, 200))
    for ox, oy in [(-12, -8), (12, -8), (-12, 8), (12, 8)]:
        draw.line([dx, dy, dx + ox, dy + oy], fill=(200, 200, 200), width=1)
        draw.ellipse([dx + ox - 5, dy + oy - 1, dx + ox + 5, dy + oy + 1],
                     fill=(220, 220, 220))
    # labels sit in the sea, below the hulls, so they never overlap them
    lf = sans_b(10)
    draw.text((x + 44, y + h - 16), "GULF OF FINLAND", font=lf, fill=WHITE)
    draw.text((x + w - 190, y + h - 16), "BENGHAZI", font=lf, fill=WHITE)


def draw_tower_scene(draw, x, y, w, h):
    """Riyadh lead illustration: dusk sky, tower silhouette, smoke.
    Height-aware: everything fits inside the h-tall band."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(58 + (214 - 58) * t)
        g = int(44 + (120 - 44) * t)
        draw.line([x, y + i, x + w, y + i], fill=(r, g, 60))
    # tower: stepped silhouette
    tx = x + w // 2 - 12
    draw.rectangle([tx, y + 10, tx + 24, y + h], fill=(16, 16, 22))
    draw.rectangle([tx - 5, y + 18, tx + 29, y + h], fill=(16, 16, 22))
    draw.rectangle([tx + 8, y + 4, tx + 16, y + 10], fill=(16, 16, 22))
    for wy in (y + 22, y + 30):
        draw.rectangle([tx + 2, wy, tx + 22, wy + 3], fill=GOLD)
    # smoke plume
    for (sx, sy, sr) in [(tx + 38, y + 10, 8), (tx + 48, y + 5, 10),
                         (tx + 58, y + 12, 7)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(150, 146, 140))
    # drone dot
    draw.ellipse([x + 22, y + 10, x + 27, y + 15], fill=(220, 220, 220))


def draw_breach_scene(draw, x, y, w, h):
    """CIA/ODNI lead illustration: dark panel, padlock, warning triangle.
    Height-aware: everything fits inside the h-tall band."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 22, 40))
    # binary dots (two rows only)
    for i in range(6):
        for j in range(2):
            px = x + 12 + i * 15
            py = y + 6 + j * 12
            draw.rectangle([px, py, px + 6, py + 6],
                           fill=(60, 80, 140) if (i + j) % 2 else (90, 110, 170))
    # padlock (small, top-right)
    lx, ly = x + w - 46, y + 4
    draw.arc([lx, ly, lx + 24, ly + 20], 180, 360, fill=GOLD, width=3)
    draw.rounded_rectangle([lx - 3, ly + 16, lx + 27, ly + 32],
                           radius=3, fill=GOLD)
    draw.ellipse([lx + 8, ly + 21, lx + 16, ly + 29], fill=NAVY)
    # warning triangle (bottom-left)
    tx, ty = x + 12, y + h - 16
    draw.polygon([(tx, ty + 14), (tx + 8, ty), (tx + 16, ty + 14)],
                 fill=RED)
    draw.text((tx + 6, ty + 4), "!", font=sans_b(9), fill=WHITE)


def build():
    with open(DATA, encoding="utf-8") as fh:
        d = json.load(fh)
    img = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(img)
    mx = 24                      # side margin
    rx = W - mx                  # right edge

    # ---- top navy bar -------------------------------------------------
    dr.rectangle([0, 0, W, 6], fill=NAVY)

    # ---- masthead ------------------------------------------------------
    mast = serif_b(44)
    dr.text((mx, 16), d["paper"], font=mast, fill=NAVY)
    date_f = sans_b(15)
    dr.text((rx - dr.textlength("WEDNESDAY 25 NOVEMBER 2026", font=date_f), 22),
            "WEDNESDAY 25 NOVEMBER 2026", font=date_f, fill=RED)
    sub_f = sans(12)
    dr.text((rx - dr.textlength("ONE PAGE · 36 STORIES · 7 REGIONS", font=sub_f), 44),
            "ONE PAGE · 36 STORIES · 7 REGIONS", font=sub_f, fill=GREY)
    dr.text((rx - dr.textlength("Verified to 08:00 UTC", font=sub_f), 62),
            "Verified to 08:00 UTC", font=sub_f, fill=GREY)
    rule(dr, mx, 84, rx, fill=NAVY, w=2)
    deck_f = serif(14)
    dr.text((mx, 90),
            "The world's news of Wednesday 25 November 2026 — on a single page.",
            font=deck_f, fill=INK)
    dr.text((rx - dr.textlength("Price: one careful look", font=sans_i(12)), 92),
            "Price: one careful look", font=sans_i(12), fill=GREY)
    rule(dr, mx, 108, rx, fill=RED, w=2)

    # ---- key numbers strip --------------------------------------------
    nums = d["numbers"]
    bw = (rx - mx - 5 * 8) // 6
    ny, nh = 114, 44
    for i, item in enumerate(nums):
        x0 = mx + i * (bw + 8)
        dr.rectangle([x0, ny, x0 + bw, ny + nh], fill=PAPER2,
                     outline=LINE, width=1)
        vf = serif_b(19)
        dr.text((x0 + 8, ny + 3), item["value"], font=vf, fill=RED)
        lf = sans(9)
        y = draw_wrapped(dr, x0 + 8, ny + 26, item["label"], lf, bw - 16,
                         fill=GREY, lh=10)
    rule(dr, mx, 164, rx, fill=LINE, w=1)

    # ---- hero (left) ----------------------------------------------------
    hero = d["hero"]
    hx0, hx1 = mx, 664
    hy = 172
    draw_sea_scene(dr, hx0, hy, hx1 - hx0, 92)
    hy += 100
    dr.text((hx0, hy), hero["kicker"], font=sans_b(11), fill=RED)
    hy += 16
    hy = draw_wrapped(dr, hx0, hy, hero["headline"], serif_b(28),
                      hx1 - hx0, fill=NAVY, lh=32)
    hy += 4
    hy = draw_wrapped(dr, hx0, hy, hero["deck"], serif(12),
                      hx1 - hx0, fill=INK, lh=15)
    hy += 5
    bf = sans(11)
    for b in hero["bullets"]:
        dr.text((hx0, hy), "▪", font=bf, fill=RED)
        hy = draw_wrapped(dr, hx0 + 14, hy, b, bf, hx1 - hx0 - 14,
                          fill=INK, lh=13)
    hero_bottom = hy

    # ---- leads (right column) ------------------------------------------
    lx0, lx1 = 676, rx
    ly = 172
    for lead, scene in zip(d["leads"], (draw_tower_scene, draw_breach_scene)):
        box_h = 128
        dr.rectangle([lx0, ly, lx1, ly + box_h], fill=PAPER2,
                     outline=LINE, width=1)
        scene(dr, lx0 + 1, ly + 1, lx1 - lx0 - 2, 34)
        ty = ly + 40
        dr.text((lx0 + 8, ty), lead["kicker"], font=sans_b(10), fill=RED)
        ty += 14
        ty = draw_wrapped(dr, lx0 + 8, ty, lead["headline"], serif_b(15),
                          lx1 - lx0 - 16, fill=NAVY, lh=17)
        ty += 2
        ty = draw_wrapped(dr, lx0 + 8, ty, lead["deck"], serif(11),
                          lx1 - lx0 - 16, fill=INK, lh=12)
        dr.text((lx0 + 8, ly + box_h - 12),
                "Source: " + lead["source"], font=sans_i(9), fill=GREY)
        ly += box_h + 8
    leads_bottom = ly - 8
    rule(dr, mx, max(hero_bottom, leads_bottom) + 6, rx, fill=LINE, w=1)

    # ---- medium cards ---------------------------------------------------
    my = max(hero_bottom, leads_bottom) + 14
    cw = (rx - mx - 3 * 10) // 4
    for i, card in enumerate(d["medium"]):
        x0 = mx + i * (cw + 10)
        pin(dr, x0 + 10, my + 10, card["pin"], r=9)
        dr.text((x0 + 26, my + 2), card["kicker"], font=sans_b(10),
                fill=REGION_FILL.get("WORLD", GREY))
        y = draw_wrapped(dr, x0, my + 22, card["headline"], serif_b(14),
                         cw, fill=NAVY, lh=17)
        y += 3
        deck_lines = wrap(dr, card["deck"], serif(10), cw)[:1]
        for ln in deck_lines:
            dr.text((x0, y), trunc(dr, ln, serif(10), cw), font=serif(10),
                    fill=INK)
            y += 13
        dr.text((x0, my + 92), "Source: " + card["source"],
                font=sans_i(9), fill=GREY)
    med_bottom = my + 104
    rule(dr, mx, med_bottom + 4, rx, fill=LINE, w=1)

    # ---- six moments timeline -------------------------------------------
    ty = med_bottom + 10
    dr.text((mx, ty), "SIX MOMENTS THAT MADE THE DAY", font=sans_b(12),
            fill=NAVY)
    ty += 16
    mw = (rx - mx - 5 * 10) // 6
    for i, m in enumerate(d["moments"]):
        x0 = mx + i * (mw + 10)
        dr.text((x0, ty), m["part"], font=sans_b(11), fill=RED)
        draw_wrapped(dr, x0, ty + 15, m["text"], sans(10), mw, fill=INK,
                     lh=13)
        if i < 5:
            dr.line([(x0 + mw + 5, ty), (x0 + mw + 5, ty + 44)],
                    fill=LINE, width=1)
    tl_bottom = ty + 44
    rule(dr, mx, tl_bottom + 4, rx, fill=LINE, w=1)

    # ---- world map + pin legend -----------------------------------------
    my2 = tl_bottom + 8
    dr.text((mx, my2), "WHERE IT HAPPENED", font=sans_b(12), fill=NAVY)
    my2 += 14
    pins = [(31.7, 1.4, 1), (31.1, 3.8, 2), (35.3, 4.5, 3),
            (16.0, 3.2, 4), (18.0, 2.2, 5), (29.0, 2.6, 6),
            (47.7, 3.3, 7)]
    draw_map(dr, mx, my2, 9, pins)
    lx = 620
    legend = [
        (1, "Gulf of Finland — Kyiv's drone strike"),
        (2, "Benghazi — Russian warship sunk"),
        (3, "Riyadh — PIF Tower hit, 11 hurt"),
        (4, "Washington — CIA and ODNI breached"),
        (5, "New York — Huawei convicted"),
        (6, "Warsaw — NATO jets on the way"),
        (7, "Seoul — minister quits"),
    ]
    ly2 = my2 + 2
    for n, text in legend:
        pin(dr, lx + 10, ly2 + 7, n, r=7)
        dr.text((lx + 26, ly2), text, font=sans(11), fill=INK)
        ly2 += 15
    map_bottom = my2 + 110
    rule(dr, mx, map_bottom + 4, rx, fill=LINE, w=1)

    # ---- ALSO list --------------------------------------------------------
    ay = map_bottom + 8
    dr.text((mx, ay), "ALSO — IN BRIEF", font=sans_b(12), fill=NAVY)
    dr.text((rx - dr.textlength("EU Europe · ME Middle East · AP Asia-Pacific · AM Americas · AF Africa · WO World",
                                font=sans_i(10)), ay + 1),
            "EU Europe · ME Middle East · AP Asia-Pacific · AM Americas · AF Africa · WO World",
            font=sans_i(10), fill=GREY)
    ay += 18
    cols = [d["also"][i::3] for i in range(3)]
    col_w = (rx - mx - 2 * 16) // 3
    af = sans(9)
    REGION_CODE = {"EUROPE": "EU", "MIDDLE EAST": "ME", "ASIA-PACIFIC": "AP",
                   "AMERICAS": "AM", "AFRICA": "AF", "OCEANIA": "OC",
                   "WORLD": "WO"}
    for ci, col in enumerate(cols):
        x0 = mx + ci * (col_w + 16)
        y = ay
        for item in col:
            tag = REGION_CODE[item["region"]]
            tag_f = sans_b(8)
            tw = dr.textlength(tag, font=tag_f) + 8
            dr.rounded_rectangle([x0, y, x0 + tw, y + 12], radius=2,
                                 fill=REGION_FILL[item["region"]])
            dr.text((x0 + 4, y + 1), tag, font=tag_f, fill=WHITE)
            rest = f"{item['n']}. {item['headline']} · {item['source']}"
            dr.text((x0 + tw + 5, y + 1),
                    trunc(dr, rest, af, col_w - tw - 5), font=af, fill=INK)
            y += 15
    also_bottom = ay + 10 * 15
    rule(dr, mx, also_bottom + 4, rx, fill=LINE, w=1)

    # ---- date check + footer ----------------------------------------------
    fy = also_bottom + 8
    dr.rounded_rectangle([mx, fy, rx, fy + 28], radius=3, outline=RED,
                         width=1)
    dr.text((mx + 10, fy + 3), "DATE CHECK", font=sans_b(11), fill=RED)
    df = sans(10)
    dr.text((mx + 10, fy + 15), trunc(dr, d["date_check"]["note"], df,
                                       rx - mx - 20), font=df, fill=INK)
    fy += 34
    dr.text((mx, fy), trunc(dr, d["date_check"]["left_out"], sans_i(9),
                            rx - mx), font=sans_i(9), fill=GREY)
    fy += 15
    rule(dr, mx, fy, rx, fill=LINE, w=1)
    fy += 4
    dr.text((mx, fy),
            "Sources: Reuters · RFE/RL · WH News · BBC · BusinessWorld · "
            "Jagran Josh · Dell — all reporting crawled 25 November 2026.",
            font=sans(9), fill=GREY)
    dr.text((rx - dr.textlength("THE WEDNESDAY LEDGER · 25 NOV 2026",
                                font=sans_b(9)), fy),
            "THE WEDNESDAY LEDGER · 25 NOV 2026", font=sans_b(9), fill=NAVY)
    img.save(OUT, format="PNG", optimize=True)
    return fy + 12


def main():
    final_y = build()
    print(f"final content y={final_y} (canvas {H})")
    assert final_y <= H - 4, f"content overflows canvas: {final_y} > {H}"
    out = OUT
    data = open(out, "rb").read()
    assert len(data) <= 1048576, f"entry.png too big: {len(data)}"
    im = Image.open(out)
    assert im.size == (1024, 1024), f"wrong size: {im.size}"
    h1 = hashlib.sha256(data).hexdigest()
    build()
    data2 = open(out, "rb").read()
    h2 = hashlib.sha256(data2).hexdigest()
    assert h1 == h2, "non-deterministic render!"
    print(f"entry.png {len(data)} bytes sha256={h1}")


if __name__ == "__main__":
    main()
