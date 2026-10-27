# Lección 2. Leer el firmware

**Escuchá:** leer-firmware.mp3 (2 min)

**La idea, en tres líneas**
- El firmware Akuvox se lee A.B.C.D: modelo, OEM, rama y versión. Ejemplo: `216.30.10.121` es un E16 V2, logo Akuvox, rama 10.
- Varios modelos tienen dos o tres versiones de hardware y cada una lleva su archivo; la etiqueta del R20A engaña (V3.0 es hardware 2).
- Una rama C de 10 o más indica el modo de alta seguridad, que cambia herramientas y comandos.

**Impacto:** cero porteros brickeados por subir el archivo de otro hardware, y tickets que soporte no rebota por firmware viejo.

**Quién lo dice:** 2 de 3 fuentes coinciden (Knowledge Base y portal de soporte de Akuvox); Yeastar suma versiones mínimas para autoprovisión. Nadie discrepa.

**Laboratorio** · Admin · 15 min
1. En dos equipos, abrí `Status > Basic > Product Information` y anotá firmware y hardware.
2. Decodificá cada número con esta tabla parcial de la documentación de Akuvox:
```text
A (modelo): 29=R29  915=X915  12=E12  216=E16 V2  416=E16 V3  316=C316  115=C315
            20=R20  220=R20 V2  320=R20 V3
B (OEM):    30 = logo Akuvox    31 = sin logo
C (rama):   10 o más = rama con modo de alta seguridad
D:          mayor = más nuevo (mismo modelo, OEM y rama)
```
3. Exportá la configuración del equipo como backup (sección de backup o upgrade avanzado de la web).
4. Bajá el firmware de la Knowledge Base, sección Firmware & Tool: `.rom` para equipos Linux, `.zip` para Android.
5. Subilo en `System > Basic > Select File > Upgrade` y esperá sin cerrar ni refrescar la pestaña.
6. Verificá la versión nueva y anotala en la ficha.
⚠️ Antes de actualizar, backup. Siempre. En producción, actualizá fuera de horario y con alguien del lado de la puerta.

**Regla para quedarse**
Modelo, versión de hardware y rama antes de bajar un archivo; backup antes de subirlo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo leer versiones y actualizar: https://knowledge.akuvox.com/docs/upgrade-devices
- Qué pide soporte antes de abrir un ticket: https://ticket.akuvox.com/support/solutions/articles/48001200817-read-first-how-to-provide-information-to-effectively-resolve-a-technical-issue-on-akuvox-intercom-
