# Lección 9. BabyWare primero

**Escuchá:** babyware-primero.mp3 (2 min)

**La idea, en tres líneas**
- BabyWare conecta local con el cable 307USB (o un CV4USB) al conector serie de la central, o remoto por módulo IP o PCS.
- Pide dos llaves propias: ID de panel en [910] y contraseña de PC en [911] (hexadecimales). Tienen que coincidir con la cuenta en BabyWare.
- El reseteo por botón vuelve todo a fábrica salvo esas dos llaves; y el módulo IP atiende una conexión a la vez.

**Impacto:** tenés una copia de la central antes de tocar nada, y nadie con un cable entra a una central de tu cartera.

**Quién lo dice:** 2 de 4 fuentes sostienen el procedimiento (guía SP+, hilo de IPVM); la guía SP+ dice que BabyWare obliga a cambiar 0000 en la primera conexión, mientras los manuales de IP180 y BlueEye siguen citando 0000 de fábrica. El límite de una conexión sale de un foro de openHAB (su experiencia).

**Laboratorio** · Campo · 15 min
Material: central de banco, cable 307USB, notebook con BabyWare.
1. Conectá el 307USB al conector serie de 4 pines de la central y al USB de la notebook.
2. En la central, cambiá las dos llaves (valores de ejemplo, usá los tuyos):
```text
[ENTER] + código de instalador + [910] + 1A2B     ID de panel (4 dígitos hexa)
[CLEAR] [911] + 3C4D                              contraseña de PC (4 dígitos hexa)
[CLEAR] [CLEAR]                                   sale de programación
```
3. En BabyWare, creá una cuenta nueva con el mismo ID de panel y contraseña de PC, conexión directa por el puerto COM del 307USB.
4. Conectá y leé toda la programación de la central (recepción completa).
5. Guardá la cuenta con el nombre de la obra y la fecha. Esa es tu copia antes de cualquier cambio.
6. Desconectá BabyWare al terminar: si después alguien intenta entrar por el módulo IP, una sesión abierta lo deja afuera.
7. Anotá ID de panel y contraseña de PC en la ficha de la obra.

⚠️ No dejes la notebook conectada al serie con la central en servicio y el gabinete abierto: el tamper de la caja y la sesión abierta son dos alertas para monitoreo.

**Regla para quedarse**
Antes de cambiar nada, copia de la central en BabyWare.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- BabyWare, ID de panel, contraseña de PC y reseteo por botón (guía de instalación SP+): https://www.paradox.com/Downloader/?ID=11662
- MG5050 sin código de instalador y la vía BabyWare (IPVM): https://ipvm.com/forums/video-surveillance/topics/paradox-mg5050-installer-id-issue
- IP150 con una conexión a la vez (foro openHAB): https://community.openhab.org/t/help-build-binding-for-paradox-alarm-panel-with-ip150/1712?page=3
