# Lección 34. A15 y WR01

**Escuchá:** a15-y-wr01.mp3 (2 min)

**La idea, en tres líneas**
- A15: terminal facial de 4,59" para marco de puerta. PIN, 13,56 MHz, rostro, Bluetooth y QR; PoE 802.3at o 12 V 2 A; borne de 12 V de 500 mA con PoE+ o 1 A con fuente. IP: mantener la pantalla 5 s, PIN o tarjeta de administrador, `Setting > System Info > Network`.
- WR01 (ficha): controlador de relé web de borde, 2 relés y 2 entradas, 20.000 usuarios y 100.000 registros, BLE, pared o riel DIN; WR01-L con LTE. Alimentación AC o DC de 12 a 24 V o PoE 802.3at; borne de 12 V 500 mA.
- El WR01 no tiene lector: según la tabla de métodos, solo Bluetooth. Lee patentes de cámaras desde 1401.30.11.221.

**Impacto:** el marco angosto lleva un A15 y la carga lejos del portero se maneja con un WR01, sin tender cable hasta el portero.

**Quién lo dice:** 8 de 11 fuentes de control de acceso coinciden en el reparto de equipos; del WR01 hay ficha propia leída, del A15 solo las tablas de Akuvox.

**Laboratorio** · Foco · 15 min
1. Montá el WR01 en riel DIN y alimentalo (PoE 802.3at o fuente de 12 o 24 V).
2. Relé 1 a una lámpara de 12 V de banco usando el borne de 12 V (máximo 500 mA); entrada 1 a un pulsador.
3. Sacá la IP con IP Scanner o del DHCP y entrá a la web; cambiá la clave de fábrica.
4. Abrí el relé desde la web y verificá el registro; probá el pulsador.
5. Anotá:
```text
WR01   ubicación ______   relé 1: ______   relé 2: ______
       entrada 1: ______  entrada 2: ______  alimentación: ______
```
6. Si tenés un A15: pantalla 5 s, PIN de administrador, `Setting > System Info > Network`.
⚠️ El WR01 maneja cargas en lugares sin vigilancia: va dentro de un gabinete cerrado y en la VLAN de porteros.

**Regla para quedarse**
Marco angosto, A15; carga lejos del portero, WR01.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ficha del WR01: https://www.akuvox.com/productsDisp?pid=130
- Salida de 12 V de A15 y WR01: https://knowledge.akuvox.com/docs/devices-supporting-12v-power-output
- Acceso al menú del A15: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
