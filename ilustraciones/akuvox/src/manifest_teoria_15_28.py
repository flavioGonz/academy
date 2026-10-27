#!/usr/bin/env python3
"""Arma manifest-teoria-15-28.json (solo teoria_figs) y valida anclas contra el teoria_md combinado."""
import glob, json, re

D = "/home/claude/ies-training/ilustraciones/akuvox/"
F = {
 "15": ("se mira el firmware del portero",
        "Animación en cuatro tiempos. 1: en la pantalla de monitoreo del portón, tocás la tecla Portón del monitor, sin llamada abierta. 2: el monitor arma un GET a /fcgi/OpenDoor con usuario, clave y DoorNum, y lo manda directo al portero 192.168.88.22 por la VLAN de porteros, sin central. 3: el portero verifica la credencial y dispara el relé indicado: DoorNum=1 es el relé A y el portón abre; el relé B queda en reposo. 4: con alta seguridad (tercer bloque del firmware 10 o más y el modo encendido), un pedido con la URL vieja /fcgi/do y usuario y clave en la consulta queda rechazado.",
        "Seguí el GET desde la tecla hasta el relé A, y mirá qué pasa con la URL vieja."),
 "16": ("ningún par de esos cables alimenta la cerradura",
        "Animación en cuatro tiempos. Del lado de la calle está el portero; adentro, el SR01, la cerradura y su fuente, unidos al portero solo por el bus RS485. 1: llega al portero un pedido HTTP con DoorNum=SB. 2: el portero manda la orden por RS485; el SR01 cierra su contacto y la cerradura libera durante el Hold Delay de 5 segundos, con Trigger Delay 0. 3: alguien arranca el frente y puentea los cables. 4: solo hay un bus de datos, ningún par alimenta la cerradura y la puerta sigue cerrada.",
        "El frente solo manda datos: aunque lo rompan y puenteen, la cerradura no recibe energía."),
 "17": ("Esa línea es la prueba de que el portero avisó",
        "Animación en cuatro tiempos. 1: se dispara el relé A y el portero 192.168.88.21 toma la URL de Relay A Triggered, http://192.168.88.10:8000/relaytrigger=$relay1status. 2: reemplaza $relay1status por 1 y arma http://192.168.88.10:8000/relaytrigger=1. 3: manda el GET a la PC de laboratorio con python3 -m http.server; responde 404, pero la terminal imprime la línea GET /relaytrigger=1. 4: al cerrarse el relé A, la URL de Relay A Closed llega como GET /relayclose=0.",
        "Mirá cómo la variable se convierte en 1 o 0 antes de salir, y la línea que queda en la terminal."),
 "18": ("y lo manda en un segundo pedido. La clave no viaja",
        "Animación en cuatro tiempos con dos diagramas de secuencia entre curl y el portero. 1: con Basic, el GET lleva Authorization: Basic con usuario:clave en Base64 y el portero abre en un solo pedido. 2: quien captura el tráfico decodifica el Base64 y lee curl-lab:Ejemplo-Curl-2026. 3: con Digest, el primer GET recibe un 401 con un desafío, el nonce. 4: el cliente calcula un resumen con la clave, la ruta y el nonce y lo manda en un segundo GET; el portero abre y la clave no viaja.",
        "Basic resuelve en un pedido y deja la clave a la vista; Digest necesita dos, pero la clave no viaja."),
 "19": ("por eso la planilla se completa mirando la web del equipo",
        "Animación en cuatro tiempos. A la izquierda, la web del equipo muestra el firmware; a la derecha, la planilla del catálogo. 1: 29.x.y.z empieza con 29, el código del R29, serie R. 2: 915.x.y.z es el X915, serie X. 3: 320.x.y.z es el R20 versión 5, serie R. 4: la planilla queda completa; la etiqueta da el nombre comercial y el primer bloque del firmware da el modelo, con el que se buscan alimentación, relé y 12 V en las tablas de la Knowledge Base.",
        "El primer bloque del firmware alcanza para ubicar el modelo en la planilla."),
 "20": ("no alcanza con que diga PoE",
        "Animación en cuatro tiempos entre un switch PoE (PSE) y un portero S539 (PD) con un solo cable. 1: el switch detecta si hay un equipo PoE y el portero responde con su firma. 2: el switch pregunta la clase, el portero pide PoE+ (802.3at) y recién entonces llega la energía. 3: con un puerto 802.3at hay hasta 25,5 W en el equipo y el S539 arranca y anda. 4: con un puerto solo af hay unos 12,95 W; al subir el consumo (pantalla, cámara, lectores) pasa el límite y el portero puede no arrancar o reiniciarse. La barra de consumo es un esquema sin valores.",
        "Primero detecta, después clasifica, después da energía; y el límite del puerto manda."),
 "21": ("el lazo hace que el audio llegue directo al audífono",
        "Animación en cuatro tiempos. 1: el portero S535 o S532 con lazo de inducción recibe la voz de la llamada y la saca por el parlante. 2: en la vereda, esa voz llega al visitante con audífono mezclada con el ruido de la calle. 3: el lazo manda la misma voz como campo magnético alrededor del portero. 4: la telebobina del audífono toma ese campo directo: por el aire llegan voz y ruido, por el lazo solo la voz.",
        "Por el aire llegan voz y ruido; por el lazo, solo la voz a la telebobina."),
 "22": ("El R29 publica IK06; el X915 V2.0, IK10.",
        "Animación en cuatro tiempos. A la izquierda el código IP (IEC 60529), a la derecha el IK (IEC 62262). 1: primer dígito del IP, sólidos: 6 es hermético al polvo, igual en IP65 e IP66. 2: segundo dígito, agua: 5 resiste chorros de agua. 3: 6 resiste chorros potentes; entre IP65 e IP66 cambia la fuerza del agua. 4: el IK va de 00 a 10 y mide la energía de impacto: IK06 es 1 joule (R29) e IK10, 20 joules (X915 V2.0).",
        "Cada dígito del IP es una prueba distinta; el IK es una escala de golpe."),
 "23": ("o se pasa la cerradura a fuente propia",
        "Animación en cuatro tiempos. A la izquierda, un X910 que da 12 V por el relé a una cerradura con un tester en paralelo; a la derecha, la tensión en la cerradura en el tiempo. 1: en reposo no circula corriente y el tester marca 12 V. 2: al abrir, la cerradura pide corriente a la alimentación del portero. 3: con alimentación justa (X910 con PoE af) la tensión cae durante la apertura. 4: con PoE+ o fuente de 12 V 2 A la tensión se sostiene. El gráfico es un esquema sin valores.",
        "En vacío todo marca 12 V: la caída aparece recién cuando la cerradura pide corriente."),
 "24": ("el R29 abre leyendo patentes de cámaras Hikvision y Dahua",
        "Animación en cuatro tiempos. 1: llega un auto y una cámara de patentes Hikvision o Dahua lee la patente. 2: la cámara manda la lectura al R29 por la HTTP API. 3: con firmware 29.30.10.745 o más, el R29 abre y su relé levanta la barrera. 4: con un firmware anterior esa función no está y la barrera no se mueve. Abajo, el firmware se lee en Status > Basic > Product Information y el primer bloque, 29, es el código del R29.",
        "La misma cámara y el mismo R29: lo que cambia es el firmware."),
 "25": ("la cerradura no depende del volumen",
        "Animación en cuatro tiempos. 1: un R25 con PoE da 12 V por el relé a una cerradura de banco, hasta 400 mA, con firmware 25.30.10.11 o más. 2: Akuvox avisa que esa salida queda afectada por el volumen: al mover el volumen, se mueve la aguja de tensión en la cerradura. 3: se mide durante la apertura, con la carga conectada, con volumen bajo y alto. 4: en obra, fuente propia para la cerradura y el relé como contacto seco; al mover el volumen la aguja no cambia. El medidor es un esquema sin valores.",
        "Con PoE la salida de 12 V del R25 sigue al volumen; con fuente propia, no."),
 "26": ("R20K-L con PIN y solo 13,56 MHz",
        "Animación en cuatro tiempos. 1: la tarjeta de 125 kHz, tipo EM o HID Prox, es simple y fácil de copiar. 2: la de 13,56 MHz, ISO 14443 como MIFARE, permite cifrado y más datos. 3: el R20A lee las dos frecuencias y abre con cualquiera. 4: el R20K-L lee solo 13,56 MHz: con la de 125 kHz no lee, con la de 13,56 MHz abre.",
        "Antes de prometer una tarjeta, mirá qué frecuencia lee ese R20."),
 "27": ("En un electroimán, diodo en antiparalelo",
        "Animación en cuatro tiempos con dos circuitos: a la izquierda una cerradura fail-secure en COM y NO; a la derecha un electroimán fail-safe en COM y NC con diodo en antiparalelo; en los dos, el positivo de la fuente de 12 V va a COM. 1: el relé del E16C o E18C es un contacto seco, no aporta energía. 2: en reposo COM toca NC: la cerradura de NO queda sin energía y trabada, el electroimán de NC tiene energía y traba. 3: el relé actúa y COM pasa a NO: la fail-secure recibe energía y el electroimán la pierde; las dos liberan. 4: sin energía en la fuente, la fail-secure queda trabada y la fail-safe libera.",
        "El relé solo une COM con NO o con NC: la energía la pone siempre la fuente."),
 "28": ("devuelve un archivo para desbloquear",
        "Animación en cuatro tiempos. 1: un E12 o E13S, de un botón y sin pantalla, con la clave web perdida: la web no deja entrar. 2: caminos 1 y 2: SmartPlus, o PC Manager desde una PC en la misma LAN. 3: camino 3: se exporta la llave del equipo con la herramienta y se manda a soporte de Akuvox. 4: soporte devuelve un archivo para desbloquear, que vuelve al portero. Por eso la clave web se cambia y se documenta en la primera visita.",
        "Ningún camino es rápido: la clave se documenta el primer día."),
}

M = {}
for f in sorted(glob.glob(D + "manifest*.json")):
    if "manifest-teoria" in f:
        continue
    for k, v in json.load(open(f)).items():
        if isinstance(v, dict):
            M.setdefault(k, {}).update(v)
out, bad = {}, []
for lid, (after, alt, cap) in F.items():
    md = M[lid]["teoria_md"]
    n = md.count(after)
    line = next((l for l in md.splitlines() if after in l), "")
    if n != 1 or line.startswith("#") or not (15 <= len(after) <= 60):
        bad.append((lid, n, len(after), line[:40]))
    out[lid] = {"teoria_figs": [{"file": f"{lid}-t1.svg", "after": after, "alt": alt, "caption": cap}]}
json.dump(out, open(D + "manifest-teoria-15-28.json", "w"), ensure_ascii=False, indent=1)
print("problemas:", bad or "ninguno")
