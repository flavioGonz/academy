#!/usr/bin/env python3
"""Arma ilustraciones/omada/manifest-anims-omada.json (animaciones de Resumen, Laboratorio y teoría extra).
El alt sale del <desc> de cada SVG; verifica que cada 'after' exista una sola vez en el lab.md (fuera de bloques de código)
o en theory_md del curso vigente del servidor."""
import html, json, re, sys
from pathlib import Path

CURSO = "/mnt/user-data/uploads/ies-training/sync/omada-srv1029.json"
SITE = Path("/home/claude/ies-training/site2/ilustraciones/omada")
OUT = Path("/home/claude/ies-training/ilustraciones/omada/manifest-anims-omada.json")

R = {  # id: caption del Resumen
    1: "Cortá la fibra y mirá qué sigue andando: con OC300 y Cloud Access, todo en el lugar; con Omada Central, nada se gestiona.",
    2: "Con red bridge la web abre pero el broadcast del EAP no cruza el NAT de Docker; con red host llega al 29810.",
    3: "Un puerto para cada momento: UDP 29810 para presentarse, TCP 29814 para adoptar y gestionar, y los demás ya Connected.",
    4: "Discovery Utility, Inform URL u option 138: los tres le dicen al EAP lo mismo y después llama directo.",
    5: "El segundo ER no entra en el sitio Central: va en su propio sitio, y Auto IPsec une los dos.",
    6: "Mismo uplink, tres redes: cada trama lleva el número de su VLAN y el broadcast no se mezcla.",
    7: "El broadcast queda en la VLAN 30, pero el paquete ruteado llega al NVR hasta que entra la Gateway ACL.",
    8: "La banda de 2.4 GHz en frecuencia: por qué 3 y 9 se pisan con los vecinos, y 1 y 6 no.",
    9: "Cada salto de mesh reparte otra vez el tiempo de aire; Auto Failover busca otro uplink si cae uno.",
    10: "La web que pidió el huésped queda retenida, el portal la reemplaza y, con el voucher validado, navega directo.",
    11: "Con el router del proveedor adelante: UDP 500 y 4500 abiertos, Manual IPsec y el EAP adoptado por adentro del túnel.",
    12: "El .cfg semanal en el SFTP de IES: muere el disco, se restaura en un controlador nuevo y todo vuelve a Connected.",
}
STEPS = {  # id: [(paso, archivo, after, caption)]
    1: [(3, "1-l1.svg", "Si elegiste Central Standard, anotá cuántas licencias",
         "La licencia corre desde que se activa, avisa 30 días antes y, vencida, apaga portal, Fast Roaming y Schedule.")],
    2: [(1, "2-l1.svg", "Verificá AVX",
         "Lo que pasa por dentro: sin AVX, el MongoDB del 6.x no arranca y restart lo vuelve a levantar en bucle."),
        (3, "2-l2.svg", "Esperá la línea de arranque con la versión",
         "Lo que pasa por dentro: Java y MongoDB tardan 1 a 2 minutos; el 8043 contesta recién con la línea de la versión.")],
    3: [(3, "3-l1.svg", "Volvé al controlador e intentá adoptarlo",
         "Lo que pasa en la red: el EAP rechaza la adopción por clave y Retry con la de la web local lo deja Connected.")],
    4: [(5, "4-l1.svg", "Si hay NAT entre sede y controlador",
         "Lo que pasa en la red: el router cambia la IP de destino y deja el puerto igual; en el 6 hace falta también el 29817.")],
    5: [(3, "5-l1.svg", "Cerrá sesión y entrá con ese usuario",
         "Lo que pasa por dentro: el Viewer ve su sitio y su cambio no se aplica; el de un Administrator sí llega al EAP.")],
    6: [(4, "6-l1.svg", "Enchufá una notebook en el puerto 5",
         "Lo que pasa en la red: el DHCP de la VLAN 20 va sin etiqueta en el puerto 5 y con la 20 por el uplink."),
        (5, "6-l2.svg", "Si no agarra IP, revisá en orden",
         "Lo que pasa en la red: dónde muere el Discover según qué pata de la VLAN falla.")],
    7: [(4, "7-l1.svg", "a la VLAN 30, conectá una notebook",
         "Lo que pasa en la red: su gateway responde, la deny descarta el ping a la red interna e internet responde.")],
    8: [(5, "8-l1.svg", "Medí después desde los mismos tres puntos",
         "Lo que pasa en la práctica: un punto por debajo de -70 dBm se corrige subiendo un escalón solo el AP que lo cubre."),
        (6, "8-l2.svg", "programala para las 3:30",
         "Lo que pasa en la red: mientras optimiza, los AP escanean y los clientes quedan sin internet; lejos del reinicio.")],
    9: [(5, "9-l1.svg", "Caminá de un AP al otro y volvé",
         "Lo que pasa en la red: el cliente decide el salto y cada Tiempo de espera agotado es un corte."),
        (6, "9-l2.svg", "activado en el SSID",
         "Lo que pasa en el aire: sin 802.11r hay 4 mensajes de claves en cada salto; con 802.11r, no.")],
    10: [(2, "10-l1.svg", "Authentication > Portal > Create New Portal",
          "Lo que pasa en la red: con HTTPS Redirection el portal va por el 8843, y con certificado propio se ve limpio.")],
    11: [(2, "11-l1.svg", "cambiá la LAN por defecto de cada uno según la tabla",
          "Lo que pasa en la red: los clientes quedan en la red vieja hasta renovar; el ER rechaza la IP vieja y reciben una nueva."),
         (5, "11-l2.svg", "Desde una PC en la Central",
          "Lo que pasa en la red: el ping viaja cifrado como ESP entre las IP públicas y sale igual del otro lado.")],
    12: [(3, "12-l1.svg", "copiá también el volumen de datos con el contenedor detenido",
          "Lo que pasa por dentro: MongoDB cierra en hasta 60 s, tar copia el volumen quieto y start vuelve a levantar."),
         (4, "12-l2.svg", "En el controlador nuevo: en el asistente creá una cuenta local",
          "Lo que pasa por dentro: el restore pisa la cuenta del asistente, y un .cfg más nuevo no entra en un controlador más viejo.")],
}
TEO = {7: [("7-t2.svg", "Funciona como lista negra, con permiso por defecto",
            "La Switch ACL deja pasar todo salvo lo que cortás: permit a lo interno arriba, deny a todo abajo.")]}


def alt(f):
    s = (SITE / f).read_text(encoding="utf-8")
    d = html.unescape(re.search(r'<desc id="d">(.*?)</desc>', s, re.S).group(1)).strip()
    if len(d) > 1000:
        sys.exit(f"alt de {f} tiene {len(d)} caracteres")
    return d


def step_lines(lab, n):
    """Líneas del paso n fuera de bloques de código."""
    out, cur, fence = [], None, False
    for ln in lab.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(\d+)\.\s", ln)
        if m:
            cur = int(m.group(1))
        if cur == n:
            out.append(ln)
    return out


c = json.load(open(CURSO, encoding="utf-8"))
by = {int(l["id"]): l for l in c["lessons"]}
man, errs = {}, []
for lid in range(1, 13):
    l = by[lid]
    e = {"anims": [{"file": f"{lid}-r1.svg", "alt": alt(f"{lid}-r1.svg"), "caption": R[lid]}]}
    lab = l["lab"]["md"]
    nofence = "\n".join(x for x in re.sub(r"```.*?```", "", lab, flags=re.S).split("\n"))
    sts = []
    for n, f, after, cap in STEPS.get(lid, []):
        if nofence.count(after) != 1:
            errs.append(f"{lid}: '{after}' aparece {nofence.count(after)} veces fuera de código")
        if not any(after in ln for ln in step_lines(lab, n)):
            errs.append(f"{lid}: '{after}' no está en el paso {n}")
        sts.append({"step": n, "file": f, "after": after, "alt": alt(f), "caption": cap})
    if sts:
        e["steps"] = sts
    tfs = []
    for f, after, cap in TEO.get(lid, []):
        if l["theory_md"].count(after) != 1:
            errs.append(f"{lid}: teoría '{after}' aparece {l['theory_md'].count(after)} veces")
        tfs.append({"file": f, "after": after, "alt": alt(f), "caption": cap})
    if tfs:
        e["teoria_figs"] = tfs
    for x in [e["anims"][0]] + sts + tfs:
        if not (SITE / x["file"]).exists():
            errs.append(f"falta {x['file']}")
    man[str(lid)] = e
if errs:
    sys.exit("\n".join(errs))
OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, "anims", sum(len(v["anims"]) for v in man.values()), "steps", sum(len(v.get("steps", [])) for v in man.values()),
      "teoria_figs", sum(len(v.get("teoria_figs", [])) for v in man.values()))
