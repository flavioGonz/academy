# Lección 44. Theme del portero

**Escuchá:** theme-porteros.mp3 (2 min)

**La idea, en tres líneas**
- El theme decide qué ve la visita al llegar. Según la tabla de Akuvox (junio de 2026): S539 y S538 Villa, Building (de fábrica), Office, Multi-factor Authentication y Alphanumeric; X915 y R29 Villa, Building, Office y Alphanumeric; S535 Villa, Building, Speed Dial y QR Code; X912 y S532 Default, Directory, Customized Text y Gate Mode (X912 suma Speed Dial); X916 Intercom, VMS y Directory; E18 Default, QR Code y Speed Dial (E16 suma Custom UI).
- Ruta: `Setting > Key/Display > Theme` en S539, S538, S535, S532, X915, X912 y R29; `Intercom > Key/Display > Theme` en el X916; `Device > LCD > Theme` en E18 y E16. Dentro del theme se elige la página de inicio (íconos, o directo al directorio o al teclado), el nombre de cada tecla y, en Building, hasta 4 idiomas en pantalla.
- Protector con imágenes (y video en S539, S538 y X915 V2.0) para publicidad, fondo, íconos y logo de arranque van en la web. Gate Mode y Parking Lot dependen del área pública de una comunidad en SmartPlus, y el Office del S539 de Smart Access Cloud.

**Impacto:** la visita encuentra a quién llamar en dos o tres toques, en su idioma, y el portero no queda en un theme de nube que en una obra local no muestra nada.

**Quién lo dice:** 8 de 8 páginas leídas, todas de la Knowledge Base de Akuvox, coinciden en el camino; difieren en la lista: la nota de themes de junio da cuatro al R29 y su guía de septiembre de 2026 suma Parking Lot (también en la guía del S539). No encontramos practicantes que lo documenten.

**Laboratorio** · Foco · 20 min
Con un R29 o un X915 en la mesa y su web abierta:
1. Elegí el theme y mirá la pantalla del portero después de cada cambio:
```text
S539 / S538 / S535 / S532 / X915 / X912 / R29 : Setting > Key/Display > Theme
X916                                          : Intercom > Key/Display > Theme
E18 / E16                                     : Device > LCD > Theme
```
2. Probá `Villa`: tres íconos (contacto, PIN y llamar). Después volvé a `Building`.
3. En `Setting > Key/Display > Key In Homepage Of The Building Theme`, cambiá la página de inicio (X915: `Default Page`; R29: `Display Type`) de la de íconos a directorio (`Tenants` o `Contacts`) y después a teclado (`PIN`).
4. En la misma pantalla, renombrá las teclas en español: `Llamar`, `Directorio`, `Código`.
5. En `Language Setting of The Building Theme`: visible, Language 1 español y Language 2 inglés.
6. Protector del R29: `Device > LCD > Standby Interface Display` (Sleep 30 s, Wake Mode `IR Detection`) y `Device > Import/Export > Upload Screensaver Picture` con un JPG de 800x1280 y Play Time de 10 s. En el X915: `Device > LCD > Upload Screensaver`.
7. Prueba de calle: alguien que no conoce el edificio llama a un apartamento. Contá los toques.
⚠️ Gate Mode, Parking Lot y el Office del S539 necesitan la nube; en una obra sin SmartPlus, elegí Villa o Building. Y si la web del equipo muestra otra lista, manda la del firmware que tenés.

**Regla para quedarse**
El theme se elige por quién llega a la puerta, y se prueba con alguien que no conoce el edificio.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Themes por modelo y rutas: https://knowledge.akuvox.com/docs/configure-theme-on-akuvox-door-phone
- Pantalla del R29 (themes, protector, logo, apariencia): https://knowledge.akuvox.com/docs/screen-display
- Pantalla del X915 (Villa, Building, idiomas, fondo): https://knowledge.akuvox.com/docs/screen-display-configuration-1
- Idiomas de pantalla por modelo: https://knowledge.akuvox.com/docs/languages-supported-by-different-models
