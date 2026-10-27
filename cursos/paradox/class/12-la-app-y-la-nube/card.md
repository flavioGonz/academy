# Lección 12. La app y la nube

**Escuchá:** la-app-y-la-nube.mp3 (2 min)

**La idea, en tres líneas**
- BlueEye reemplaza a Insite Gold; los sitios viejos se agregan con ID de sitio y correo de Swan. No soporta cámaras HD78/HD88.
- Dos caminos: Swan (servidor de Paradox, sitio con suscripción) o IP estática sin Swan (directo al módulo, port forward desde afuera), esta última solo en módulos legado.
- El código de PC que pide BlueEye es el de BabyWare; en MG/SP cada 0 se escribe como A (6089 se ingresa 6A89).

**Impacto:** el cliente sabe qué paga y qué pasa si vence, y el monitoreo no depende de la app.

**Quién lo dice:** 4 de 8 fuentes sostienen Swan como camino por defecto (soporte Paradox, guía BlueEye, manual IP150M, ficha CSD) y 4 de 8 que la IP estática sigue existiendo en legado (soporte Paradox, guía BlueEye, CSD, PAI). Discrepa PAI, que no recomienda Swan por una vulnerabilidad documentada (proyecto que compite con la app oficial).

**Laboratorio** · Campo · 15 min
Material: central de banco con IP150+ o IP180 en internet, teléfono con BlueEye, cuenta de instalador de paradox.com aprobada por el distribuidor.
1. En BlueEye: Menú, entorno instalador, "My Other Paradox Systems", login con la cuenta de instalador.
2. Si el sitio no existe: tres puntos, "Create Swan System", número de serie de la central, nombre de sitio y correo. Requiere un módulo conectado a la central y a internet.
3. Entrá al sitio con el código de PC (el de BabyWare; en MG/SP, 0 se escribe A).
4. Abrí los detalles del sitio y anotá: días de suscripción, fecha de renovación, tipo y firmware de central y módulo.
5. Solo módulos legado y si el cliente no quiere suscripción: en la app, +, tres puntos, "Use Static IP without Swan", buscar el IP150/+ y cargar IP local y puerto.
6. Completá la ficha:
```text
Sitio Swan: ID ______  correo ______  vence ______  paga ______
Conexión app: Swan / IP estática (local) / IP estática (port forward)
Monitoreo: canal ______  receptora ______  (independiente de la app)
```
⚠️ Con IP150 de firmware 1.xx o 4.0.4, la IP estática exige la contraseña de fábrica del módulo: un port forward ahí deja el módulo accesible con una clave pública. Evitalo o actualizá antes.

**Regla para quedarse**
Antes de vender la app, explicá quién paga la suscripción y qué pasa si vence.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- No conecto a mi sitio Swan: BlueEye, reinicio y migración desde Insite Gold (soporte Paradox): https://support.paradox.com/portal/en/kb/articles/i-cannot-connect-to-my-site-what-should-i-do
- Sitio por IP estática sin Swan (soporte Paradox): https://support.paradox.com/portal/en/kb/articles/how-can-i-add-a-static-ip-site-in-blueeye
- Menú instalador de BlueEye V2.0: sitios, código de PC, detalles y Swan: https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Software/BlueEye/BlueEye_Installer_Menu_v2.0%20.pdf
- La voz en contra de Swan (PAI): https://www.mintlify.com/ParadoxAlarmInterface/pai/connection/ip150
