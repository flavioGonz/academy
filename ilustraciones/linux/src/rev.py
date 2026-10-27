"""Montaje de PNG para revisar: python3 rev.py a.png b.png ... -> ../_rev.png"""
import sys
from PIL import Image
fs = sys.argv[1:]
W, H = 1200, 675
cols = 2
rows = (len(fs) + 1) // 2
m = Image.new("RGB", (W * cols, H * rows), "white")
for i, f in enumerate(fs):
    m.paste(Image.open(f).convert("RGB").resize((W, H)), ((i % 2) * W, (i // 2) * H))
m.save("/home/claude/ies-training/ilustraciones/linux/_rev.png")
