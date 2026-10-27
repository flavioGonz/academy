# Lección 9. Interno remoto

**Escuchá:** interno-remoto.mp3 (2 min)

**La idea, en tres líneas**
- En la UCM: External Host (IP pública o DDNS), Use IP address in SDP y Local Network Address con las redes internas.
- En el router: reenvío de 5060 UDP y RTP 10000 a 20000 UDP hacia la central, SIP ALG apagado; NAT activo en la extensión.
- En el teléfono remoto, STUN si no registra; el puerto SIP se cambia en la central, no solo en el router.

**Impacto:** el remoto registra y tiene audio en los dos sentidos a la primera visita, sin prueba y error.

**Quién lo dice:** 3 de 3 fuentes coinciden (guía de extensiones remotas, manual del UCM630x, foro de FreePBX); RemoteConnect de Grandstream es la alternativa paga que evita el reenvío de puertos.

**Laboratorio** · Campo · 20 min
Armado: UCM en 192.168.88.0/24 detrás de un router con IP "pública" de laboratorio 203.0.113.10; teléfono detrás de un segundo router hogareño.
1. En la UCM:
```text
PBX Settings > SIP Settings > NAT
External Host: 203.0.113.10
Use IP address in SDP: Sí
Local Network Address: 192.168.88.0/24
```
Guardá y reiniciá cuando lo pida.
2. En el router de la central (ejemplo genérico):
```text
UDP 5060          -> 192.168.88.20:5060
UDP 10000-20000   -> 192.168.88.20:10000-20000
SIP ALG / SIP Helper: desactivado
```
3. En la extensión del remoto: Media > NAT activado.
4. En el teléfono remoto: servidor SIP 203.0.113.10. Si no registra:
```text
Settings > General Settings > STUN Server: stun.ipvideotalk.com
Account > (cuenta) > Network Settings > NAT Traversal: STUN
```
5. Llamada de prueba de 2 minutos en los dos sentidos.
⚠️ Abrir 5060 a internet sin Fail2ban, lista blanca o Geo-IP expone la central a barridos de fuerza bruta (lección 11).

**Regla para quedarse**
External Host sin Local Network Address es medio trabajo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía oficial de extensiones remotas: https://documentation.grandstream.com/knowledge-base/ucm-remote-extensions-guide/
- Por qué reenviar 5555 a 5060 no funciona: https://community.freepbx.org/t/fail2ban-securing-pbx-behind-router-with-port-forwarding/70943
