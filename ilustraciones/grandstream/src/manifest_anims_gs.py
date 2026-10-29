#!/usr/bin/env python3
"""Arma ilustraciones/grandstream/manifest-anims-grandstream.json (Resumen "Cómo se ve en la red" y Laboratorio)
para las lecciones 1 a 18. El alt de cada animación es la <desc> del propio SVG (una sola fuente de verdad)."""
import html, json, re
from pathlib import Path

SITE = Path("/home/claude/ies-training/site2/ilustraciones/grandstream")
OUT = Path("/home/claude/ies-training/ilustraciones/grandstream/manifest-anims-grandstream.json")


def alt(name):
    s = (SITE / name).read_text(encoding="utf-8")
    m = re.search(r'<desc id="d">(.*?)</desc>', s, re.S)
    return html.unescape(m.group(1)).strip()


R = {  # lección: caption del Resumen
    1: "Mirá quién contesta el DHCP del teléfono: en Switch el router, en Route la UCM con la opción 66.",
    2: "Mirá la lista de registros: el límite frena al equipo de más aunque tenga la clave.",
    3: "Del Discover al 200 OK: la URL de la opción 66 llega junto con la IP del teléfono.",
    4: "Mirá la sesión del router: la abre el REGISTER y por ella vuelven las respuestas y entran las llamadas.",
    5: "Aunque la extensión tenga el nivel, el número no llega al proveedor sin el PIN.",
    6: "Una ruta, tres llamadas: lo que queda después del Strip es la interna; con otro formato, no coincide.",
    7: "La pata del troncal no cambia: la UCM atiende, recibe la tecla y une la llamada con ventas.",
    8: "Con todos ocupados el grupo manda al buzón; la cola retiene y entrega cuando alguien se libera.",
    9: "Mirá la línea c= que recibe cada teléfono: sin Local Network Address, la oficina recibe la pública.",
    10: "Compará el SDP que salió con el que llegó: el ALG cambió la IP y se perdió un sentido del audio.",
    11: "Seguí el contador: al llegar al límite la IP queda en la Blocklist y la UCM deja de contestarle.",
    12: "El grupo hace sonar a los dos teléfonos; el que atiende se queda con la llamada y al otro se le cancela.",
    13: "Mientras la alarma tiene el par, para Antel la línea está ocupada y el FXO2 no ve el timbre.",
    14: "Seguí los colores: cada FXO es una troncal con nombre, y el Dashboard muestra qué pasa en cada una.",
    15: "Cada señal de corte tiene su detector en la troncal; si ninguno la reconoce, la línea queda tomada.",
    16: "Primero el teléfono con pantalla: dice si falta el servicio o si falta acertar el esquema.",
    17: "Cada línea entra por su troncal y su ruta: horario para la línea 1, directo al fax para la 2.",
    18: "Cada prueba saca un sospechoso; con el cruce de pares se sabe si llamar a Antel o seguir en la central.",
}

STEPS = {  # lección: [(paso, archivo, ancla exacta en lab.md, caption)]
    1: [(5, "1-l1.svg", "Con el backup guardado, recién ahí actualizá",
         "Lo que pasa en este paso: el .tar sale de la central antes de que entre el firmware, y vuelve con Restore si algo sale mal.")],
    2: [(3, "2-l1.svg", "En cada una, revisá:",
         "Lo que pasa en la red en este paso: con Direct Media activado la central les pasa a los teléfonos la dirección del otro y el audio directo no cruza el NAT.")],
    3: [(6, "3-l1.svg", "Comprobá en el teléfono que la cuenta registró",
         "Lo que pasa en la red en este paso: REGISTER y 200 OK para la cuenta, NTP en hora universal y la zona de la Global Policy para la hora.")],
    4: [(2, "4-l1.svg", "Guardá, aplicá y entrá a Advanced Settings",
         "Lo que pasa en la red en este paso: el INVITE ofrece solo PCMA y PCMU, y la respuesta elige entre esos dos.") ,
        (3, "4-l2.svg", "Revisá el estado en System Status > Dashboard (Trunks)",
         "Lo que pasa en la red en este paso: Rejected es un REGISTER que no llega a nadie o una respuesta con credenciales que no coinciden.")],
    5: [(5, "5-l1.svg", "Revisá cómo prioriza tu central",
         "Lo que pasa en este paso: con List Sorting gana la primera ruta que coincide, con Accuracy First el patrón más parecido.")],
    6: [(4, "6-l1.svg", "Hacé una llamada de prueba y mirá en CDR",
         "Lo que pasa en la red en este paso: el proveedor manda el número en su formato y el CDR lo muestra tal cual; el Strip se calcula con ese.")],
    7: [(1, "7-l1.svg", "Definí horario de oficina y un feriado de prueba",
         "Lo que pasa en este paso: la central compara su hora con Office Time/Holiday; con la zona horaria mal, el destino cambia a la hora equivocada.")],
    8: [(5, "8-l1.svg", "Llamá a la cola desde dos teléfonos a la vez",
         "Lo que pasa en este paso: Least Recent entrega cada llamada al agente libre que hace más que no atiende; con la fila llena, al desborde.")],
    9: [(3, "9-l1.svg", "En la extensión del remoto: Media > NAT activado",
         "Lo que pasa en la red en este paso: con NAT activado la UCM contesta a la IP y el puerto de donde vino el paquete, no a lo que dice el mensaje.")],
    10: [(2, "10-l1.svg", "Hacé una llamada de 20 segundos entre una interna",
          "Lo que pasa en la red en este paso: la captura guarda la señalización y unos 1000 paquetes de audio por sentido en 20 segundos.")],
    11: [(4, "11-l1.svg", "Geo-IP (si la central recibe remotos por internet)",
          "Lo que pasa en la red en este paso: lo que viene de un país no permitido se corta antes de Fail2ban; tu IP va a una lista blanca antes de guardar.")],
    12: [(3, "12-l1.svg", "Timbre y apertura:",
          "Lo que pasa en este paso: el PIN llega como eventos RFC 4733 y el GDS solo mueve la cerradura si la salida está en Open Door.")],
    13: [(4, "13-l1.svg", "Llamá a la línea desde un celular: el teléfono tiene que sonar",
          "Lo que pasa en este paso: la línea recibe el timbre en ráfagas, el celular escucha el tono de llamada y, al atender, se cierra el lazo.")],
    14: [(5, "14-l1.svg", "Descolgá el teléfono de prueba en paralelo con la línea 1",
          "Lo que pasa en este paso: el teléfono en paralelo cierra el lazo; un FXO en uso sin llamadas en Active Calls es la marca de algo en paralelo.")],
    15: [(4, "15-l1.svg", "Probá el corte: llamá desde el celular a una interna",
          "Lo que pasa en este paso: después del corte llegan tonos de ocupado; con Busy Tone Count 4 el FXO1 vuelve a libre en unos cuatro segundos.")],
    16: [(5, "16-l1.svg", "Con la línea libre, detectá la impedancia",
          "Lo que pasa en este paso: con la impedancia mal, parte de tu voz rebota como eco; ACIM lo baja y recién después se tocan las ganancias.")],
    17: [(6, "17-l1.svg", "Desconectá el cable del FXO1 y repetí",
          "Lo que pasa en este paso: sin la línea 1 la ruta prueba el failover, y el celular ve el número de la línea por la que salió.")],
    18: [(3, "18-l1.svg", "Con el teléfono de prueba: tono, llamada desde un celular, timbre",
          "Lo que pasa en este paso: un tono distinto del normal marca una facilidad activa; con la transferencia, las entrantes nunca llegan a la línea.")],
}

man = {}
for lid in range(1, 19):
    e = {"anims": [{"file": f"{lid}-r1.svg", "alt": alt(f"{lid}-r1.svg"), "caption": R[lid]}],
         "steps": [{"step": st, "file": f, "after": a, "alt": alt(f), "caption": c} for st, f, a, c in STEPS[lid]]}
    man[str(lid)] = e
OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(v["anims"]) for v in man.values()), "anims,", sum(len(v["steps"]) for v in man.values()), "steps")
