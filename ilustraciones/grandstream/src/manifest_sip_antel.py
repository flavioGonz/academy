"""Genera /home/claude/ies-training/ilustraciones/grandstream/manifest-sip-antel.json (lección 19, Troncal SIP de Antel).

No pisa los otros manifests: enriquecer.py combina todos los manifest*.json por campo, y este solo trae la 19.
Al final verifica: cada 'after' de pasos existe una sola vez en el laboratorio de card.md (fuera de bloques de código)
y en la línea del paso que dice 'step'; cada 'after' de teoria_figs existe una sola vez en teoria_md y no en un título;
la teoría tiene 250 a 450 palabras con sus dos subtítulos; cada archivo existe en site2/ilustraciones/grandstream/;
no hay guiones largos.
"""
import json
import re
from pathlib import Path

ROOT = Path("/home/claude/ies-training")
SITE = ROOT / "site2" / "ilustraciones" / "grandstream"
CARD = Path("/home/claude/claudemy/grandstream/class/19-troncal-sip-antel/card.md")
OUT = ROOT / "ilustraciones" / "grandstream" / "manifest-sip-antel.json"

M = {"19": {
    "fig": {"file": "19.svg",
            "alt": "A la izquierda, dentro de una zona punteada que dice red privada de Antel, el servidor SIP 203.0.113.10 y el equipo de Antel con el RJ45 de la troncal, con una nota de que no es internet. Al medio, la UCM6300 en modo Dual: su puerto LAN, resaltado, va al equipo de Antel con 198.51.100.2/30 y sin gateway (LAN1); su puerto WAN va al router del cliente 192.168.88.1 con la IP 192.168.88.20 y el gateway (LAN2), por donde salen teléfonos, web e internet. Arriba a la derecha, lo que entrega Antel: IP de cliente, máscara y gateway, IP del servidor SIP, números y canales del plan, sin usuario ni contraseña. Abajo, tres tarjetas: Peer SIP Trunk con la IP del servidor de Antel en Host Name y sin registro; los OPTIONS de Antel, que la UCM contesta con 200 OK; y el caller ID de la troncal en toda saliente, o Antel la rechaza. Datos de ejemplo.",
            "caption": "La troncal de Antel va por IP, sin usuario ni contraseña, a su propio puerto de la UCM; la red del cliente queda en el otro."},
    "anims": [
        {"file": "19-r1.svg",
         "alt": "Animación en cuatro tiempos. A la izquierda, la red privada de Antel con el servidor SIP 203.0.113.10 y el gateway 198.51.100.1; al medio, la UCM6300 en modo Dual con LAN1 198.51.100.2 hacia Antel, LAN2 192.168.88.20 hacia la red del cliente y su tabla de rutas (203.0.113.0/24 por 198.51.100.1 y LAN; la ruta por defecto por 192.168.88.1 y LAN2); a la derecha, el router del cliente e internet. 1: Antel manda OPTIONS a LAN1 y la UCM contesta 200 OK por el mismo puerto. 2: una saliente al 203.0.113.10 usa la ruta estática y sale por LAN1 hacia Antel, que contesta. 3: sin la ruta estática, el mismo INVITE sigue la ruta por defecto hacia el router del cliente e internet, que no llega a la red privada de Antel: nadie contesta y termina en 408. 4: web, GDMS, actualizaciones e internos remotos salen por LAN2; la troncal nunca toca internet.",
         "caption": "Lo de Antel sale por el puerto de la troncal gracias a la ruta estática; sin ella, el INVITE se va a internet y nadie contesta."}
    ],
    "steps": [
        {"file": "19-paso1.svg", "step": 1, "after": "Juntá la planilla antes de ir a la obra",
         "alt": "Tabla con los datos que se le piden a Antel y un ejemplo de cada uno: número de servicio P00000, plan TSIP8 de 8 simultáneas, IP del cliente 198.51.100.2 con máscara 255.255.255.252, gateway 198.51.100.1, servidor SIP 203.0.113.10 en 5060 UDP, redes a rutear para señalización y audio 203.0.113.0/24 (resaltada), números 2900 1001 a 2900 1008, número por defecto 2900 1001, codecs G.711 y T.38 con DTMF RFC 2833 o inband, y el formato entrante y saliente a confirmar. A la derecha, en ámbar, lo que casi nunca viene: todas las IP desde las que Antel manda señalización y audio, el formato del número de las entrantes y si el servidor contesta los OPTIONS de la central. Una nota: el número de servicio, una P y cinco cifras, es el que pide el 0800 2599 para un reclamo.",
         "caption": "La planilla completa antes de la obra; lo que casi nunca viene se pide por escrito."},
        {"file": "19-paso2.svg", "step": 2, "after": "Pasá la UCM a modo Dual",
         "alt": "La UCM6300 con Method Dual y sus dos puertos: el LAN, en cian, va al equipo de Antel con el RJ45 de la troncal (LAN1); el WAN, en azul, va al switch del cliente en la red 192.168.88.0/24 (LAN2). Debajo, dos tarjetas: LAN1, puerto LAN, troncal, con Static 198.51.100.2 / 255.255.255.252, sin gateway porque a Antel se llega con la ruta estática del paso 3, y nada más colgado de ese puerto; LAN2, puerto WAN, red del cliente, con la IP de la central en la red del cliente, Default Interface LAN2 con su gateway, y teléfonos, web, internet y GDMS por ahí. Un aviso: cambiar el modo reinicia la central, backup antes y en sitio.",
         "caption": "Antel al puerto LAN sin gateway; la red del cliente al WAN, que queda como interfaz por defecto."},
        {"file": "19-l1.svg", "step": 5, "after": "Mirá el estado y el OPTIONS de Antel",
         "alt": "Animación en cuatro tiempos con dos servidores de Antel de ejemplo, 203.0.113.10 y 203.0.113.11, la UCM en LAN1 198.51.100.2, los troncales configurados a la derecha y lo que muestra la captura abajo. 1: OPTIONS desde 203.0.113.10, el Host Name del troncal Antel_Troncal, y 200 OK de la UCM. 2: la UCM manda su OPTIONS de heartbeat cada 60 segundos; si Antel contesta, el Dashboard lo muestra disponible, y si no contesta, conviene apagar el heartbeat. 3: un OPTIONS desde 203.0.113.11, una IP que no está en ningún troncal: la UCM lo rechaza, por ejemplo con 401 o 404. 4: con esa IP en un segundo troncal, Antel_2, y la red de Antel en la Allowlist de Fail2ban, también recibe 200 OK.",
         "caption": "Lo que pasa en la red en este paso: cada OPTIONS de Antel recibe 200 OK solo si viene de una IP que la UCM tiene como troncal."},
        {"file": "19-paso7.svg", "step": 7, "after": "Armá la salida con el plan de Uruguay",
         "alt": "Tabla de patrones de la ruta saliente: _2XXXXXXX fijos de Montevideo y área metropolitana, _4XXXXXXX fijos del interior, _09XXXXXXX celulares con 0 más el número y _0800XXXX sin cargo, los cuatro en la ruta Uruguay; _911 y _10X emergencias (911, 104, 105, 109) sin PIN y con privilegio Internal; _00. internacional en otra ruta con PIN; _090XXXXX, 0900 a 0908 de valor agregado, con PIN o sin ruta. A la derecha: el número sale como se marcó, 8 cifras los fijos y 09 más 7 cifras los celulares; si Antel contesta 404 o 484, no es el formato que espera, se mira en el Request-URI de la captura y se ajusta con Prepend o Strip. Abajo, en rojo: el 911 no se prueba llamando, se revisa que el patrón exista, que no pida PIN y que salga por la troncal de Antel.",
         "caption": "Fijos, celulares, sin cargo y emergencias en una ruta; internacional y valor agregado con PIN."},
        {"file": "19-l2.svg", "step": 8, "after": "Probá como lo entrega Antel",
         "alt": "Animación en tres tiempos con la interna 1003, la UCM y Antel 203.0.113.10; a la derecha, el orden en que la UCM elige el caller ID según su manual: Keep Original CID, troncal con Keep Trunk CID, DOD de la interna, CallerID de la interna, troncal sin Keep Trunk CID y Global Outbound CID. 1: la 1003 llama a un celular de ejemplo y la UCM manda el INVITE con From 1003; Antel lo rechaza y en la captura se ve 403 Forbidden. 2: con Keep Trunk CID en Sí, el From lleva 29001001, Antel contesta 180 y 200 OK y el celular ve 2900 1001. 3: con DOD en la 1003 y Keep Trunk CID en No, el From lleva 29001003 y el celular ve ese número.",
         "caption": "Lo que pasa en la red en este paso: el From de la saliente decide si Antel la acepta."},
    ],
    "concepts": [
        {"name": "Peer SIP Trunk por IP",
         "para_que": "Un proveedor puede reconocer a la central de dos formas: por usuario y contraseña, que es el Register de la lección Troncal registrado, o por la IP desde la que habla. Antel usa la segunda: le asigna a la central una IP fija dentro de su red y acepta lo que llega desde ahí, sin registro.",
         "como": "En la UCM es un Peer SIP Trunk en Extension/Trunk > VoIP Trunks, con la IP del servidor de Antel en Host Name, UDP y sin NAT. La UCM, a su vez, solo trata como troncal lo que llega desde ese Host Name: si Antel usa más de una IP, cada una tiene que estar en un troncal. Para saber si la central está viva, Antel le manda OPTIONS y espera un 200 OK.",
         "ejemplo": "En la instalación de una ferretería en Las Piedras, la captura muestra OPTIONS de Antel cada pocos segundos, todos con su 200 OK desde 198.51.100.2 (datos de ejemplo). Esa captura va a la ficha del cliente como prueba de que la troncal quedó bien."},
        {"name": "Modo Dual y ruta estática",
         "para_que": "La troncal de Antel es una red privada que no tiene salida a internet, y la red del cliente sí. La central necesita estar en las dos a la vez sin mezclar el tráfico: lo de Antel por un lado, lo de internet por el otro, y sin un NAT en el medio que cambie las IP.",
         "como": "En System Settings > Network Settings, Method en Dual: el puerto WAN (LAN2) queda en la red del cliente y es la Default Interface con su gateway; el puerto LAN (LAN1) lleva la IP que dio Antel, sin gateway. En Static Routes, las redes de Antel van por el gateway de Antel e Interface LAN. Lo que se cambia acá reinicia la central: backup antes y en sitio.",
         "ejemplo": "Un técnico configura todo, el troncal figura bien y las salientes dan 408. Faltaba la ruta estática: el INVITE salía por el gateway del cliente hacia internet, que no llega a la red de Antel. Con la ruta `203.0.113.0/24` por `198.51.100.1` (de ejemplo), la llamada sale."},
        {"name": "Caller ID de la troncal",
         "para_que": "Antel solo deja salir llamadas que se presentan con un número de la troncal: es la forma de que nadie use la troncal de una empresa con números ajenos. Si el número no es de la troncal, rechaza la llamada o la saca con el número por defecto del servicio.",
         "como": "La UCM elige el número en este orden: Keep Original CID, el número del troncal con Keep Trunk CID, el DOD de la interna, el CallerID de la interna, el número del troncal sin Keep Trunk CID y el Global Outbound CID. Con Keep Trunk CID en Sí todas salen con el principal; si cada interna tiene número directo, DOD por interna y Keep Trunk CID en No, revisando que ninguna interna salga con su número de interna.",
         "ejemplo": "En una inmobiliaria de Punta Carretas, todas las salientes andan menos las de la recepción, que vuelven rechazadas. En la captura el From dice 1003: la interna tenía cargado su propio CallerID y Keep Trunk CID estaba en No. Con DOD 2900 1003 (de ejemplo), sale bien."},
        {"name": "¿Troncal SIP o líneas por FXO?",
         "para_que": "Muchos clientes tienen las dos opciones a mano: líneas analógicas de Antel, una llamada por línea y sin número llamado (módulo Líneas analógicas por FXO), o la Troncal SIP, con los canales del plan y un número directo por interna. Elegir bien evita pagar líneas de más y también quedarse sin teléfono cuando se corta algo.",
         "como": "La troncal SIP escala por plan, de 8 a 180 llamadas, y entrega DID; depende de la fibra, del equipo de Antel y de la luz, así que la UCM y el equipo de Antel van con UPS. La línea de cobre da una llamada por línea pero no depende de la red del cliente, y en la UCM630x el FXS1 queda conectado al FXO1 si se corta la luz. Lo que hoy marca por la línea (alarma, posnet, fax) se prueba uno por uno antes de dar de baja una línea analógica.",
         "ejemplo": "Una clínica en Pocitos pasa a la troncal SIP para sus 12 internas con número directo y conserva una línea analógica de Antel para el panel de alarma y como respaldo en el FXO1 de la UCM6304A."},
    ],
    "teoria_md": """### Un poco de historia

SIP es la RFC 3261, de junio de 2002: el mismo protocolo con el que los teléfonos hablan con la UCM. Durante años, las empresas uruguayas conectaban la central a Antel con líneas analógicas o con enlaces digitales como el E1. Según Simpletech, un integrador de Montevideo, Antel pasó el núcleo de su red telefónica a IP pero mantuvo esa última milla con equipos que convertían la voz; la Troncal SIP lleva el IP hasta la central del cliente, sin conversiones en el medio.

La página de Antel ofrece planes de 8 a 180 llamadas simultáneas, del TSIP8 al TSIP180, sobre FTTH y fibra dedicada, y los compara con el E1, que tiene una cantidad fija de canales. Las llamadas viajan por una red privada de Antel, no por internet. Y desde el 29 de agosto de 2010 todos los números del país tienen 8 cifras, lo que simplifica las rutas.

### Cómo funciona

No hay registro. En una troncal registrada, la central se presenta con usuario y contraseña. En la de Antel, el proveedor reconoce a la central por la IP fija que le asignó, y la UCM reconoce a Antel porque los mensajes llegan desde el Host Name del troncal. Para saber si la central está viva, Antel le manda OPTIONS, el mensaje de SIP que pregunta qué soporta un equipo, y espera un 200 OK.

Una entrante es un INVITE de Antel con el número llamado en el Request-URI; la UCM lo toma según DID Mode y lo busca en las rutas entrantes. Al atender, la UCM contesta 200 OK con un SDP, y su línea `c=` dice a qué IP mandar el audio: ahí va la IP de la central del lado de Antel. Con Session-Expires de 600 segundos (RFC 4028), uno de los dos lados refresca la sesión a mitad de tiempo.

El problema clásico es el NAT. Un router traduce la IP del paquete pero no la que va dentro del SIP, así que el SDP queda con la IP privada y el audio de Antel no vuelve; un SIP ALG intenta arreglarlo y a veces lo empeora. Por eso conviene la troncal directo a la central: modo Dual, la red del cliente en un puerto, Antel en el otro y una ruta estática hacia las redes de Antel. Sin NAT tampoco hacen falta rport (RFC 3581) ni los keepalives de RFC 5626.

Para salir, Antel mira el From: tiene que ser un número de la troncal. La UCM lo elige por prioridad, de Keep Trunk CID al DOD y al número de la interna.""",
    "teoria_figs": [
        {"file": "19-t1.svg", "after": "dice a qué IP mandar el audio",
         "alt": "Animación en cinco tiempos con tres columnas: Antel con su servidor SIP 203.0.113.10, la UCM en LAN1 198.51.100.2 y la interna 1001. 1: Antel manda OPTIONS desde la IP del Host Name y la UCM contesta 200 OK. 2: llega un INVITE a sip:29001001@198.51.100.2; la ruta entrante _2900100X con By DID y Strip 4 lo lleva a la 1001. 3: la 1001 suena, la UCM pasa el 180 Ringing y, cuando atiende, contesta 200 OK con c=198.51.100.2 en el SDP. 4: ACK, y el audio RTP va y viene por el puerto de la troncal, sin NAT. 5: con Session-Expires de 600 segundos, la sesión se refresca a los 300 con un UPDATE o un re-INVITE; al cortar, Antel manda BYE y la UCM lo pasa a la 1001. Datos de ejemplo.",
         "caption": "Una entrante completa: OPTIONS, INVITE, ruta entrante, SDP con la IP del lado de Antel, RTP y BYE."},
        {"file": "19-t2.svg", "after": "y a veces lo empeora",
         "alt": "Animación en cuatro tiempos con la UCM 192.168.88.20, un router con NAT que sale como 198.51.100.2 y Antel 203.0.113.10; debajo, un paquete con la IP del paquete y la línea c= del SDP. 1: la UCM manda el INVITE con c=192.168.88.20. 2: el router cambia la IP del paquete a 198.51.100.2 pero el SDP sigue con la privada; un ALG o un firewall sin SIP hace lo mismo o lo reescribe mal. 3: Antel manda el audio a 192.168.88.20, que no existe en su red, y se pierde: audio de un lado. 4: con la troncal directo a la central no hay NAT, y con un firewall en el medio se carga External Host 198.51.100.2 y se apaga el ALG: el SDP lleva 198.51.100.2 y el audio vuelve.",
         "caption": "Con NAT en el medio, el SDP queda con la IP privada y el audio de Antel no vuelve."},
    ],
}}

json.dump(M, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- verificación
card = CARD.read_text(encoding="utf-8")
lab = card.split("**Laboratorio**", 1)[1].split("**Regla para quedarse**", 1)[0]
lines, fence, outside = lab.splitlines(), False, []
step_of, cur = {}, None
for ln in lines:
    if ln.strip().startswith("```"):
        fence = not fence
        continue
    if not fence:
        outside.append(ln)
        m = re.match(r"^(\d+)\.\s", ln)
        if m:
            cur = int(m.group(1))
            step_of[ln] = cur
errs = []
for lid, e in M.items():
    for st in e["steps"]:
        hits = [ln for ln in outside if st["after"] in ln]
        if len(hits) != 1:
            errs.append(f"{st['file']}: 'after' aparece {len(hits)} veces fuera de código")
        elif step_of.get(hits[0]) != st["step"]:
            errs.append(f"{st['file']}: 'after' no está en la línea del paso {st['step']}")
        if not 15 <= len(st["after"]) <= 40:
            errs.append(f"{st['file']}: 'after' de {len(st['after'])} caracteres")
    th = e["teoria_md"]
    words = len(re.sub(r"[#`]", "", th).split())
    if not 250 <= words <= 450:
        errs.append(f"teoría de {words} palabras")
    for h in ("### Un poco de historia", "### Cómo funciona"):
        if h not in th:
            errs.append(f"falta {h}")
    for tf in e["teoria_figs"]:
        n = th.count(tf["after"])
        if n != 1 or any(tf["after"] in ln for ln in th.splitlines() if ln.startswith("###")):
            errs.append(f"{tf['file']}: 'after' aparece {n} veces o en un título")
    files = [e["fig"]["file"]] + [a["file"] for a in e["anims"]] + [s["file"] for s in e["steps"]] + [t["file"] for t in e["teoria_figs"]]
    for f in files:
        p = SITE / f
        if f.endswith(".svg") and not p.exists():
            p = SITE / (Path(f).stem + ".webp")
        if not p.exists():
            errs.append(f"no existe {p}")
    print(f"lección {lid}: teoría {words} palabras, {len(e['steps'])} pasos, {len(e['concepts'])} conceptos, {len(e['anims'])} anims, {len(e['teoria_figs'])} figuras de teoría")
txt = json.dumps(M, ensure_ascii=False)
if "—" in txt or "–" in txt:
    errs.append("hay guiones largos")
print("errores:", errs or "ninguno")
