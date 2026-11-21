#!/usr/bin/env python3
"""make.fun bounty: Sum up 21 November's world news in one image.

Writes one deterministic 1024x1024 PNG to /output/entry.png (or the path in
the OUTPUT env var when run locally). No network; the picture is drawn with
Pillow from the day's public reporting: the missile strike on Kryvyi Rih,
the global AI sell-off, the ICJ genocide ruling on Myanmar, COP31 in
overtime, the capture of El Chapo Isidro and nine briefs. Same input ->
same bytes on every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARK = (24, 32, 48)
GREY = (90, 86, 78)
LINE = (200, 192, 176)
GOLD = (255, 214, 90)
PALE = (235, 235, 235)


def font(kind, size, bold=False):
    if kind == "serif":
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif"
        path += "-Bold.ttf" if bold else "-Regular.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans"
        path += "-Bold.ttf" if bold else ".ttf"
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def para(draw, x, y, max_w, text, fnt, fill=INK, lh=None):
    lh = lh or (fnt.size + 4)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def head(draw, x, y, max_w, text, size, fill=INK, lh=None):
    fnt = font("serif", size, bold=True)
    lh = lh or (size + 2)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x, y, w, fill=INK, h=2):
    draw.rectangle([x, y, x + w, y + h], fill=fill)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 34
CW = W - 2 * M

# ---- masthead ----
tag = "14 STORIES  •  ONE PAGE"
f_lab = font("sans", 20, True)
d.text((M, 20), "SATURDAY 21 NOVEMBER 2026", font=f_lab, fill=RED)
d.text((W - M - d.textlength(tag, font=f_lab), 20), tag, font=f_lab, fill=GREY)
y = head(d, M, 44, CW, "THE WORLD IN ONE DAY", 66, lh=68)
rule(d, M, y + 4, CW, h=4)
rule(d, M, y + 12, CW, fill=RED, h=2)
y += 22

# ---- lead row: Kryvyi Rih (wide left) + AI sell-off (right) ----
col_w, gap = 600, 24
side_w = CW - col_w - gap
x_side = M + col_w + gap
top = y
y = head(d, M, top, col_w, "MISSILE HITS ZELENSKY'S HOMETOWN", 36, lh=38)
y = para(d, M, y + 4, col_w,
         "Kryvyi Rih — A Russian ballistic missile strikes the centre of "
         "the president's hometown, killing two people and wounding 60, "
         "Kyiv says, in an overnight barrage of 3 missiles and 148 "
         "drones, 117 of them shot down.",
         font("sans", 17), lh=22)
lead_end = y
ys = head(d, x_side, top, side_w, "AI SELL-OFF ROCKS MARKETS", 27, lh=29, fill=RED)
ys = para(d, x_side, ys + 4, side_w,
          "Fears that AI spending will not pay off spark a broad rout: "
          "the S&P 500 falls 3.7% and Tokyo's Nikkei 5.1%.",
          font("sans", 16), lh=21)
y = max(lead_end, ys) + 8
rule(d, M, y, CW, fill=LINE, h=2)
y += 10

# ---- second row: ICJ ruling (left) + COP31 (right), equal columns ----
half = (CW - gap) // 2
x_r = M + half + gap
top = y
yl = head(d, M, top, half, "UN COURT: MYANMAR COMMITTED GENOCIDE", 26, lh=28)
yl = para(d, M, yl + 4, half,
          "The Hague — The International Court of Justice finds Myanmar "
          "responsible for genocide against the Rohingya, a landmark "
          "ruling delivered on Saturday.",
          font("sans", 16), lh=21)
yr = head(d, x_r, top, half, "COP31 DEADLOCKED IN OVERTIME", 26, lh=28, fill=RED)
yr = para(d, x_r, yr + 4, half,
          "Antalya — The climate summit runs deep into overtime, split "
          "over fossil fuels; the EU warns of a good deal or no deal "
          "at all.",
          font("sans", 16), lh=21)
y = max(yl, yr) + 8
rule(d, M, y, CW, fill=LINE, h=2)
y += 10

# ---- banner: Mexico cartel capture ----
bh = 58
d.rectangle([M, y, W - M, y + bh], fill=DARK)
d.text((M + 16, y + 6), "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO'",
       font=font("sans", 26, True), fill=GOLD)
d.text((M + 16, y + 36),
       "Soldiers seize Fausto Isidro Meza Flores, an FBI most-wanted, in Guasave, Sinaloa",
       font=font("sans", 16), fill=PALE)
y += bh + 10
rule(d, M, y, CW, fill=LINE, h=2)
y += 8

# ---- markets strip ----
y = head(d, M, y, CW, "S&P 500 -3.7%  •  NIKKEI -5.1%  •  FTSE -1.0%  •  BRENT $89.95",
         22, lh=24, fill=RED)
y = para(d, M, y + 2, CW,
         "Brent crude edges up 0.6% and natural gas 1.8% even as the AI "
         "rout slides across three continents; the EU and Indonesia sign "
         "a trade deal after 10 years of talks.",
         font("sans", 16), lh=21)
y += 6
rule(d, M, y, CW, fill=LINE, h=2)
y += 8

# ---- briefs grid: 2 columns x 4 rows ----
briefs = [
    ("PERU EARTHQUAKE",
     "A magnitude 6.9 quake shakes the Andes; no damage or casualties immediately reported."),
    ("SAUDI INTERCEPTS",
     "Air defences down three Houthi ballistic missiles aimed at Riyadh, others at Jazan."),
    ("KILLER-ROBOT RULES",
     "Nations in Geneva agree to elaborate rules for AI-run autonomous weapons by 2028."),
    ("MERCURY ORBIT",
     "Europe and Japan's BepiColombo reaches Mercury's orbit after an eight-year journey."),
    ("DENGUE BREAKTHROUGH",
     "Mosquitoes carrying a bacterium cut dengue cases by 69% in Brazil, researchers report."),
    ("DENMARK PLOT CHARGE",
     "Copenhagen accuses Russia of plotting to kill a US-Ukrainian citizen; a diplomat is expelled."),
    ("FRANCE MARCHES",
     "Some 82,500 people march across France over living costs and student rights."),
    ("ENGLAND ROUT ALL BLACKS",
     "A record 37-12 win over New Zealand at Twickenham keeps England's final hopes alive."),
]
bw = (CW - 24) // 2
cols_x = [M, M + bw + 24]
grid_top = y
for i, (h, t) in enumerate(briefs):
    bx = cols_x[i % 2]
    by = grid_top + (i // 2) * 84
    d.text((bx, by), h, font=font("sans", 18, True), fill=RED)
    para(d, bx, by + 23, bw, t, font("sans", 16), lh=20)

# ---- footer ----
fy = H - 40
rule(d, M, fy - 8, CW, fill=LINE, h=2)
d.text((M, fy),
       "Compiled from public reporting of Saturday 21 November 2026  •  make.fun news-image-20261121",
       font=font("sans", 15), fill=GREY)

out = os.environ.get("OUTPUT", "/output/entry.png")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
