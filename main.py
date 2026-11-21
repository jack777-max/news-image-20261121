#!/usr/bin/env python3
"""The Global Ledger: one page summing up Saturday 21 November 2026.

The program paints a broadsheet front page of that day's world news and
writes it as a PNG named entry.png into the output directory (the
MAKEFUN_OUTPUT_DIR environment variable when set, else /output).
Everything on the page is fixed data in fixed positions, so two runs
write byte-identical files.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
LEFT = 44
RIGHT = PAGE - LEFT
WIDTH = RIGHT - LEFT

PAPER = (247, 241, 222)
INK = (26, 22, 17)
SOFT = (94, 86, 71)
ACCENT = (163, 22, 33)
BAND = (24, 26, 31)
SKY = (29, 35, 46)
SKYLINE = (13, 16, 22)
WINDOW_LIT = (250, 205, 105)
TRAIL = (255, 220, 150)
BURST = (240, 130, 40)

FONT_ROOT = "/usr/share/fonts/truetype/"


def pick_font(rel_paths, size):
    """First available font file wins; the bitmap default is the fallback."""
    for rel in rel_paths:
        candidate = os.path.join(FONT_ROOT, rel)
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def load_fonts():
    serif_bold = ["dejavu/DejaVuSerif-Bold.ttf"]
    serif = ["dejavu/DejaVuSerif.ttf"]
    serif_it = ["liberation/LiberationSerif-Italic.ttf",
                "dejavu/DejaVuSerif.ttf"]
    sans = ["dejavu/DejaVuSans.ttf"]
    sans_bold = ["dejavu/DejaVuSans-Bold.ttf"]
    return {
        "masthead": pick_font(serif_bold, 57),
        "micro": pick_font(sans, 12),
        "band": pick_font(sans_bold, 17),
        "kicker": pick_font(sans_bold, 14),
        "head": pick_font(serif_bold, 39),
        "deck": pick_font(serif_it, 17),
        "caption": pick_font(serif_it, 13),
        "sect": pick_font(sans_bold, 15),
        "feat_head": pick_font(serif_bold, 21),
        "feat_body": pick_font(serif, 15),
        "brief_place": pick_font(sans_bold, 13),
        "brief": pick_font(serif, 15),
        "also": pick_font(serif, 14),
        "num": pick_font(serif_bold, 30),
        "num_lab": pick_font(serif, 12),
        "foot": pick_font(serif, 12),
    }


# ---------------------------------------------------------------- the news

LEAD_KICKER = "UKRAINE - THE WAR"
LEAD_HEADLINE = "Russian Missile Strikes President Zelensky's Home Town"
LEAD_DECK = (
    "A ballistic missile tore into the centre of Kryvyi Rih, killing two "
    "people and wounding 60, in an overnight barrage of 3 missiles and 148 "
    "drones; Kyiv said 117 of the drones were shot down."
)
LEAD_CAPTION = "Kryvyi Rih, the president's home town, hit in the early hours of Saturday."

FEATURES = [
    {
        "kicker": "MARKETS",
        "headline": "AI Sell-Off Rattles Markets Worldwide",
        "body": (
            "Doubts that huge AI spending will pay off sent the S&P 500 down "
            "3.7% and Tokyo's Nikkei 5.1%. The FTSE fell 1.0%; Brent crude "
            "held near $89.95."
        ),
    },
    {
        "kicker": "THE HAGUE",
        "headline": "Myanmar Responsible for Genocide, Court Rules",
        "body": (
            "The UN's highest court found Myanmar responsible for "
            "genocide against the Rohingya, a landmark ruling on the "
            "2017 crackdown."
        ),
    },
]

BRIEFS = [
    ("MEXICO", "Mexican soldiers captured cartel boss Fausto Isidro "
     "Meza Flores, 'El Chapo Isidro', in Sinaloa."),
    ("ANTALYA", "COP31 climate talks ran into overtime, deadlocked "
     "over fossil fuels; the EU wants a good deal or none."),
    ("PERU", "A magnitude 6.9 earthquake shook the Andes; no "
     "casualties were reported in the first hours."),
    ("BASRA", "A fire at the Hartha power station in southern Iraq "
     "killed at least four people and injured 30, officials said."),
    ("FRANCE", "82,500 marched nationwide over living costs and "
     "student rights, in a lower, peaceful turnout."),
    ("DENMARK", "Copenhagen accused Russia of plotting to kill a "
     "US-Ukrainian citizen and expelled a Russian diplomat."),
    ("GENEVA", "Nations agreed to elaborate rules for AI-run "
     "autonomous weapons by 2028; a binding treaty is out of reach."),
    ("SAUDI ARABIA", "Houthi missiles were launched at the kingdom; "
     "Saudi defences intercepted those aimed at Riyadh."),
]

ALSO_TODAY = (
    "BepiColombo reaches Mercury orbit after eight years  -  England "
    "rout New Zealand 37-12  -  Bolsonaro in intensive care"
)


# ---------------------------------------------------------------- helpers

def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, x0, x1, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((x0 + (x1 - x0 - w) / 2, y), text, font=fnt, fill=fill)


def hairline(draw, y, x0=LEFT, x1=RIGHT, fill=INK, thick=1):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)


# ---------------------------------------------------------------- sections

def page_frame(draw):
    draw.rectangle([14, 14, PAGE - 14, PAGE - 14], outline=INK, width=3)
    draw.rectangle([21, 21, PAGE - 21, PAGE - 21], outline=INK, width=1)


def masthead(draw, fonts):
    draw.text((LEFT, 30), "ONE PAGE - ONE DAY - THE WHOLE WORLD",
              font=fonts["micro"], fill=SOFT)
    tag = "LATE EDITION"
    draw.text((RIGHT - draw.textlength(tag, font=fonts["micro"]), 30),
              tag, font=fonts["micro"], fill=SOFT)
    hairline(draw, 52)
    centred(draw, 0, PAGE, 60, "The Global Ledger", fonts["masthead"], INK)
    hairline(draw, 132, thick=3)
    hairline(draw, 138)
    draw.rectangle([LEFT, 148, RIGHT, 182], fill=BAND)
    centred(draw, LEFT, RIGHT, 156,
            "SATURDAY, 21 NOVEMBER 2026 - THE WORLD IN ONE PAGE",
            fonts["band"], PAPER)
    return 196


def night_illustration(draw, y):
    """A drawn night skyline under a missile trail, for the lead story."""
    bottom = y + 70
    draw.rectangle([LEFT, y, RIGHT, bottom], fill=SKY)
    # skyline: fixed building widths and heights along the panel floor
    buildings = [(0, 30), (52, 46), (118, 24), (168, 55), (238, 34),
                 (300, 62), (372, 28), (430, 48), (502, 36), (566, 58),
                 (640, 26), (700, 44), (772, 33), (838, 52), (900, 30)]
    for offset, height in buildings:
        bx = LEFT + offset
        draw.rectangle([bx, bottom - height, bx + 44, bottom], fill=SKYLINE)
        for row in range(3):
            for col in range(3):
                if (offset + row * 5 + col * 11) % 4 == 0:
                    wx = bx + 6 + col * 13
                    wy = bottom - height + 6 + row * 13
                    if wy < bottom - 6:
                        draw.rectangle([wx, wy, wx + 5, wy + 7],
                                       fill=WINDOW_LIT)
    # missile trail arcing in from the top right, burst above the rooftops
    tip = (LEFT + 620, y + 34)
    for shift in (-3, 0, 3):
        draw.line([RIGHT - 26 + shift, y + 4, tip[0] + shift, tip[1]],
                  fill=TRAIL, width=2)
    cx, cy = tip
    points = []
    for i in range(16):
        angle = math.pi * i / 8
        radius = 17 if i % 2 == 0 else 6
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(points, fill=BURST)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 240, 200))
    return bottom


def lead_story(draw, fonts, y):
    draw.text((LEFT, y), LEAD_KICKER, font=fonts["kicker"], fill=ACCENT)
    y += 22
    for line in wrap(draw, LEAD_HEADLINE, fonts["head"], WIDTH):
        draw.text((LEFT, y), line, font=fonts["head"], fill=INK)
        y += 48
    y += 2
    for line in wrap(draw, LEAD_DECK, fonts["deck"], WIDTH):
        draw.text((LEFT, y), line, font=fonts["deck"], fill=INK)
        y += 23
    y += 8
    y = night_illustration(draw, y)
    y += 6
    draw.text((LEFT, y), LEAD_CAPTION, font=fonts["caption"], fill=SOFT)
    return y + 24


def feature_pair(draw, fonts, y):
    gap = 20
    box_w = (WIDTH - gap) // 2
    box_h = 160
    for i, feat in enumerate(FEATURES):
        x0 = LEFT + i * (box_w + gap)
        x1 = x0 + box_w
        draw.rectangle([x0, y, x1, y + box_h], outline=INK, width=1)
        draw.rectangle([x0, y, x1, y + 4], fill=ACCENT)
        tx = x0 + 14
        ty = y + 13
        draw.text((tx, ty), feat["kicker"], font=fonts["kicker"],
                  fill=ACCENT)
        ty += 21
        for line in wrap(draw, feat["headline"], fonts["feat_head"],
                         box_w - 28):
            draw.text((tx, ty), line, font=fonts["feat_head"], fill=INK)
            ty += 26
        ty += 2
        for line in wrap(draw, feat["body"], fonts["feat_body"],
                         box_w - 28):
            draw.text((tx, ty), line, font=fonts["feat_body"], fill=INK)
            ty += 20
    return y + box_h


def draw_brief(draw, fonts, y, place, text):
    label = place + "  "
    label_w = draw.textlength(label, font=fonts["brief_place"])
    words = text.split()
    lines, current, avail = [], "", WIDTH - label_w
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fonts["brief"]) <= avail or not current:
            current = trial
        else:
            lines.append(current)
            current = word
            avail = WIDTH
    if current:
        lines.append(current)
    draw.text((LEFT, y + 2), label, font=fonts["brief_place"], fill=ACCENT)
    draw.text((LEFT + label_w, y), lines[0], font=fonts["brief"], fill=INK)
    yy = y + 20
    for line in lines[1:]:
        draw.text((LEFT, yy), line, font=fonts["brief"], fill=INK)
        yy += 20
    return yy


def wire_briefs(draw, fonts, y):
    draw.text((LEFT, y), "ON THE WIRE", font=fonts["sect"], fill=INK)
    hairline(draw, y + 22)
    y += 30
    for place, text in BRIEFS:
        y = draw_brief(draw, fonts, y, place, text)
        y += 5
    return y


def also_today(draw, fonts, y):
    hairline(draw, y, thick=2)
    y += 11
    tag = "ALSO TODAY:  "
    line = wrap(draw, ALSO_TODAY, fonts["also"], WIDTH)[0]
    tag_w = draw.textlength(tag, font=fonts["sect"])
    line_w = draw.textlength(line, font=fonts["also"])
    x = LEFT + (WIDTH - tag_w - line_w) / 2
    draw.text((x, y - 2), tag, font=fonts["sect"], fill=ACCENT)
    draw.text((x + tag_w, y), line, font=fonts["also"], fill=INK)
    return y + 20


def footer(draw, fonts):
    hairline(draw, 946)
    centred(draw, LEFT, RIGHT, 954,
            "Compiled from wire reports - Saturday 21 November 2026",
            fonts["foot"], SOFT)


def main():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()
    page_frame(draw)
    y = masthead(draw, fonts)
    y = lead_story(draw, fonts, y)
    hairline(draw, y)
    y = feature_pair(draw, fonts, y + 8)
    y = wire_briefs(draw, fonts, y + 14)
    y = also_today(draw, fonts, y + 10)
    footer(draw, fonts)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
