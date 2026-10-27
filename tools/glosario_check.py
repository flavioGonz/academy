#!/usr/bin/env python3
"""Chequeo del glosario de IES Training.

Uso:
    python3 glosario_check.py akuvox mikrotik
    python3 glosario_check.py --all-courses        # todos los cursos con carpeta en claudemy/
    python3 glosario_check.py akuvox --verbose     # muestra dónde aparece cada sigla faltante

Hace tres cosas:
1. Valida site2/data/glosario.json: campos obligatorios, ids y alias únicos,
   tipos correctos, entradas RFC con año y sin guiones largos.
2. Recorre el texto de los cursos pedidos (card.md, quiz.json y script.txt de
   claudemy/<slug>/class/*, más los campos de ilustraciones/<slug>/manifest*.json)
   y lista los RFC citados que no tienen entrada rfcNNNN.
3. Lista las siglas en MAYÚSCULAS de 2 a 6 letras que aparecen en esos textos y
   que no están cubiertas por ningún término o alias del glosario (salvo las de
   la lista IGNORAR: palabras comunes, marcadores de ejemplo, prefijos de modelo).

Sale con código 1 si hay errores de validación o RFC faltantes; las siglas
faltantes son informativas (código 0), para revisarlas a mano.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)                      # /home/claude/ies-training
CLAUDEMY = os.path.join(os.path.dirname(RAIZ), "claudemy")
GLOSARIO = os.path.join(RAIZ, "site2", "data", "glosario.json")
ILUS = os.path.join(RAIZ, "ilustraciones")

CAMPOS = {"id": str, "term": str, "aliases": list, "cat": str, "short": str, "long": str, "case": bool}

# Siglas que no van al glosario: obvias, gritos/énfasis, marcadores de ejemplo
# del laboratorio, prefijos de códigos de modelo y siglas de una sola fuente.
IGNORAR = {
    "IP", "PC", "OK", "USB", "CPU", "MB", "GB", "KB", "TB", "FAQ", "IES", "UTE", "OS",
    "CLAVE", "PEGAR", "LAB", "SAFE", "SOLO", "SERIE", "RESP", "XX", "XXX", "US", "NA",
    "SYSTEM", "DROP", "COMM", "CSO", "BIOS", "XIX", "PB", "PM", "IT", "IC", "CC", "BT",
    "MP", "PH", "SP", "HCP", "ACR", "NS", "NX", "CX", "RJ", "RB", "LOG", "ID",
    "RAM", "ASCII", "SIZE", "TOKEN", "RR", "ORIGEN", "MANO", "WG", "PUERTO",
}

# Marcadores de plantilla de los scripts de laboratorio, como {{PUERTO}}.
RE_PLANTILLA = re.compile(r"\{\{[^{}]*\}\}")

RE_RFC = re.compile(
    r"\bRFCs?\s?-?\s?(\d{3,4})((?:\s*(?:,|y|e|o|a|al)\s*\d{3,4})*)", re.UNICODE)
RE_SIGLA = re.compile(r"(?<![A-Za-z0-9_/.\-])[A-Z]{2,6}(?![A-Za-z0-9_])")
RE_SIGLA_TOKEN = re.compile(r"(?<![A-Za-z0-9_])[A-Z]{2,6}(?![A-Za-z0-9_])")
GUIONES = ("—", "–")


def strings(x):
    if isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)
    elif isinstance(x, str):
        yield x


def textos_de(slug):
    """Devuelve [(ruta_corta, texto)] con todo el texto del curso."""
    out = []
    base = os.path.join(CLAUDEMY, slug, "class")
    for ruta in sorted(glob.glob(os.path.join(base, "*", "card.md")) +
                       glob.glob(os.path.join(base, "*", "script.txt"))):
        with open(ruta, encoding="utf-8") as f:
            out.append((os.path.relpath(ruta, CLAUDEMY), f.read()))
    for ruta in sorted(glob.glob(os.path.join(base, "*", "quiz.json"))):
        try:
            with open(ruta, encoding="utf-8") as f:
                out.append((os.path.relpath(ruta, CLAUDEMY), "\n".join(strings(json.load(f)))))
        except (OSError, ValueError) as e:
            print(f"  aviso: no pude leer {ruta}: {e}")
    for ruta in sorted(glob.glob(os.path.join(ILUS, slug, "manifest*.json"))):
        try:
            with open(ruta, encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, ValueError) as e:
            print(f"  aviso: no pude leer {ruta} (¿lo están escribiendo?): {e}")
            continue
        # De cada lección: teoria_md, concepts y los textos de figuras/pasos.
        out.append((os.path.relpath(ruta, RAIZ), "\n".join(strings(datos))))
    return out


def rfcs_en(texto):
    """Números de RFC citados, expandiendo 'RFC 1034 y 1035' y 'RFC 9110 a 9112'."""
    nums = set()
    for m in RE_RFC.finditer(texto):
        primero = int(m.group(1))
        nums.add(primero)
        resto = m.group(2) or ""
        previo = primero
        for sep, n in re.findall(r"\s*(,|y|e|o|a|al)\s*(\d{3,4})", resto):
            n = int(n)
            if sep in ("a", "al") and previo < n <= previo + 20:
                nums.update(range(previo, n + 1))
            else:
                nums.add(n)
            previo = n
    return nums


def validar(doc):
    errores = []
    if not isinstance(doc, dict) or "terms" not in doc or "version" not in doc:
        return ["el JSON tiene que ser {\"version\": ..., \"terms\": [...]}"]
    ids = Counter()
    formas = defaultdict(list)   # forma en minúscula -> [(forma, case, id)]
    for i, e in enumerate(doc["terms"]):
        ref = e.get("id", f"#{i}")
        for campo, tipo in CAMPOS.items():
            if campo not in e:
                errores.append(f"{ref}: falta el campo '{campo}'")
            elif not isinstance(e[campo], tipo):
                errores.append(f"{ref}: '{campo}' tiene que ser {tipo.__name__}")
        if not isinstance(e.get("aliases"), list):
            continue
        for campo in ("term", "short", "long", "cat"):
            if isinstance(e.get(campo), str) and not e[campo].strip():
                errores.append(f"{ref}: '{campo}' está vacío")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(e.get("id", ""))):
            errores.append(f"{ref}: id con caracteres no válidos")
        ids[e.get("id")] += 1
        for campo in ("term", "short", "long"):
            if any(g in str(e.get(campo, "")) for g in GUIONES):
                errores.append(f"{ref}: '{campo}' tiene guion largo")
        if "year" in e and not (isinstance(e["year"], int) and 1960 <= e["year"] <= 2100):
            errores.append(f"{ref}: 'year' tiene que ser un año entero")
        if e.get("cat") == "RFC":
            m = re.fullmatch(r"RFC (\d+)", e.get("term", ""))
            if not m or e.get("id") != f"rfc{m.group(1)}":
                errores.append(f"{ref}: una entrada RFC tiene term 'RFC NNNN' e id 'rfcNNNN'")
            if "year" not in e:
                errores.append(f"{ref}: a la entrada RFC le falta 'year'")
        caso = e.get("case", True)
        for forma in [e.get("term", "")] + list(e.get("aliases", [])):
            if not isinstance(forma, str) or not forma.strip():
                errores.append(f"{ref}: alias vacío o no es texto")
                continue
            formas[forma.lower()].append((forma, caso, ref))
    # Dos formas chocan si son iguales (respetando mayúsculas cuando las dos
    # entradas tienen case=true) o iguales sin mayúsculas si alguna tiene case=false.
    for grupo in formas.values():
        for a in range(len(grupo)):
            for b in range(a + 1, len(grupo)):
                fa, ca, ra = grupo[a]
                fb, cb, rb = grupo[b]
                if (ca and cb and fa != fb):
                    continue
                if ra == rb:
                    errores.append(f"{ra}: forma repetida '{fa}'")
                else:
                    errores.append(f"'{fa}' está en '{ra}' y '{fb}' en '{rb}'")
    for k, n in ids.items():
        if n > 1:
            errores.append(f"id repetido: {k} ({n} veces)")
    return sorted(set(errores))


def cubiertas(doc):
    """Siglas cubiertas: las que aparecen dentro de algún término o alias."""
    exactas, sin_caso = set(), set()
    for e in doc.get("terms", []):
        for forma in [e.get("term", "")] + list(e.get("aliases", [])):
            for tok in RE_SIGLA_TOKEN.findall(forma):
                exactas.add(tok)
            if not e.get("case", True):
                sin_caso.add(forma.lower())
                for tok in re.findall(r"[A-Za-z]{2,6}", forma):
                    sin_caso.add(tok.lower())
    return exactas, sin_caso


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cursos", nargs="*", help="slugs de curso, por ejemplo akuvox mikrotik")
    ap.add_argument("--all-courses", action="store_true", help="revisar todos los cursos de claudemy/")
    ap.add_argument("--glosario", default=GLOSARIO)
    ap.add_argument("--verbose", "-v", action="store_true", help="mostrar archivos de ejemplo")
    ap.add_argument("--min", type=int, default=1, help="mostrar siglas con al menos N apariciones")
    args = ap.parse_args()

    cursos = args.cursos
    if args.all_courses:
        cursos = sorted(os.path.basename(os.path.dirname(p))
                        for p in glob.glob(os.path.join(CLAUDEMY, "*", "class")))
    if not cursos:
        ap.error("pasá al menos un curso (o --all-courses)")

    with open(args.glosario, encoding="utf-8") as f:
        doc = json.load(f)
    terms = doc.get("terms", [])
    n_rfc = sum(1 for e in terms if e.get("cat") == "RFC")
    print(f"Glosario: {args.glosario}")
    print(f"  versión {doc.get('version')}, {len(terms)} entradas, {n_rfc} RFC")

    errores = validar(doc)
    print(f"\n== Validación del JSON: {'OK' if not errores else f'{len(errores)} errores'}")
    for e in errores:
        print("  -", e)

    ids = {e.get("id") for e in terms}
    exactas, sin_caso = cubiertas(doc)
    faltan_rfc_total = 0
    for slug in cursos:
        textos = textos_de(slug)
        if not textos:
            print(f"\n== {slug}: no encontré textos")
            continue
        rfc_donde = defaultdict(set)
        siglas = Counter()
        siglas_donde = defaultdict(set)
        for ruta, t in textos:
            for n in rfcs_en(t):
                rfc_donde[n].add(ruta)
            for s in RE_SIGLA.findall(RE_PLANTILLA.sub(" ", t)):
                siglas[s] += 1
                siglas_donde[s].add(ruta)
        faltan_rfc = sorted(n for n in rfc_donde if f"rfc{n}" not in ids)
        faltan_rfc_total += len(faltan_rfc)
        print(f"\n== {slug}: {len(textos)} archivos, {len(rfc_donde)} RFC citados")
        print(f"  RFC citados: {', '.join(str(n) for n in sorted(rfc_donde))}")
        print(f"  RFC sin entrada en el glosario: {', '.join(map(str, faltan_rfc)) if faltan_rfc else 'ninguno'}")
        if args.verbose:
            for n in faltan_rfc:
                print(f"    RFC {n}: {', '.join(sorted(rfc_donde[n])[:3])}")
        faltan = [(s, c) for s, c in siglas.most_common()
                  if s not in exactas and s.lower() not in sin_caso
                  and s not in IGNORAR and c >= args.min]
        print(f"  Siglas en mayúsculas sin entrada (revisar a mano): {len(faltan)}")
        for s, c in faltan:
            extra = f"  [{', '.join(sorted(siglas_donde[s])[:2])}]" if args.verbose else ""
            print(f"    {s} ({c}){extra}")

    if errores or faltan_rfc_total:
        sys.exit(1)


if __name__ == "__main__":
    main()
