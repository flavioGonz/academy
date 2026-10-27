# Lección 3. Licencia sin sorpresas

**Escuchá:** licencia-sin-sorpresas.mp3 (2 min)

**La idea, en tres líneas**
- Primero una licencia base, después las expansiones (cámaras, puertas, módulos). Solo el usuario admin activa, actualiza o desactiva.
- Online si el SYS tiene internet; offline con archivo de pedido (ActivationRequestFile.bin) y de respuesta (ActivationResponseFile.bin) dentro de las 24 horas.
- La hora del servidor importa: corrida más de 24 h, la activación offline falla; modificada, aparece el error 1114.

**Impacto:** activaciones a la primera y menos tickets al soporte del fabricante.

**Quién lo dice:** 2 de 5 fuentes de licenciamiento lo explican así (Quick Start y manual del Web Client, ambos de Hikvision); los códigos de error salen solo del FAQ V2.5.500. No se encontró quien discrepe. Nada de esto se saltea ni se evade: la licencia es la que vende el canal oficial.

**Laboratorio** · Admin · 15 min
1. En el SYS de laboratorio, revisá hora y sincronización:
```powershell
w32tm /query /status
Get-Date
```
2. Entrá al Web Client (en el navegador, 192.168.88.10) como admin. En la página de inicio: Activate > Offline Activation.
3. Cargá el código de activación (16 o 32 caracteres, sin guiones), aceptá el acuerdo y elegí el entorno: Physical Machine, AWS o Azure.
4. Clic una sola vez en Generate Request File. Guardá el .bin en un pendrive.
5. En una PC con internet, entrá a kms.hikvision.com, sección de activación, subí el pedido y bajá la respuesta. Importala y Activate. Cargá el email del admin.
6. Armá la ficha de licencia de la obra:
```text
Obra:            Ejemplo 01
Servidor SYS:    192.168.88.10 (físico / VM)
Licencia base:   código ****-****  activada el __/__/____ por ____
Expansiones:     cámaras __  puertas __  módulos __
Email del admin: soporte@ejemplo.com
```
Errores a mano: 1103 sin internet o servidor de licencias caído · 1105 respuesta que no corresponde · 1108 código usado en otro SYS · 1113 expansión sin base · 1114 hora modificada · 1116 más recursos que los licenciados.

⚠️ Con un código real, el paso 5 lo ata a ese servidor: en laboratorio, frená en el paso 4.

**Regla para quedarse**
Base primero, hora en hora, y la ficha de licencia en la carpeta de la obra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Activación offline paso a paso (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5B61A8EA-30BC-45DB-9102-A17602B8E976.html
- Errores 1103 a 1116 y licencia que no toma efecto (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
