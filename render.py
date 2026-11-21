#!/usr/bin/env python3
"""Draw a one-page brief of Saturday 21 November 2026 world news.

Pillow is used only while building the image. main.py copies the bytes.
Facts are limited to what wire and public-service reports dated that day.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "news.png"
W = H = 1024

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

INK = (22, 20, 18)
PAPER = (244, 238, 226)
NAVY = (16, 28, 43)
WHITE = (255, 252, 247)
RED = (163, 38, 32)
MUTED = (84, 74, 62)
GOLD = (232, 196, 154)

LEADS = [
    {
        "kicker": "MIDDLE EAST  ·  SHIPPING",
        "color": (163, 38, 32),
        "title": "Two tankers hit off the Strait of Hormuz",
        "deck": "UKMTO: projectiles hit two ships near Khasab, Oman. No casualties. Iran says a tanker struck a mine.",
        "source": "UKMTO  ·  Reuters",
        "icon": "ship",
    },
    {
        "kicker": "CLIMATE  ·  ANTALYA",
        "color": (22, 102, 78),
        "title": "COP31 still deadlocked, with no deal",
        "deck": "Saturday talks, still no text. Fossil-fuel lines and a $120bn adaptation goal African states want back remain open. The US is absent.",
        "source": "Reuters  ·  BBC",
        "icon": "climate",
    },
    {
        "kicker": "EUROPE  ·  WAR",
        "color": (28, 54, 102),
        "title": "Zelensky: bridge strikes a “fair response”",
        "deck": "He said so in Kyiv, meeting Britain’s defence secretary. Finland: a drone damaged a Russian cargo ship in the Gulf of Finland.",
        "source": "BBC",
        "icon": "bridge",
    },
    {
        "kicker": "GAZA  ·  CONFLICT",
        "color": (122, 64, 28),
        "title": "Strike on a food van killed three",
        "deck": "Shifa Hospital said an Israeli strike hit a food van in Tel al-Hawa. The military said it targeted militants.",
        "source": "AP  ·  AFP",
        "icon": "van",
    },
]

BRIEFS = [
    {
        "label": "PERU",
        "color": (36, 78, 120),
        "text": "M6.7 in Junín, late Friday locally (00:09 UTC Sat). Eight injured.",
        "source": "Indeci",
    },
    {
        "label": "BASRA",
        "color": (163, 38, 32),
        "text": "Al-Hartha blast: people killed, dozens hurt; inquiry ordered.",
        "source": "INA",
    },
    {
        "label": "GENEVA",
        "color": (28, 54, 102),
        "text": "Two years to draft autonomous-weapon rules. No binding ban.",
        "source": "AFP",
    },
    {
        "label": "PACIFIC",
        "color": (22, 102, 78),
        "text": "Magnitude 6.8 quake, Banda Sea, 226 km northeast of Dili.",
        "source": "GFZ",
    },
    {
        "label": "MARKETS",
        "color": (92, 68, 22),
        "text": "Bitcoin near $55,000, a two-year low, then rebounded toward $60,000.",
        "source": "Reuters",
    },
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, face, width):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else f"{cur} {word}"
        if face.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_ship(d, box, color):
    x0, y0, x1, y1 = box
    mid = (y0 + y1) / 2

    def hull(cx, cy, scale):
        d.polygon(
            [
                (cx - 30 * scale, cy),
                (cx + 32 * scale, cy),
                (cx + 22 * scale, cy + 14 * scale),
                (cx - 22 * scale, cy + 14 * scale),
            ],
            fill=color,
        )
        d.rectangle(
            (cx - 6 * scale, cy - 16 * scale, cx + 4 * scale, cy),
            fill=color,
        )
        d.rectangle(
            (cx + 8 * scale, cy - 9 * scale, cx + 16 * scale, cy),
            fill=color,
        )

    hull((x0 + x1) / 2 - 8, mid - 6, 1.0)
    hull((x0 + x1) / 2 + 18, mid + 16, 0.72)


def draw_climate(d, box, color):
    """A thermometer: the climate story, not an abstract mark."""
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    top = y0 + 4
    bulb_b = y1 - 4
    d.rounded_rectangle((cx - 7, top, cx + 7, bulb_b - 16), radius=7, outline=color, width=3)
    d.ellipse((cx - 13, bulb_b - 28, cx + 13, bulb_b), outline=color, width=3)
    d.rectangle((cx - 3, top + 18, cx + 3, bulb_b - 16), fill=color)
    d.ellipse((cx - 8, bulb_b - 22, cx + 8, bulb_b - 6), fill=color)


def draw_bridge(d, box, color):
    """Two towers, cables, and a deck with a gap."""
    x0, y0, x1, y1 = box
    deck = y0 + 40
    mid = (x0 + x1) / 2
    d.rectangle((x0 + 12, y0 + 8, x0 + 20, deck + 10), fill=color)
    d.rectangle((x1 - 20, y0 + 8, x1 - 12, deck + 10), fill=color)
    d.line((x0 + 16, y0 + 12, mid - 12, deck), fill=color, width=3)
    d.line((x1 - 16, y0 + 12, mid + 12, deck), fill=color, width=3)
    d.rectangle((x0 + 6, deck, mid - 12, deck + 6), fill=color)
    d.rectangle((mid + 12, deck, x1 - 6, deck + 6), fill=color)
    d.arc((x0 + 8, deck + 12, x1 - 8, deck + 28), 200, 340, fill=color, width=2)


def draw_van(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 4
    d.rounded_rectangle((cx - 32, cy - 16, cx + 28, cy + 10), radius=3, outline=color, width=4)
    d.rectangle((cx + 8, cy - 16, cx + 28, cy - 2), outline=color, width=4)
    d.ellipse((cx - 24, cy + 6, cx - 12, cy + 18), outline=color, width=3)
    d.ellipse((cx + 10, cy + 6, cx + 22, cy + 18), outline=color, width=3)


def draw_icon(d, kind, box, color):
    {"ship": draw_ship, "climate": draw_climate, "bridge": draw_bridge, "van": draw_van}[kind](
        d, box, color
    )


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 148), fill=NAVY)
    d.rectangle((0, 148, W, 156), fill=RED)

    mast = font(SANS_BOLD, 20)
    d.text((32, 18), "WORLD DESK", font=mast, fill=GOLD)
    d.text((W - 32, 18), "SATURDAY", font=mast, fill=GOLD, anchor="ra")

    date_face = font(SERIF, 48)
    d.text((W / 2, 80), "Saturday 21 November 2026", font=date_face, fill=WHITE, anchor="mm")
    sub = font(SANS, 20)
    d.text(
        (W / 2, 124),
        "What the wires reported on this day",
        font=sub,
        fill=(214, 208, 196),
        anchor="mm",
    )

    title_face = font(SERIF, 30)
    deck_face = font(SANS, 22)
    kick_face = font(SANS_BOLD, 15)
    src_face = font(SANS, 14)

    y = 166
    margin = 28
    text_x = 122
    text_w = W - text_x - margin

    for story in LEADS:
        title_lines = wrap(story["title"], title_face, text_w)
        deck_lines = wrap(story["deck"], deck_face, text_w)
        block_h = 8 + 18 + len(title_lines) * 34 + 4 + len(deck_lines) * 26 + 16
        d.rounded_rectangle((margin, y, W - margin, y + block_h), radius=8, fill=WHITE)
        d.rectangle((margin, y, margin + 8, y + block_h), fill=story["color"])
        draw_icon(d, story["icon"], (margin + 16, y + 12, margin + 88, y + 76), story["color"])
        ty = y + 6
        d.text((text_x, ty), story["kicker"], font=kick_face, fill=story["color"])
        ty += 18
        for line in title_lines:
            d.text((text_x, ty), line, font=title_face, fill=INK)
            ty += 34
        ty += 2
        for line in deck_lines:
            d.text((text_x, ty), line, font=deck_face, fill=INK)
            ty += 26
        d.text((text_x, y + block_h - 16), story["source"], font=src_face, fill=MUTED)
        y += block_h + 5

    brief_top = y
    row_h = 48
    brief_h = row_h * len(BRIEFS) + 8
    footer_gap = 10
    footer_size = 22
    footer_bottom = brief_top + brief_h + footer_gap + footer_size
    if footer_bottom > H - margin:
        raise SystemExit(f"layout overflow: footer ends at {footer_bottom}")
    d.rounded_rectangle((margin, brief_top, W - margin, brief_top + brief_h), radius=8, fill=WHITE)
    d.rectangle((margin, brief_top, margin + 8, brief_top + brief_h), fill=NAVY)
    label_face = font(SANS_BOLD, 18)
    brief_face = font(SANS_BOLD, 22)
    src_brief = font(SANS, 14)
    label_col = max(label_face.getlength(b["label"]) for b in BRIEFS)
    text_x0 = margin + 16 + label_col + 14
    for i, brief in enumerate(BRIEFS):
        ry = brief_top + 6 + i * row_h
        d.text((margin + 16, ry + 12), brief["label"], font=label_face, fill=brief["color"])
        source_w = src_brief.getlength(brief["source"])
        text_right = W - margin - 16
        source_left = text_right - source_w
        text_end = text_x0 + brief_face.getlength(brief["text"])
        if text_end > source_left - 28:
            raise SystemExit(f"brief collides with source: {brief['label']}")
        d.text((text_x0, ry + 8), brief["text"], font=brief_face, fill=INK)
        d.text((text_right, ry + 14), brief["source"], font=src_brief, fill=MUTED, anchor="ra")
        if i < len(BRIEFS) - 1:
            rule_y = ry + row_h - 1
            d.line((margin + 16, rule_y, text_right, rule_y), fill=(228, 220, 206), width=1)

    footer_face = font(SANS_BOLD, footer_size)
    d.text(
        (W / 2, brief_top + brief_h + footer_gap),
        "World news  ·  Saturday 21 November 2026",
        font=footer_face,
        fill=NAVY,
        anchor="ma",
    )

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes footer_bottom={footer_bottom}")


if __name__ == "__main__":
    main()
