# Lección 36. Ascensor EC33

**Escuchá:** ascensor-ec33.mp3 (2 min)

**La idea, en tres líneas**
- EC33 (ficha): controlador IP de ascensor, 32 relés ampliables a 64, Wiegand 26/34, 20.000 tarjetas y 100.000 registros, TCP/IP y RS485. PoE 802.3at o 100 a 240 VAC; relé 30 V 3 A. Se integra con todos los porteros y terminales Akuvox salvo A094 y E20.
- Dos cableados: directo al piso (relé en paralelo con el botón del piso) o liberar botones para elegir (relé en serie con el común o la línea de autorización).
- Configuración por HTTP: en el EC33, `Device > Relay > Open Relay via HTTP` con usuario propio; en el terminal, `Device > Lift Control`, tipo Akuvox, IP, puerto y credenciales. Dos EC33 posibles (desbloqueo y llamado); `Floor Starts From` y `Ground Floor` para subsuelos.

**Impacto:** cada residente llega solo a su piso, y el ascensorista recibe un esquema claro de paralelo o serie.

**Quién lo dice:** 1 de 11 fuentes de control de acceso explica el cableado (la guía de Akuvox); la ficha del EC33 aporta los números. Ninguna discrepa, pero la evidencia es del fabricante.

**Laboratorio** · Foco · 20 min
1. EC33 en la mesa: `Device > Relay`, habilitá `Open Relay via HTTP`, usuario `ec33-lab`, clave `Ejemplo-Lift-2026`.
2. Terminal (A08 o portero): `Device > Lift Control`, `Lift Control List = Akuvox`:
```text
Server 1 (Unlock) IP : 192.168.88.40   puerto: el que use el EC33
Usuario / clave      : ec33-lab / Ejemplo-Lift-2026
Floor Starts From    : -1 (si hay un subsuelo)
Device Location      : planta baja
```
3. `Directory > User`: un usuario con tarjeta y permiso al piso 3.
4. En el relé del piso 3 del EC33, una lámpara de banco; pasá la tarjeta y verificá que solo ese relé actúe.
5. Dibujá para el ascensorista qué escenario usás:
```text
Directo al piso   -> relé EC33 en PARALELO con el botón del piso
Elegir piso       -> relé EC33 en SERIE con el común o la línea de autorización
```
⚠️ En el ascensor real, el cableado lo hace o lo autoriza la empresa de mantenimiento del ascensor.

**Regla para quedarse**
Antes de tocar el ascensor, acuerdo con el ascensorista si es paralelo o serie.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Escenarios, cableado y configuración del EC33: https://knowledge.akuvox.com/docs/configure-lift-control-1
- Ficha del EC33: https://www.akuvox.com/productsDisp?pid=83
