# Lección 1. Primer acceso

**Escuchá:** primer-acceso.mp3 (2 min)

**La idea, en tres líneas**
- Cada familia Akuvox muestra su IP a su manera: voz, pantalla, código en el teclado o IP Scanner.
- Con la IP se entra por navegador; la web de fábrica es admin / admin en toda la línea.
- El PIN de sistema del E16 cambió con el firmware: `admin` en versiones viejas, `Admin321` en las nuevas.

**Impacto:** la primera media hora de cada obra baja a cinco minutos y ningún equipo queda con la clave publicada en internet.

**Quién lo dice:** 3 de 3 fuentes coinciden en "primero la IP, después la web" (Akuvox, Yeastar, Grandstream); ninguna discrepa, pero solo los investigadores de seguridad insisten en cambiar la clave el primer día.

**Laboratorio** · Rápido · 10 min
1. Conectá un portero y un monitor a un switch con DHCP del rango 192.168.88.0/24.
2. Sacá la IP del portero por el método de su modelo:
```text
R20A / E12 / E13 / X910 : mantener el botón de llamada ~5 s (la dice en voz alta)
R20K / R25K             : marcar *3258*
E16 / E18               : mantener la pantalla ~5 s, PIN de sistema (admin o Admin321 según firmware)
R29 / X915              : marcar 9999, luego 3888, System Info
```
3. Sacá la IP del monitor en pantalla:
```text
C316 / C319 / S567 : Settings > System Info > Network
C315               : More > System Info > Network
```
4. Confirmá las dos IP con el IP Scanner de Akuvox (Windows de 64 bits; pausá el firewall solo mientras escanea).
5. Abrí `192.168.88.X` en el navegador, entrá con admin / admin y cambiá la clave web por una propia (ejemplo de laboratorio: `Lab-Portero-2026!`).
6. Anotá modelo, IP, MAC y clave nueva en la ficha del equipo.
⚠️ En producción, el firewall de la PC se vuelve a activar apenas termina el escaneo.

**Regla para quedarse**
La IP se le pide al equipo, no se adivina, y la clave de fábrica no sobrevive a la primera visita.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo sacar la IP en cada modelo Akuvox: https://knowledge.akuvox.com/docs/before-entering-device-web-interface
- El E12S anunciando su IP en una integración con Grandstream: https://documentation.grandstream.com/knowledge-base/wp8x6-access-control-systems-configuration-guide/
- Por qué la clave por defecto publicada es un problema: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
