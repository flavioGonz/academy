#!/usr/bin/env python3
"""Arma ilustraciones/omada/manifest-teoria-1-12.json (solo teoria_figs) y valida las anclas contra el teoria_md combinado.
El alt sale del <desc> de cada SVG para que coincida con la animación."""
import glob, html, json, re, sys
from pathlib import Path

BASE = Path("/home/claude/ies-training/ilustraciones/omada")
SITE = Path("/home/claude/ies-training/site2/ilustraciones/omada")

FIGS = {
    "1": ("1-t1.svg", "como el portal cautivo, deja de autenticar",
          "Mirá qué sigue andando y qué se frena cuando el controlador desaparece."),
    "2": ("2-t1.svg", "se puede borrar y recrear sin perder nada",
          "El contenedor se borra y se recrea; la configuración vive en el volumen."),
    "3": ("3-t1.svg", "es sospechoso habitual",
          "Cada síntoma corta la adopción en un momento distinto, y apunta a una causa distinta."),
    "4": ("4-t1.svg", "Llega con cada concesión nueva",
          "La option 138 viaja en la respuesta DHCP; después el EAP llama directo al controlador."),
    "5": ("5-t1.svg", "cada usuario lleva un rol MSP y un rol Customer",
          "El mismo árbol de cliente y sitios, visto por tres roles distintos."),
    "6": ("6-t1.svg", "Si cualquiera de los tres tramos falla, no hay IP",
          "Seguí el pedido DHCP de la cámara: la etiqueta 20 aparece y desaparece en el switch."),
    "7": ("7-t1.svg", "nunca llega a actuar",
          "Seguí cada paquete por la lista: la primera regla que coincide decide."),
    "8": ("8-t1.svg", "achica la celda sin dejar huecos",
          "Mismo canal: se turnan. Canales distintos: hablan a la vez. Después, la potencia."),
    "9": ("9-t1.svg", "el problema no es de roaming sino de potencia",
          "Mirá la barra de señal: el cliente salta cuando cruza su propio umbral."),
    "10": ("10-t1.svg", "para los que tienen que navegar sin portal",
           "Qué deja pasar el EAP según el estado de cada cliente, y qué pasa sin controlador."),
    "11": ("11-t1.svg", "el router nunca mandaría nada al túnel",
           "Primero IKE por UDP 500 (o 4500 con NAT), después ESP cifrado por el túnel."),
    "12": ("12-t1.svg", "Si se hace Forget antes, los equipos quedan sin controlador",
           "Mirá el estado de los equipos en cada controlador durante la migración."),
}


def teoria():
    d = {}
    for f in sorted(glob.glob(str(BASE / "manifest*.json"))):
        if "teoria-" in Path(f).name:
            continue
        for k, v in json.load(open(f)).items():
            d.setdefault(k, {}).update(v)
    return d


def main():
    d, out, errs = teoria(), {}, []
    for lid, (file, after, cap) in FIGS.items():
        svg = (SITE / file).read_text(encoding="utf-8")
        alt = html.unescape(re.search(r'<desc id="d">(.*?)</desc>', svg, re.S).group(1))
        th = d[lid]["teoria_md"]
        n = th.count(after)
        line = next((ln for ln in th.splitlines() if after in ln), "")
        if n != 1:
            errs.append(f"{lid}: ancla aparece {n} veces")
        if line.lstrip().startswith("#"):
            errs.append(f"{lid}: ancla en un título")
        if not 15 <= len(after) <= 60:
            errs.append(f"{lid}: ancla de {len(after)} caracteres")
        kb = (SITE / file).stat().st_size / 1024
        if kb >= 120:
            errs.append(f"{lid}: {file} pesa {kb:.0f} KB")
        if any(c in alt + cap for c in "—–"):
            errs.append(f"{lid}: guion largo en alt o caption")
        out[lid] = {"teoria_figs": [{"file": file, "after": after, "alt": alt, "caption": cap}]}
        print(f"{lid:>2} {file:10} {kb:5.0f} KB  ancla x{n}")
    (BASE / "manifest-teoria-1-12.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("errores:", errs or "ninguno")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
