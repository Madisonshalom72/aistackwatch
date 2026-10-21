#!/usr/bin/env python3
"""Programmatic OG/share images (1200x630) for AI StackWatch 24 — PIL renders,
site + per-layer variants + brief/breakthroughs. Dark futuristic theme."""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
W, H = 1200, 630
BG = (5, 7, 13)
CYAN = (34, 211, 238)
GOLD = (245, 197, 66)
WHITE = (235, 242, 250)
DIM = (140, 155, 175)

def font(sz, bold=True):
    paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
             else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def render(name, kicker, title_lines, sub, accent):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # grid lines
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(12, 18, 30))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(12, 18, 30))
    # accent frame + glow bar
    d.rectangle([24, 24, W - 24, H - 24], outline=accent, width=3)
    d.rectangle([24, 24, W - 24, 34], fill=accent)
    d.text((70, 84), kicker, font=font(30), fill=accent)
    y = 140
    for line in title_lines:
        d.text((70, y), line, font=font(76), fill=WHITE)
        y += 92
    d.text((70, y + 18), sub, font=font(30, bold=False), fill=DIM)
    d.text((70, H - 84), "AI STACKWATCH 24", font=font(28), fill=GOLD)
    d.text((W - 430, H - 84), "madisonshalom72.github.io/aistackwatch", font=font(22, bold=False), fill=DIM)
    img.save(os.path.join(OUT, name), "PNG")
    print("wrote", name)

LAYERS = {
    1: ("LAYER 1 · ENERGY", (52, 211, 153)),
    2: ("LAYER 2 · CHIPS", (167, 139, 250)),
    3: ("LAYER 3 · CLOUD & INFRASTRUCTURE", (96, 165, 250)),
    4: ("LAYER 4 · AI MODELS", (244, 114, 182)),
    5: ("LAYER 5 · PLATFORMS", (34, 211, 238)),
    6: ("LAYER 6 · APPLICATIONS", (245, 197, 66)),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render("og-home.png", "DAILY MARKET INTELLIGENCE", ["WHO IS BUILDING", "THE AI REVOLUTION?"],
           "36 companies · 6 layers · tracked daily with real market data", CYAN)
    for n, (kick, acc) in LAYERS.items():
        render(f"og-layer-{n}.png", kick, ["AI STACKWATCH 24"],
               "Daily prices, movers and notes for this layer of the AI stack", acc)
    render("og-brief.png", "THE DAILY BRIEF", ["TODAY IN THE", "AI STACK"],
           "The market wrap across all 36 tracked companies", GOLD)
    render("og-breakthroughs.png", "HOT TECH BREAKTHROUGHS", ["THE STORIES MOVING", "THE AI STACK"],
           "Verified breakthroughs from the companies on the map", (244, 114, 182))
