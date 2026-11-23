#!/usr/bin/env python3
"""Draw THE WORLD TODAY - Monday, 23 November 2026 - as a 1024x1024
newspaper front page summing up the day's world news. Pure stdlib + Pillow.
Deterministic: no randomness, no timestamps, no network. Run: python3 main.py
Writes entry.png (1024x1024) next to this file, or to $MAKEFUN_OUTPUT_DIR.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (158, 27, 27)
BLUE = (24, 64, 110)
GREY = (90, 86, 78)
SEA = (46, 110, 138)
ORANGE = (214, 106, 24)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(d, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 5
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(d, x, y, text, size, width, fill=INK):
    f = font(SERIF, size)
    return para(d, x, y, text, f, width, fill=fill, leading=size + 4)


def kicker(d, x, y, text, fill=RED):
    f = font(SANS_B, 17)
    d.text((x, y), text, font=f, fill=fill)
    return y + 24


def rule(d, x0, y, x1, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def draw_ship(d, x, y, w, h):
    """Cargo ship on waves with a smoke plume."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 236))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=SEA)
    for i in range(5):
        wx = x + 8 + i * 52
        d.arc([wx, y + h - 12, wx + 44, y + h - 2], 180, 360, fill=(255, 255, 255), width=3)
    d.polygon([(x + 18, y + h - 34), (x + w - 18, y + h - 34),
               (x + w - 42, y + h - 14), (x + 42, y + h - 14)], fill=(60, 60, 66))
    for i, cx in enumerate(range(x + 52, x + w - 92, 46)):
        d.rectangle([cx, y + h - 56, cx + 40, y + h - 34],
                    fill=[(214, 106, 24), (46, 110, 138), (90, 120, 60)][i % 3])
    d.rectangle([x + w - 86, y + h - 58, x + w - 46, y + h - 34], fill=(235, 235, 228))
    d.rectangle([x + w - 82, y + h - 54, x + w - 50, y + h - 46], fill=(24, 64, 110))
    sx = x + w // 2 - 60
    for i, r in enumerate([10, 13, 16, 13, 10]):
        d.ellipse([sx + i * 10, y + 2 + i * 4, sx + i * 10 + r * 2, y + 2 + i * 4 + r * 2],
                  fill=(120, 118, 112))
    d.text((x + 10, y + 4), "SPARTA II",
           font=font(SANS_B, 13), fill=INK)


def draw_building(d, x, y, w, h):
    """Five-storey block, one corner collapsed, rescue ladder."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    bx, by, bw, bh = x + 60, y + 4, 150, h - 8
    d.rectangle([bx, by, bx + bw, by + bh], fill=(168, 158, 140))
    for r in range(5):
        for c in range(4):
            wx = bx + 14 + c * 36
            wy = by + 4 + r * 10
            d.rectangle([wx, wy, wx + 22, wy + 7], fill=(250, 244, 220))
    d.polygon([(bx + bw, by + 20), (bx + bw + 52, by + 32), (bx + bw + 52, by + bh),
               (bx + bw, by + bh)], fill=(120, 112, 98))
    for i in range(6):
        d.rectangle([bx + bw + 6 + i * 8, by + bh - 12 - (i % 3) * 5,
                     bx + bw + 18 + i * 8, by + bh - 4 - (i % 3) * 5], fill=(96, 90, 78))
    d.line([(bx + 8, by + bh), (bx + 44, by + 6)], fill=RED, width=4)
    for i in range(5):
        t = i / 4.0
        lx = bx + 8 + (44 - 8) * t
        ly = by + bh - (bh - 6) * t
        d.line([(lx - 6, ly + 3), (lx + 6, ly - 3)], fill=RED, width=2)
    d.text((x + w - 168, y + 4), "DYMER  •  KYIV REGION",
           font=font(SANS_B, 13), fill=INK)


def draw_fire(d, x, y, w, h):
    """Factory with flames and smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 196))
    d.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 14], fill=(140, 130, 116))
    d.rectangle([x + 30, y + h - 46, x + w - 90, y + h - 34], fill=(112, 104, 92))
    for i in range(4):
        d.rectangle([x + 44 + i * 34, y + h - 28, x + 64 + i * 34, y + h - 18],
                    fill=(250, 244, 220))
    for fx, fh in [(x + 52, 22), (x + 96, 28), (x + 142, 22), (x + 186, 26)]:
        d.polygon([(fx, y + h - 34), (fx + 12, y + h - 34 - fh),
                   (fx + 24, y + h - 34)], fill=ORANGE)
        d.polygon([(fx + 6, y + h - 34), (fx + 12, y + h - 34 - fh + 10),
                   (fx + 18, y + h - 34)], fill=(240, 200, 60))
    for i, r in enumerate([9, 12, 15]):
        d.ellipse([x + w - 90 + i * 10, y + 2 + i * 6,
                   x + w - 90 + i * 10 + r * 2, y + 2 + i * 6 + r * 2],
                  fill=(110, 108, 102))
    d.text((x + 10, y + 4), "CIKANDE  •  BANTEN, JAVA",
           font=font(SANS_B, 13), fill=INK)


def draw_strait(d, x, y, w, h):
    """Strait of Hormuz: tanker, missile arcs, sun."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 232))
    d.ellipse([x + w - 66, y + 4, x + w - 18, y + 52], fill=(240, 200, 60))
    d.arc([x + 20, y + 2, x + 170, y + 90], 200, 340, fill=RED, width=4)
    d.arc([x + 60, y + 12, x + 210, y + 100], 200, 340, fill=RED, width=4)
    d.ellipse([x + 168, y + 30, x + 180, y + 42], fill=RED)
    d.ellipse([x + 208, y + 42, x + 220, y + 54], fill=RED)
    d.polygon([(x + 30, y + h - 26), (x + w - 30, y + h - 26),
               (x + w - 52, y + h - 12), (x + 52, y + h - 12)], fill=(40, 40, 44))
    d.rectangle([x + w - 96, y + h - 44, x + w - 52, y + h - 26], fill=(235, 235, 228))
    for i in range(5):
        d.arc([x + 14 + i * 52, y + h - 10, x + 58 + i * 52, y + h - 2],
              180, 360, fill=(255, 255, 255), width=3)
    d.text((x + 232, y + 4), "STRAIT OF HORMUZ",
           font=font(SANS_B, 13), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin
    rx = W - mx

    # --- masthead ---
    rule(d, mx, 14, rx, 3)
    title = "THE WORLD TODAY"
    tf = font(SERIF, 88)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title, font=tf, fill=INK)
    rule(d, mx, 128, rx, 2)
    tag = "MONDAY, 23 NOVEMBER 2026   •   WORLD NEWS IN ONE PAGE   •   PRICE: FREE"
    sf = font(SANS_B, 19)
    d.text(((W - d.textlength(tag, font=sf)) / 2, 138), tag, font=sf, fill=INK)
    rule(d, mx, 168, rx, 4)

    # --- lead: COP31 (dynamic y-cursor; nothing may pass y=430) ---
    y = 182
    y = kicker(d, mx, y, "CLIMATE  —  ANTALYA, TÜRKIYE")
    y = headline(d, mx, y + 2, "COP31 COLLAPSES:", 46, 600)
    y = headline(d, mx, y - 2, "NO CLIMATE PACT", 46, 600, fill=RED)
    y = para(d, mx, y + 6,
             "The longest UN climate summit ever ended on Sunday with no pact — the first "
             "collapse since Copenhagen in 2009. The draft never even named fossil fuels. "
             "The EU refused it.",
             font(SERIF_R, 22), 600, leading=27)
    print("lead ends y =", y)
    # lead illustration: globe with a crack, "NO DEAL" stamp top-right
    ix, iy, iw, ih = 668, 182, 320, 200
    d.rectangle([ix, iy, ix + iw, iy + ih], fill=(206, 224, 232))
    d.rectangle([ix, iy, ix + iw, iy + ih], outline=INK, width=2)
    cx, cy, r = ix + 120, iy + 105, 72
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=3)
    d.ellipse([cx - 46, cy - 42, cx + 4, cy + 2], fill=(46, 110, 60))
    d.ellipse([cx + 8, cy + 6, cx + 52, cy + 46], fill=(46, 110, 60))
    d.ellipse([cx - 18, cy - 54, cx + 26, cy - 26], fill=(46, 110, 60))
    d.line([(cx - 62, cy - 52), (cx - 18, cy - 8), (cx + 8, cy + 26),
            (cx + 36, cy + 58)], fill=INK, width=5)
    d.line([(cx - 18, cy - 8), (cx + 20, cy - 22)], fill=INK, width=4)
    d.rectangle([ix + 178, iy + 10, ix + 308, iy + 52], outline=RED, width=4)
    d.text((ix + 190, iy + 18), "NO DEAL", font=font(SANS_B, 26), fill=RED)
    d.text((ix + 10, iy + ih - 24), "THE ANTALYA PACT, REJECTED",
           font=font(SANS_B, 14), fill=INK)
    rule(d, mx, 430, rx, 2)

    # --- rows: kicker 20 + headline 2 lines + para 3 lines + picture 62 = 210 ---
    col_w = 464
    x2 = mx + col_w + 24

    def story(x, y0, kick, head, body, draw_fn):
        y = kicker(d, x, y0, kick)
        y = headline(d, x, y, head, 27, col_w)
        y = para(d, x, y + 4, body, font(SANS, 16), col_w, leading=20)
        draw_fn(d, x, y + 6, col_w, 62)
        return y + 6 + 62

    e1 = story(mx, 446, "BALTIC SEA  —  SHIP STILL SMOULDERING",
               "Burning Sparta II towed out of Finnish waters",
               "Drones set the Russian cargo ship ablaze on Saturday; a rescue vessel is "
               "now towing her out of Finnish waters. All 16 crew were evacuated, one hurt.",
               draw_ship)
    e2 = story(x2, 446, "UKRAINE  —  DYMER, KYIV REGION",
               "Drone flattens flats: 14 missing in the rubble",
               "A Russian drone collapsed part of a five-storey block north of Kyiv. Nine "
               "were pulled out; the search halted under a new air raid warning.",
               draw_building)
    print("row2 ends:", e1, e2)
    rule(d, mx, 668, rx, 2)

    e3 = story(mx, 684, "INDONESIA  —  CANDY FACTORY FIRE",
               "24 body bags after Java factory blaze",
               "Fire tore through the PT Fonusa Agung Mulia plant in Cikande on Saturday. "
               "About 30 workers are unaccounted for; DNA tests may take weeks to name "
               "the dead.", draw_fire)
    e4 = story(x2, 684, "THE GULF  —  WAR AT SEA",
               "Iran hits US bases; tankers struck in Hormuz",
               "Tehran says it struck two US Patriot radars; Bahrain says a civilian plant "
               "burned and two were hurt. Two more tankers were hit in the strait.",
               draw_strait)
    print("row3 ends:", e3, e4)

    # --- bottom band: two columns of short items ---
    by = 906
    d.rectangle([mx, by, rx, 992], outline=INK, width=2)
    d.text((mx + 12, by + 7), "ALSO TODAY", font=font(SANS_B, 17), fill=RED)
    left_items = [
        "Lisbon: thousands march in rain over living costs.",
        "Delhi: Nepal PM Shah holds talks with PM Modi.",
        "Wellington: India post record 720/9 declared.",
    ]
    right_items = [
        "Seoul: S. Korea minister quits in AI cheating row.",
        "Kuala Lumpur: Malaysia to press UN over Myanmar.",
    ]
    yy = by + 30
    for it in left_items:
        d.text((mx + 12, yy), "•  " + it, font=font(SANS, 13), fill=INK)
        yy += 18
    yy = by + 30
    for it in right_items:
        d.text((mx + 488, yy), "•  " + it, font=font(SANS, 13), fill=INK)
        yy += 18
    foot = "Sources: UN News, Reuters, CNN, AFP, AP, Euronews, Xinhua  •  Drawn with Pillow — no photographs"
    ff = font(SANS, 12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1000), foot, font=ff, fill=GREY)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.png")
    img.save(path, "PNG")
    print("wrote", path)


if __name__ == "__main__":
    main()
