#!/usr/bin/env python3
"""Validador simple del campo script_rsc en los manifests de MikroTik (IES Training).

Uso:
  python3 /home/claude/ies-training/tools/rsc_check.py [carpeta_o_manifest ...]
Sin argumentos recorre /home/claude/ies-training/ilustraciones/mikrotik/manifest*.json.

Revisa, por cada lección que tenga script_rsc:
  - forma: titulo, descripcion, variables (nombre/valor/detalle), codigo, notas
  - variables {{X}}: todas declaradas en "variables", ninguna declarada sin usar, nombres en MAYUSCULAS sin repetir
  - llaves, corchetes y paréntesis balanceados y comillas cerradas (fuera de comentarios, con escapes \\")
  - longitud: 15 a 60 líneas
  - cosas que rompen el pegado en la terminal: tabs (autocompletan), '?' fuera de strings (abre la ayuda),
    caracteres no ASCII fuera de comentarios (se imprimen como \\XX)
  - que lo que se crea lleve comment="ies-..." y que termine con un :put "Listo: ..."
Sale con código 1 si hay errores. Las advertencias no cortan.
"""
import json
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path("/home/claude/ies-training/ilustraciones/mikrotik")
VAR_RE = re.compile(r"\{\{([^{}]*)\}\}")
NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
PAIRS = {")": "(", "]": "[", "}": "{"}


def scan(code):
    """Recorre el código como lo haría RouterOS: comentarios (# fuera de string) y strings con escapes.

    Devuelve (errores, avisos, código_sin_comentarios_ni_strings)."""
    errs, warns = [], []
    stack = []
    bare = []  # código sin comentarios ni contenido de strings, para otros chequeos
    in_str = False
    str_line = 0
    lines = code.split("\n")
    for ln, line in enumerate(lines, 1):
        i = 0
        at_line_start = True
        while i < len(line):
            ch = line[i]
            if in_str:
                if ch == "\\":
                    i += 2
                    continue
                if ch == '"':
                    in_str = False
                    bare.append('"')
                i += 1
                continue
            if ch == "#" and (at_line_start or line[:i].rstrip().endswith(";")):
                # comentario hasta el fin de la línea
                break
            if not ch.isspace():
                at_line_start = False
            if ch == '"':
                in_str = True
                str_line = ln
                bare.append('"')
            elif ch in "([{":
                stack.append((ch, ln))
                bare.append(ch)
            elif ch in ")]}":
                if not stack:
                    errs.append(f"línea {ln}: '{ch}' de más (no hay apertura)")
                else:
                    op, oln = stack.pop()
                    if op != PAIRS[ch]:
                        errs.append(f"línea {ln}: '{ch}' cierra '{op}' abierto en la línea {oln}")
                bare.append(ch)
            else:
                bare.append(ch)
            i += 1
        if in_str and not line.endswith("\\"):
            errs.append(f"línea {str_line}: comillas sin cerrar")
            in_str = False
        bare.append("\n")
    for op, oln in stack:
        errs.append(f"línea {oln}: '{op}' sin cerrar")
    return errs, warns, "".join(bare)


def comment_lines(code):
    out = []
    for ln, line in enumerate(code.split("\n"), 1):
        if line.lstrip().startswith("#"):
            out.append((ln, line))
    return out


def check_script(sr):
    errs, warns = [], []
    for k in ("titulo", "descripcion", "variables", "codigo", "notas"):
        if k not in sr:
            errs.append(f"falta el campo '{k}'")
    if errs:
        return errs, warns
    if not isinstance(sr["variables"], list) or not isinstance(sr["notas"], list):
        errs.append("'variables' y 'notas' tienen que ser listas")
        return errs, warns
    code = sr["codigo"]

    # variables
    declared = {}
    for v in sr["variables"]:
        for k in ("nombre", "valor", "detalle"):
            if k not in v:
                errs.append(f"variable sin '{k}': {v}")
        n = v.get("nombre", "")
        if not NAME_RE.match(n):
            errs.append(f"nombre de variable inválido: '{n}' (MAYUSCULAS, números y _)")
        if n in declared:
            errs.append(f"variable repetida: {n}")
        declared[n] = str(v.get("valor", ""))
        val = declared[n]
        if any(c in val for c in '"$\\'):
            warns.append(f"el valor de {n} tiene comillas, $ o barra invertida: rompe el script")
    used = VAR_RE.findall(code)
    for n in sorted(set(used)):
        if n not in declared:
            errs.append(f"{{{{{n}}}}} se usa pero no está declarada en 'variables'")
    for n in declared:
        if n not in used:
            errs.append(f"variable declarada y no usada: {n}")
    # marcas mal formadas, por ejemplo {{X} o {X}}
    rest = VAR_RE.sub("", code)
    if re.search(r"\{\{[A-Z_]", rest) or re.search(r"[A-Z_]\}\}", rest):
        errs.append("hay una marca de variable mal formada ({{X} o {X}})")

    # longitud
    nlines = len(code.rstrip("\n").split("\n"))
    if not 15 <= nlines <= 60:
        errs.append(f"{nlines} líneas (tiene que tener entre 15 y 60)")

    # sintaxis, con los valores de ejemplo ya reemplazados
    filled = VAR_RE.sub(lambda m: declared.get(m.group(1), "X"), code)
    e2, w2, bare = scan(filled)
    errs += e2
    warns += w2

    # pegado en la terminal
    if "\t" in code:
        errs.append("tiene tabs: en la terminal autocompletan")
    if "\r" in code:
        errs.append("tiene \\r: usar solo \\n")
    noncomment = "\n".join(l for l in code.split("\n") if not l.lstrip().startswith("#"))
    if "?" in bare:
        errs.append("tiene '?' fuera de strings: en la terminal abre la ayuda")
    elif "?" in noncomment:
        warns.append("tiene '?' dentro de un string: en RouterOS 7 es literal (el escape \\? se quitó en 7.1rc2), pero probalo pegándolo en la terminal")
    bad = sorted({c for c in noncomment if ord(c) > 127})
    if bad:
        errs.append("caracteres no ASCII fuera de comentarios (se ven como \\XX): " + "".join(bad))
    for ln, line in comment_lines(code):
        if "?" in line:
            warns.append(f"línea {ln}: '?' en un comentario (la terminal lo toma como ayuda)")
        if any(ord(c) > 127 for c in line):
            warns.append(f"línea {ln}: caracteres no ASCII en un comentario")

    # comentarios ies- en lo que se crea, y cierre con :put "Listo
    creates = re.search(r"/add\b", noncomment)
    if creates and not re.search(r'comment=\(?"ies-', code):
        errs.append('agrega cosas pero ningún comment="ies-..."')
    adds = len(re.findall(r"/add\b", noncomment))
    tagged = len(re.findall(r'comment=\(?"ies-', code))
    if adds and tagged < adds:
        warns.append(f"{adds} '/add' y {tagged} comment=\"ies-...\": revisá que cada cosa creada se pueda encontrar")
    if not re.search(r':put \(?"Listo', code):
        errs.append('falta el :put "Listo: ..." final')
    if not code.lstrip().startswith("#"):
        warns.append("no empieza con el comentario de encabezado")
    return errs, warns


def manifests(args):
    if not args:
        return sorted(DEFAULT_DIR.glob("manifest*.json"))
    out = []
    for a in args:
        p = Path(a)
        out += sorted(p.glob("manifest*.json")) if p.is_dir() else [p]
    return out


def main():
    total_err = total_warn = n_scripts = 0
    for mf in manifests(sys.argv[1:]):
        try:
            data = json.loads(mf.read_text(encoding="utf-8"))
        except Exception as e:  # JSON roto
            print(f"ERROR {mf.name}: JSON inválido: {e}")
            total_err += 1
            continue
        for lid, entry in sorted(data.items(), key=lambda kv: (len(kv[0]), kv[0])):
            if not isinstance(entry, dict) or "script_rsc" not in entry:
                continue
            n_scripts += 1
            errs, warns = check_script(entry["script_rsc"])
            nl = len(entry["script_rsc"].get("codigo", "").rstrip("\n").split("\n"))
            estado = "OK   " if not errs else "ERROR"
            print(f"{estado} {mf.name} lección {lid}: {nl} líneas, {len(entry['script_rsc'].get('variables', []))} variables")
            for e in errs:
                print(f"      error: {e}")
            for w in warns:
                print(f"      aviso: {w}")
            total_err += len(errs)
            total_warn += len(warns)
    print(f"\n{n_scripts} scripts revisados, {total_err} errores, {total_warn} avisos")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
