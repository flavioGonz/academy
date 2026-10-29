#!/usr/bin/env python3
"""Arma ilustraciones/unifi/manifest-anims-unifi.json con las animaciones "Cómo se ve en la red" (anims) y las de
Laboratorio (steps). El alt sale del <desc> de cada SVG generado; los after se verifican contra lab.md del curso vigente
(sync/unifi-srv1029.json): tienen que existir una sola vez y fuera de los bloques de código."""
import html
import json
import re
from pathlib import Path

SITE = Path("/home/claude/ies-training/site2/ilustraciones/unifi")
OUT = Path("/home/claude/ies-training/ilustraciones/unifi/manifest-anims-unifi.json")
CURSO = Path("/mnt/user-data/uploads/ies-training/sync/unifi-srv1029.json")

R = {  # id: caption de la animación del Resumen
    "1": "Cada equipo tiene un solo host: con UXG, el server central; con UCG, el propio UCG. Site Manager solo es la puerta.",
    "2": "Un AP de otra obra sigue fiel a su host viejo: borrarlo allá, resetear y adoptar con el firmware al día.",
    "3": "Detrás de NAT, el controlador conoce su IP interna: con Inform Host y Override anuncia un nombre al que el AP llega.",
    "4": "Las consolas salen hacia Site Manager y son de la empresa; los técnicos entran con su rol y la plantilla marca al que se apartó.",
    "5": "Tres redes viajan etiquetadas por el mismo cable; quién habla con quién lo decide la zona en el gateway.",
    "6": "Con un switch de terceros en el medio, la gestión del AP va sin etiqueta y los SSID etiquetados, de punta a punta.",
    "7": "En 2.4 GHz solo 1, 6 y 11 no se pisan: el mismo canal se comparte por turnos y uno intermedio ensucia a dos.",
    "8": "Con menos potencia las celdas se tocan en el borde y cada celular queda en el AP cercano; el rincón débil pide un AP más.",
    "9": "Un equipo viejo que no entiende Fast Roaming no se conecta: va a un SSID de legado en su VLAN, sin apagar FT para todos.",
    "10": "Un WiFi solo con contraseña en zona Hotspot muestra un portal hasta desmarcar Show Landing Page; el aislamiento sigue igual.",
    "11": "El backup se baja antes de actualizar: es de la versión vieja y es el que sirve para volver.",
    "12": "Roam en el borde, desconexión y reconexión o ping-pong: cada patrón del historial dice qué cambiar primero.",
}
L = {  # id: [(paso, archivo, after, caption)]
    "1": [(3, "1-l1.svg", "Al terminar, el instalador indica la dirección de acceso",
           "Lo que pasa en la red en este paso: la notebook abre por HTTPS la dirección que dio el instalador, crea el admin local y lee las versiones.")],
    "2": [(3, "2-l1.svg", "Buscá la IP que tomó el AP",
           "Lo que pasa en la red en este paso: SSH al puerto 22 con ubnt / ubnt, info responde con el estado y el AP se sigue anunciando por UDP 10001."),
          (5, "2-l2.svg", "y no actualiza solo, bajá el firmware",
           "Lo que pasa en la red en este paso: el AP descarga la imagen él mismo por HTTPS, reinicia y vuelve listo para adoptar.")],
    "3": [(1, "3-l1.svg", "Opción A, DHCP option 43 en RouterOS 7",
           "Lo que pasa en la red en este paso: la opción 43 viaja en el Offer y el Ack del DHCP y el AP la lee como 10.10.10.5."),
          (2, "3-l2.svg", "Opción B, DNS.",
           "Lo que pasa en la red en este paso: el AP consulta el nombre unifi al DNS del MikroTik y la entrada estática contesta 10.10.10.5.")],
    "4": [(2, "4-l1.svg", "Si no aparece en Site Manager, desde una PC de esa red",
           "Lo que pasa en la red en este paso: la consulta DNS y el SYN al 443 muestran si la salida está abierta o bloqueada.")],
    "5": [(4, "5-l1.svg", "Para CCTV en zona propia, creá una política",
           "Lo que pasa en la red en este paso: el NVR pasa por la regla que lo permite; la PC de Staff y la cámara caen en el bloqueo.")],
    "6": [(3, "6-l1.svg", "Hacé Power Cycle del puerto (PoE)",
           "Lo que pasa en la red en este paso: la cámara pide IP sin etiqueta, el puerto la pone en la VLAN 30 y el DHCP de esa VLAN contesta.")],
    "7": [(1, "7-l1.svg", "UniFi Devices > elegí un AP > AirView > Environment",
           "Lo que pasa en la red en este paso: con el escaneo Full la radio deja a sus clientes y recorre los canales midiendo el aire."),
          (5, "7-l2.svg", "Si los canales 36 a 48 están saturados y querés probar DFS",
           "Lo que pasa en la red en este paso: en un canal DFS, si aparece un radar el AP deja el canal en el acto y los clientes se cortan.")],
    "8": [(4, "8-l1.svg", "Repetí la caminata.",
           "Lo que pasa en la red en este paso: en los mismos puntos, el celular cambia de AP en el medio y en C queda en el AP 2 con -65 dBm o mejor.")],
    "9": [(3, "9-l1.svg", "Con un celular en llamada de voz o video",
           "Lo que pasa en la red en este paso: sin FT el roam lleva ocho tramas o más; con FT, cuatro, y la voz sigue.")],
    "10": [(5, "10-l1.svg", "Desde un celular: conectate, ingresá el voucher, navegá.",
            "Lo que pasa en la red en este paso: hacia internet vuelve el SYN-ACK; hacia la impresora el SYN se queda en el gateway y se vence el tiempo.")],
    "11": [(5, "11-l1.svg", "porque cambió la IP del controlador, apuntalos al nuevo",
            "Lo que pasa en la red en este paso: los equipos mandan el inform a la IP vieja hasta que set-inform los apunta al controlador nuevo.")],
    "12": [(4, "12-l1.svg", "Port Manager > Time Machine del puerto del AP",
            "Lo que pasa en la red en este paso: si el uplink se cae, todos los clientes del AP se desconectan a la misma hora que marca el puerto.")],
}


def desc(f):
    s = (SITE / f).read_text(encoding="utf-8")
    return html.unescape(re.search(r'<desc id="d">(.*?)</desc>', s, re.S).group(1))


def outside_code(md):
    out, fence = [], False
    for ln in md.split("\n"):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if not fence:
            out.append(ln)
    return "\n".join(out)


curso = {str(l["id"]): l for l in json.load(open(CURSO, encoding="utf-8"))["lessons"]}
man = {}
for lid in sorted(R, key=int):
    lab = curso[lid]["lab"]["md"]
    plain = outside_code(lab)
    ent = {"anims": [{"file": f"{lid}-r1.svg", "alt": desc(f"{lid}-r1.svg"), "caption": R[lid]}], "steps": []}
    for paso, f, after, cap in L[lid]:
        assert plain.count(after) == 1 and lab.count(after) == 1, f"ancla no única o ausente en {lid}: {after}"
        ent["steps"].append({"step": paso, "file": f, "after": after, "alt": desc(f), "caption": cap})
    for x in ent["anims"] + ent["steps"]:
        assert len(x["alt"]) <= 1000, x["file"]
    man[lid] = ent
OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"ok {OUT} · {len(man)} lecciones · {sum(len(v['anims']) for v in man.values())} anims · {sum(len(v['steps']) for v in man.values())} steps")
