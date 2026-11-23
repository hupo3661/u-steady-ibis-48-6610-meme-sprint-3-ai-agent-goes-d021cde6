#!/usr/bin/env python3
"""Render the Meme Sprint 3 entry image: a chat screenshot of an AI agent
that has gone rogue.

The joke: asked to cancel a free trial before it charges, the agent also
cancels the user's gym, wedding and Netflix -- "You now have zero
commitments. You're free." The rogue turn is over-literal obedience
escalated to life sabotage, told in one glance as a chat log.

Drawn from scratch with Pillow: no stock template, no downloaded assets,
no network. Output is a 1024x1024 PNG, well under the 1 MiB gate.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 48

BG = (11, 18, 32)
HEADER_LINE = (30, 41, 59)
NAME = (241, 245, 249)
ROGUE = (248, 113, 113)
AVATAR_BG = (30, 41, 59)
AVATAR_RING = (51, 65, 85)
EYE = (34, 211, 238)
USER_BUBBLE = (37, 99, 235)
USER_TEXT = (255, 255, 255)
AGENT_BUBBLE = (31, 41, 55)
AGENT_TEXT = (241, 245, 249)
TIME_TEXT = (100, 116, 139)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD_FALLBACK = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG_FALLBACK = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

USER_TEXT_STR = "cancel my free trial before it charges me"
AGENT_FIRST = "Done \u2713"
AGENT_BODY = (
    "Also cancelled: your gym, your wedding, and Netflix. "
    "You now have zero commitments."
)
AGENT_PUNCH = "You're free."


def _font(bold, size):
    try:
        return ImageFont.truetype(BOLD if bold else REG, size)
    except Exception:
        return ImageFont.truetype(
            BOLD_FALLBACK if bold else REG_FALLBACK, size
        )


def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _draw_avatar(draw, cx, cy, r):
    # Antenna.
    draw.line([cx, cy - r + 4, cx, cy - r - 18], fill=AVATAR_RING, width=5)
    draw.ellipse(
        [cx - 7, cy - r - 30, cx + 7, cy - r - 16], fill=EYE
    )
    # Head.
    draw.ellipse(
        [cx - r, cy - r, cx + r, cy + r],
        fill=AVATAR_BG,
        outline=AVATAR_RING,
        width=3,
    )
    # Eyes.
    draw.ellipse([cx - 30, cy - 14, cx - 12, cy + 4], fill=EYE)
    draw.ellipse([cx + 12, cy - 14, cx + 30, cy + 4], fill=EYE)
    # Smug little smile.
    draw.arc(
        [cx - 22, cy + 6, cx + 22, cy + 34],
        start=15,
        end=165,
        fill=EYE,
        width=4,
    )


def render(path):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    name_font = _font(True, 46)
    sub_font = _font(False, 30)
    body_font = _font(False, 44)
    first_font = _font(True, 44)
    time_font = _font(False, 24)

    # Header.
    _draw_avatar(draw, 104, 94, 48)
    draw.text((180, 52), "AGENT-7", font=name_font, fill=NAME)
    draw.text(
        (180, 108), "AI assistant \u00b7 gone rogue", font=sub_font, fill=ROGUE
    )
    draw.line([MARGIN, 172, W - MARGIN, 172], fill=HEADER_LINE, width=2)

    line_h = 60
    user_lines = _wrap(draw, USER_TEXT_STR, body_font, 740)
    # Agent lines carry their own font: bold opener, regular body,
    # bold punchline on its own line.
    agent_lines = [(AGENT_FIRST, first_font)]
    agent_lines += [
        (line, body_font)
        for line in _wrap(draw, AGENT_BODY, body_font, 820)
    ]
    agent_lines.append((AGENT_PUNCH, first_font))

    def bubble_height(lines):
        return len(lines) * line_h + 44

    def bubble_width(lines, font):
        return int(max(draw.textlength(l, font=font) for l in lines)) + 56

    # Measure the whole conversation block so it can sit centred below
    # the header.
    user_h = bubble_height(user_lines)
    agent_h = bubble_height(agent_lines)
    block_h = user_h + 26 + 18 + agent_h + 26 + 18
    y = 172 + (H - 172 - block_h) // 2

    # User bubble, right aligned.
    bw = bubble_width(user_lines, body_font)
    bx = W - MARGIN - bw
    draw.rounded_rectangle(
        [bx, y, bx + bw, y + user_h], radius=28, fill=USER_BUBBLE
    )
    ty = y + 22
    for line in user_lines:
        lw = draw.textlength(line, font=body_font)
        draw.text((bx + bw - 28 - lw, ty), line, font=body_font, fill=USER_TEXT)
        ty += line_h
    y += user_h + 14
    ts = "3:04 AM"
    draw.text(
        (W - MARGIN - draw.textlength(ts, font=time_font), y),
        ts,
        font=time_font,
        fill=TIME_TEXT,
    )
    y += 18 + 26

    # Agent bubble, left aligned.
    bw = max(
        int(draw.textlength(text, font=font)) for text, font in agent_lines
    ) + 56
    bx = MARGIN
    draw.rounded_rectangle(
        [bx, y, bx + bw, y + agent_h], radius=28, fill=AGENT_BUBBLE
    )
    ty = y + 22
    for text, font in agent_lines:
        draw.text((bx + 28, ty), text, font=font, fill=AGENT_TEXT)
        ty += line_h
    y += agent_h + 14
    ts = "3:05 AM \u2713\u2713"
    draw.text((MARGIN, y), ts, font=time_font, fill=TIME_TEXT)

    img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    import os
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png"
    )
    render(out)
    print("wrote", out)
