# Lección 3. Resistencia al final

**Escuchá:** resistencia-al-final.mp3 (2 min)

**La idea, en tres líneas**
- En Paradox la resistencia de fin de línea (EOL) es de 1 kΩ; en las SP+ se activa en la sección [706] opción 2 y aplica a todas las zonas de la central.
- ATZ duplica la entrada (un detector con 1 kΩ y otro con 2,2 kΩ en el dibujo de la guía EVOHD+); en la serie plus solo la SP6000+ lo admite; se activa en [705] opción 1.
- Las zonas de fuego son normalmente abiertas con EOL y no se pueden anular; el tamper se configura en [705] opciones 3, 4 y 5.

**Impacto:** un cable cortado o en corto aparece como falla en el teclado, en vez de una zona que nunca dispara.

**Quién lo dice:** 3 de 4 fuentes coinciden en EOL de 1 kΩ (guías SP+ y EVOHD+, TremTech en el concepto); TremTech da valores de DSC (5,6 kΩ), que no aplican a Paradox. ATZ: 2 de 4 (las dos guías oficiales).

**Laboratorio** · Foco · 20 min
Material: central de banco (idealmente SP6000+ o EVO), tester, resistencias de 1 kΩ y 2,2 kΩ, dos contactos magnéticos.
1. Medí cada resistencia con el tester antes de usarla y anotá el valor real.
2. Zona simple con EOL: cableá un contacto con la resistencia de 1 kΩ en el extremo del detector, siguiendo la figura "Single Zone Input Connections" de la guía.
3. Activá EOL para toda la central:
```text
[ENTER] + código de instalador + [706]
[2]           enciende la opción 2 (EOL)
[ENTER]       guarda y pasa a la sección siguiente
[CLEAR]       sale
```
4. Zona doble (solo SP6000+ o EVO): cableá dos contactos en el mismo par según la figura "Double Zone Connections" (1 kΩ y 2,2 kΩ) y activá ATZ:
```text
[ENTER] + código de instalador + [705]
[1]           ATZ encendido   ([2] elige paralelo en lugar de serie)
[ENTER]
```
5. Abrí cada contacto por separado y anotá en la planilla qué número de zona marca el teclado.
6. Hacé un cortocircuito en el par con un puente y mirá la pantalla de fallas (TBL, grupo 5: tamper y cableado de zona).
7. Escribí en la tapa del gabinete: "EOL 1k: sí/no. ATZ: sí/no".

⚠️ Activar EOL en una central instalada con zonas sin resistencia pone todas las zonas en falla. Hacelo en banco o con todo el cableado ya preparado.

**Regla para quedarse**
Una central, un criterio de resistencia, anotado en la tapa.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- EOL, ATZ, tamper y zonas de fuego (guía SP+, secciones 705 y 706): https://www.paradox.com/Downloader/?ID=11662
- Dibujos de conexión simple y doble con 1 kΩ y 2,2 kΩ (guía EVOHD+): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- NC sin EOL, EOL simple y doble EOL, concepto general (TremTech): https://blog.tremtech.com/blog/how-to-wire-security-alarm-zones/
