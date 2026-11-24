#!/usr/bin/env python3
"""Draw the entry image for make.fun's news-image-20261123 bounty.

One 1024x1024 newspaper front page that sums up the world news of
Monday 23 November 2026 in six panels. Everything is drawn with PIL
primitives -- no photos, no network -- so the output bytes are stable.
Run:  python3 draw.py   (writes entry.png next to this file)
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = 1024
H = 1024

# --- palette -------------------------------------------------------------
PAPER = (248, 243, 230)
INK = (24, 22, 20)
FAINT = (96, 90, 80)
ACCENT = (168, 38, 26)        # headline red
RULE = (24, 22, 20)
PANEL_BG = (252, 249, 240)
SEA = (43, 103, 133)
SEA_DARK = (30, 76, 102)
SKY = (196, 219, 228)
SHIP = (66, 68, 72)
SMOKE = (120, 114, 104)
FIRE = (196, 74, 24)
FIRE2 = (232, 146, 44)
CHIP = (28, 104, 66)
GOLD = (176, 137, 84)
SAND = (214, 196, 152)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, fnt):
    box = draw.textbbox((0, 0), s, font=fnt)
    return box[2] - box[0]


def centered(draw, cx, y, s, fnt, fill=INK):
    draw.text((cx - text_w(draw, s, fnt) / 2, y), s, font=fnt, fill=fill)


def wrapped(draw, s, fnt, width):
    """Greedy word wrap against real font metrics."""
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if text_w(draw, trial, fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)


def kicker(draw, x, y, s, fill=ACCENT):
    draw.text((x, y), s, font=font(SANSB, 19), fill=fill)


def story_text(draw, x, y, w, headline, sub, hsize=27, ssize=18):
    """Headline (serif bold, wrapped) then a smaller sans sub-line block."""
    hf = font(SERIF, hsize)
    cy = y
    for line in wrapped(draw, headline, hf, w):
        draw.text((x, cy), line, font=hf, fill=INK)
        cy += int(hsize * 1.22)
    cy += 4
    sf = font(SANS, ssize)
    for line in wrapped(draw, sub, sf, w):
        draw.text((x, cy), line, font=sf, fill=FAINT)
        cy += int(ssize * 1.3)
    return cy


# --- canvas ---------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# faint border frame around the whole page
d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

# --- masthead --------------------------------------------------------------
centered(d, W // 2, 26, "THE WORLD IN ONE DAY", font(SERIF, 57))
d.line([24, 100, W - 24, 100], fill=ACCENT, width=5)
d.line([24, 110, W - 24, 110], fill=RULE, width=2)
centered(d, W // 2, 118, "MONDAY 23 NOVEMBER 2026", font(SANSB, 31))
d.text((24, 124), "ONE IMAGE", font=font(SANSB, 17), fill=FAINT)
right = "SIX STORIES"
d.text((W - 24 - text_w(d, right, font(SANSB, 17)), 124), right,
       font=font(SANSB, 17), fill=FAINT)
d.line([24, 156, W - 24, 156], fill=RULE, width=2)

# --- lead story: Ukraine sea drones sink a Russian corvette off Libya -----
LX, LY, LW, LH = 24, 168, 976, 332
panel(d, LX, LY, LW, LH)
kicker(d, LX + 18, LY + 14, "MEDITERRANEAN  ·  WAR IN UKRAINE")
d.text((LX + 18, LY + 42), "UKRAINE SEA DRONES SINK",
       font=font(SERIF, 37), fill=INK)
d.text((LX + 18, LY + 88), "RUSSIAN WARSHIP OFF LIBYA",
       font=font(SERIF, 37), fill=INK)

# sea scene: sky band, then water
SX0, SY0, SX1, SY1 = LX + 18, LY + 148, LX + LW - 18, LY + 262
d.rectangle([SX0, SY0, SX1, SY0 + 34], fill=SKY)
d.rectangle([SX0, SY0 + 34, SX1, SY1], fill=SEA)
d.line([SX0, SY0 + 34, SX1, SY0 + 34], fill=SEA_DARK, width=2)
horizon = SY0 + 34

# distant Libyan coast: a low sand bump along the horizon
d.polygon([(SX0 + 600, horizon), (SX0 + 740, horizon - 8),
           (SX0 + 900, horizon), (SX1, horizon)], fill=SAND)

# the corvette: hull, deck works, mast
HX0, HX1, HY = SX0 + 300, SX0 + 700, horizon + 26
d.polygon([(HX0, HY), (HX1, HY), (HX1 - 26, HY + 22), (HX0 + 18, HY + 22)],
          fill=SHIP)
d.rectangle([HX0 + 120, HY - 26, HX0 + 300, HY], fill=SHIP)
d.rectangle([HX0 + 150, HY - 44, HX0 + 235, HY - 26], fill=SHIP)
d.line([HX0 + 330, HY, HX0 + 330, HY - 58], fill=SHIP, width=5)
d.line([HX0 + 330, HY - 58, HX0 + 292, HY - 30], fill=SHIP, width=3)
d.line([HX0 + 330, HY - 58, HX0 + 372, HY - 34], fill=SHIP, width=3)
d.rectangle([HX0 + 40, HY - 14, HX0 + 96, HY], fill=SHIP)  # forward gun house

# hit at the stern: flash star + smoke column
FX, FY = HX1 - 34, HY - 6
d.polygon([(FX, FY - 26), (FX + 7, FY - 8), (FX + 24, FY - 12),
           (FX + 10, FY + 1), (FX + 16, FY + 16), (FX, FY + 6),
           (FX - 15, FY + 15), (FX - 9, FY), (FX - 23, FY - 10),
           (FX - 6, FY - 8)], fill=FIRE2, outline=FIRE)
for i, (dx, dy, r) in enumerate([(0, -26, 12), (8, -44, 15), (18, -62, 18)]):
    d.ellipse([FX + dx - r, FY + dy - r, FX + dx + r, FY + dy + r],
              fill=SMOKE if i else (150, 143, 132))

# three sea drones closing in from the left, wakes behind them
for j, (dx, dy) in enumerate([(30, 62), (96, 84), (168, 58)]):
    bx, by = SX0 + dx, SY0 + dy
    d.polygon([(bx, by), (bx + 44, by + 5), (bx + 38, by + 13), (bx + 4, by + 11)],
              fill=(30, 30, 34))
    d.line([bx - 30, by + 12, bx, by + 8], fill=(235, 242, 244), width=3)
    d.line([bx - 22, by + 17, bx + 2, by + 12], fill=(235, 242, 244), width=2)

# wave ticks on the water
for wx in range(SX0 + 24, SX1 - 30, 64):
    for wy in (SY1 - 26, SY1 - 10):
        d.arc([wx, wy, wx + 26, wy + 12], start=180, end=330,
              fill=(214, 232, 238), width=2)

capf = font(SERIF, 19)
cap = ("Zelenskyy confirms: seven maritime drones sank a Russian navy "
       "corvette at a base in Libya")
for n, line in enumerate(wrapped(d, cap, capf, LW - 36)[:2]):
    d.text((LX + 18, LY + 274 + n * 25), line, font=capf, fill=INK)

# --- row two, left: COP31 climate talks end without a deal -----------------
AX, AY, AW, AH = 24, 514, 480, 242
panel(d, AX, AY, AW, AH)
kicker(d, AX + 18, AY + 14, "ANTALYA, TÜRKİYE  ·  CLIMATE")
story_text(d, AX + 18, AY + 42, AW - 36,
           "COP31 CLIMATE TALKS END WITHOUT A DEAL",
           "Record-long UN summit splits over phasing out fossil fuels "
           "and climate finance")
# icon strip: factory chimneys, smoke, a hard sun
GY = AY + AH - 14
d.line([AX + 18, GY, AX + AW - 18, GY], fill=INK, width=2)
for i, cx in enumerate((AX + 52, AX + 96)):
    d.rectangle([cx, GY - 52, cx + 20, GY], fill=SHIP)
    d.ellipse([cx + 3, GY - 71, cx + 17, GY - 57], outline=SMOKE, width=3)
sunx, suny = AX + AW - 74, GY - 46
d.ellipse([sunx - 17, suny - 17, sunx + 17, suny + 17], fill=FIRE2)
for a in range(0, 360, 45):
    import math
    x2 = sunx + int(30 * math.cos(math.radians(a)))
    y2 = suny + int(30 * math.sin(math.radians(a)))
    x1 = sunx + int(22 * math.cos(math.radians(a)))
    y1 = suny + int(22 * math.sin(math.radians(a)))
    d.line([x1, y1, x2, y2], fill=FIRE, width=3)
d.text((AX + 150, GY - 40), "NO DEAL", font=font(SANSB, 24), fill=ACCENT)

# --- row two, right: Hormuz shipping attacks spike --------------------------
BX, BY, BW, BH = 520, 514, 480, 242
panel(d, BX, BY, BW, BH)
kicker(d, BX + 18, BY + 14, "STRAIT OF HORMUZ  ·  MIDDLE EAST")
story_text(d, BX + 18, BY + 42, BW - 36,
           "SHIPPING ATTACKS HIT WAR'S HIGHEST LEVEL",
           "Seven tankers hit in a week; Iran vows to face the US "
           "blockade with \u201call its tools\u201d")
# icon strip: an oil tanker riding low on wave lines
TY = BY + BH - 40
d.polygon([(BX + 40, TY), (BX + 300, TY), (BX + 282, TY + 18),
           (BX + 56, TY + 18)], fill=SHIP)
d.rectangle([BX + 66, TY - 12, BX + 236, TY], fill=(96, 99, 104))
d.rectangle([BX + 244, TY - 24, BX + 272, TY], fill=SHIP)
d.line([BX + 258, TY - 24, BX + 258, TY - 40], fill=SHIP, width=3)
for wx in range(BX + 30, BX + BW - 60, 46):
    d.arc([wx, TY + 22, wx + 30, TY + 34], start=180, end=330,
          fill=SEA, width=3)
d.text((BX + 330, TY - 26), "7 TANKERS\nHIT", font=font(SANSB, 20),
       fill=ACCENT)

# --- row three: three smaller stories --------------------------------------
RY, RH = 770, 198
cols = [(24, "WALL STREET  ·  TECH"),
        (354, "INDONESIA  ·  DISASTER"),
        (684, "SPACE  ·  SCIENCE")]
stories3 = [
    ("NVIDIA RESTORES JENSEN HUANG AS CEO",
     "S&P 500 leaps about 5%, winning back half of last week's plunge"),
    ("CANDY FACTORY FIRE KILLS AT LEAST 24",
     "Rescuers hunt for 34 workers missing after the blaze tore "
     "through the plant"),
    ("BEPICOLOMBO AT MERCURY AFTER 8 YEARS",
     "European\u2013Japanese craft enters orbit at the "
     "innermost planet"),
]
for (cx, kick), (head, sub) in zip(cols, stories3):
    panel(d, cx, RY, 316, RH)
    kicker(d, cx + 16, RY + 12, kick)
    story_text(d, cx + 16, RY + 38, 316 - 32, head, sub, hsize=22, ssize=15)

# row-three icons, one per panel along the bottom edge
# Nvidia: a rising market arrow
AX0, AY0 = 40, RY + RH - 34
d.line([AX0, AY0 + 16, AX0 + 60, AY0 + 8, AX0 + 110, AY0 + 12,
        AX0 + 168, AY0 - 8], fill=CHIP, width=4)
d.polygon([(AX0 + 168, AY0 - 16), (AX0 + 170, AY0 + 2), (AX0 + 154, AY0 - 4)],
          fill=CHIP)
# Indonesia: two quiet flames above a factory roofline
FX0, FY0 = 354 + 120, RY + RH - 12
d.line([FX0 - 70, FY0, FX0 + 90, FY0], fill=INK, width=3)
for fx, fh in ((FX0 - 20, 26), (FX0 + 22, 34)):
    d.polygon([(fx - 10, FY0), (fx, FY0 - fh), (fx + 10, FY0)], fill=FIRE)
    d.polygon([(fx - 5, FY0), (fx, FY0 - fh // 2), (fx + 5, FY0)], fill=FIRE2)
# BepiColombo: Mercury, an orbit ring, the little craft on it
MX, MY = 684 + 242, RY + RH - 27
d.arc([MX - 52, MY - 24, MX + 52, MY + 24], start=200, end=140, fill=FAINT,
      width=2)
d.ellipse([MX - 16, MY - 16, MX + 16, MY + 16], fill=GOLD, outline=INK, width=2)
d.rectangle([MX + 38, MY - 20, MX + 47, MY - 11], fill=INK)
d.line([MX + 42, MY - 15, MX + 52, MY - 24], fill=INK, width=2)

# --- footer ------------------------------------------------------------------
d.line([24, 980, W - 24, 980], fill=RULE, width=2)
centered(d, W // 2, 988,
         "SIX STORIES OF MONDAY 23 NOVEMBER 2026  ·  FROM THE DAY'S "
         "WIRE REPORTS (AP · REUTERS · BBC)",
         font(SANS, 16), fill=FAINT)

img.save(OUT)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
