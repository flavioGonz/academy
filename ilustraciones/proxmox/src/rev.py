"""Renderiza SVG fijos (con flock) y arma un montaje 2x2 para revisar: python3 rev.py 3.svg 3-paso1.svg ..."""
import sys, subprocess
from PIL import Image
D = "/home/claude/ies-training/ilustraciones/proxmox/"
fs = sys.argv[1:]
subprocess.run(["flock", "/home/claude/ies-training/render.lock", "python3", "/home/claude/ies-training/tools/render_svg.py"] + [D + f for f in fs], check=True)
ims = [Image.open(D + f.replace(".svg", ".png")).convert("RGB") for f in fs]
W, H = 1200, 675
rows = (len(ims) + 1) // 2
m = Image.new("RGB", (W * 2, H * rows), "white")
for i, im in enumerate(ims):
    m.paste(im, ((i % 2) * W, (i // 2) * H))
m.save(D + "_rev-fijas.png")
print("montaje", D + "_rev-fijas.png")
