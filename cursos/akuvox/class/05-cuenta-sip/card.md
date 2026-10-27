# Lección 5. Cuenta SIP

**Escuchá:** cuenta-sip.mp3 (2 min)

**La idea, en tres líneas**
- Con central (UCM, Asterisk/FreePBX, Yeastar, 3CX), portero y monitor se registran como extensiones comunes, una por equipo.
- En Akuvox va en `Account > Basic`: Register Name y Username con la extensión, Password y Server Address.
- Hay dos cuentas; la 1 es la que toma SmartPlus si se activa, así que la central puede ir en la 2.

**Impacto:** el portero hereda todo lo de la central: desvíos, colas, grupos de timbrado y apps.

**Quién lo dice:** 6 de 8 fuentes coinciden (Akuvox, Yeastar, 3CX, Grandstream, FreePBX); ninguna discrepa en el método, solo cambian los menús de cada central.

**Laboratorio** · Foco · 20 min
1. En la central de laboratorio creá dos extensiones con contraseñas largas:
```text
201  Portero calle   clave: Ejemplo-201-Lab!
202  Monitor living  clave: Ejemplo-202-Lab!
```
2. Si el equipo vino de otra obra, reseteo de fábrica antes de empezar.
3. En el portero: `Account > Basic`, cuenta habilitada:
```text
Register Name : 201
Username      : 201
Password      : Ejemplo-201-Lab!
Server Address: 192.168.88.10   (IP de la central)
Port          : 5060
```
4. Lo mismo en el monitor con la 202. Submit en los dos.
5. Verificá el registro en la central. En Asterisk/FreePBX:
```bash
asterisk -rx "pjsip show endpoints"
```
6. Llamá del portero a la 202 (sin asterisco ni prefijos) y atendé.
7. Si dice "Failed to authenticate", revisá la contraseña; si el registro cambia de puerto a cada refresco, desactivá SIP ALG en el router.

**Regla para quedarse**
Una extensión por equipo, anotada en la ficha, y verificación de registro en la central antes de irme de la obra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Registro manual de un Akuvox E16C en una central Yeastar: https://help.yeastar.com/en/p-series-appliance-edition/integrations/akuvox/manually-register-akuvox-intercom-device-with-yeastar-p-series-pbx-system.html
- El R20A que no registraba en FreePBX: https://community.freepbx.org/t/solved-sip-registration-failed-on-doorphone-akuvox-r20a/85457
- Dos cuentas SIP y su orden en Akuvox: https://knowledge.akuvox.com/docs/intercom-call-configuration-8
