"""Ayudas comunes para las ilustraciones del curso OmniAccess Face (usa ilus.py sin modificarlo)."""
import sys
sys.path.insert(0, "/home/claude/ies-training/tools")
from ilus import *  # noqa: F401,F403
from ilus import Node, text, wrap, ICON, e

OUT = "/home/claude/ies-training/ilustraciones/omniaccess-face/"


def save(c, name):
    return c.save(OUT + name)


class FaceTerminal(Node):
    """Terminal facial genérico de pared: frente vertical con cámara, pantalla con óvalo de cara y luz de relleno.
    Anclas: 'eth' y 'relay' a la derecha, 'cam' en la cámara."""
    def __init__(self, x, y, title="Terminal facial", sub="", hl=None, scale=1.0, mark=None):
        w, h = 132 * scale, 236 * scale
        super().__init__(x, y, w, h)
        self.title, self.sub, self.hl, self.s, self.mark = title, sub, hl, scale, mark
        self.anchors["eth"] = (x + w, y + h * 0.62)
        self.anchors["relay"] = (x + w, y + h * 0.80)
        self.anchors["cam"] = (x + w / 2, y + 26 * scale)

    def svg(self):
        x, y, s = self.x, self.y, self.s
        w, h = self.w, self.h
        st = self.hl or DEEP
        out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{18*s:.1f}" fill="#26323F" stroke="{st}" stroke-width="{3 if self.hl else 2}"/>',
               f'<circle cx="{x + w/2:.1f}" cy="{y + 26*s:.1f}" r="{9*s:.1f}" fill="#0B1A28" stroke="#5B6F84" stroke-width="2"/>',
               f'<circle cx="{x + w/2:.1f}" cy="{y + 26*s:.1f}" r="{3.5*s:.1f}" fill="{CYAN}"/>',
               f'<rect x="{x + 22*s:.1f}" y="{y + 18*s:.1f}" width="{18*s:.1f}" height="{6*s:.1f}" rx="3" fill="#F6E7A8" opacity=".85"/>',
               f'<rect x="{x + w - 40*s:.1f}" y="{y + 18*s:.1f}" width="{18*s:.1f}" height="{6*s:.1f}" rx="3" fill="#F6E7A8" opacity=".85"/>',
               f'<rect x="{x + 16*s:.1f}" y="{y + 46*s:.1f}" width="{w - 32*s:.1f}" height="{150*s:.1f}" rx="{10*s:.1f}" fill="#0B1A28" stroke="#5B6F84"/>',
               f'<ellipse cx="{x + w/2:.1f}" cy="{y + 112*s:.1f}" rx="{30*s:.1f}" ry="{40*s:.1f}" fill="none" stroke="{CYAN}" stroke-width="{2.5*s:.1f}" stroke-dasharray="{6*s:.1f} {5*s:.1f}"/>',
               f'<circle cx="{x + w/2:.1f}" cy="{y + 104*s:.1f}" r="{13*s:.1f}" fill="#3A4A5C"/>',
               f'<path d="M{x + w/2 - 24*s:.1f} {y + 150*s:.1f}a{24*s:.1f} {20*s:.1f} 0 0 1 {48*s:.1f} 0z" fill="#3A4A5C"/>',
               f'<rect x="{x + w/2 - 22*s:.1f}" y="{y + 210*s:.1f}" width="{44*s:.1f}" height="{8*s:.1f}" rx="4" fill="#3A4A5C"/>']
        if self.mark is not None:
            col = OK if self.mark else ALERT
            out.append(f'<rect x="{x + 22*s:.1f}" y="{y + 168*s:.1f}" width="{w - 44*s:.1f}" height="{20*s:.1f}" rx="5" fill="{col}"/>')
        out.append(text(x + w / 2, y + h + 26, self.title, 18, 600, INK, FB, anchor="middle"))
        if self.sub:
            out.append(text(x + w / 2, y + h + 48, self.sub, 15, 400, INK3, FM, anchor="middle"))
        return "".join(out)


def card(x, y, w, h, title=None, fill=None, stroke=None, sw=1.5, rx=14):
    """Rectángulo de agrupación con título opcional."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or WHITE}" stroke="{stroke or LINE2}" stroke-width="{sw}"/>']
    if title:
        out.append(text(x + 18, y + 30, title, 17, 600, INK, FB))
    return "".join(out)


def pill(x, y, s, kind="ok", anchor="start"):
    return Chip(x, y, s, kind, mono=False, anchor=anchor)


def icon(x, y, name, color=BLUE, scale=1.4, sw=1.8):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'


def face_thumb(x, y, size=64, ok=None, bad=None):
    """Miniatura de foto de rostro genérica. bad: 'side' (de costado), 'dark' (oscura), 'glasses' (lentes oscuros), 'two' (dos caras)."""
    s = size
    bg = "#D9E6F2" if bad != "dark" else "#55606C"
    out = [f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="8" fill="{bg}" stroke="{LINE2}" stroke-width="1.5"/>']
    head = "#8BA3BA" if bad != "dark" else "#3A4550"
    if bad == "side":
        out.append(f'<ellipse cx="{x + s*0.58:.1f}" cy="{y + s*0.42:.1f}" rx="{s*0.15:.1f}" ry="{s*0.19:.1f}" fill="{head}"/>')
        out.append(f'<path d="M{x + s*0.70:.1f} {y + s*0.42:.1f}l{s*0.08:.1f} {s*0.04:.1f}l{-s*0.08:.1f} {s*0.03:.1f}z" fill="{head}"/>')
    elif bad == "two":
        for cx in (0.32, 0.70):
            out.append(f'<ellipse cx="{x + s*cx:.1f}" cy="{y + s*0.42:.1f}" rx="{s*0.12:.1f}" ry="{s*0.16:.1f}" fill="{head}"/>')
    else:
        out.append(f'<ellipse cx="{x + s/2:.1f}" cy="{y + s*0.42:.1f}" rx="{s*0.17:.1f}" ry="{s*0.21:.1f}" fill="{head}"/>')
        if bad == "glasses":
            out.append(f'<rect x="{x + s*0.34:.1f}" y="{y + s*0.37:.1f}" width="{s*0.32:.1f}" height="{s*0.08:.1f}" rx="2" fill="{BLACK}"/>')
    out.append(f'<path d="M{x + s*0.18:.1f} {y + s:.1f}a{s*0.32:.1f} {s*0.26:.1f} 0 0 1 {s*0.64:.1f} 0z" fill="{head}"/>')
    if ok is not None:
        out.append(Mark(x + s - 4, y + 4, ok))
    return "".join(out)
