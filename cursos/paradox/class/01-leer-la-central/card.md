# Lección 1. Leer la central

**Escuchá:** leer-la-central.mp3 (2 min)

**La idea, en tres líneas**
- Spectra SP/SP+ y Magellan MG/MG+ se programan con ENTER, código de instalador (fábrica 0000) y secciones de tres dígitos.
- EVO192 y EVOHD+ se programan manteniendo el 0, con código de seis dígitos (fábrica 000000) y secciones de cuatro dígitos.
- La línea M (M25) va por PoE y se programa desde BlueEye o software web; el resto del parque sigue siendo SP, MG y EVO.

**Impacto:** abrís el manual correcto a la primera y no perdés la visita probando secuencias de otra familia.

**Quién lo dice:** 5 de 5 fuentes coinciden (guías SP+ y EVOHD+, página de la M25, finmon, TremTech). Son del fabricante, distribuidores o proveedores; no se encontró quien discrepe.

**Laboratorio** · Rápido · 10 min
1. Con la tapa abierta, leé el modelo serigrafiado en la placa (SP5500+, SP6000+, SP7000+, MG5050, EVOHD+, etc.).
2. Ubicá la familia en esta tabla:
```text
Familia       Entrar a programación          Secciones   Instalador de fábrica
SP / SP+      [ENTER] + código               3 dígitos   0000
MG / MG+      [ENTER] + código               3 dígitos   0000
EVO / EVOHD+  mantener [0] + código          4 dígitos   000000
M25           app BlueEye o software web     no aplica   no aplica
```
3. En SP o MG, leé la versión de firmware:
```text
[ENTER] + código de instalador + [980]
[ENTER] para pasar al dígito siguiente (dos pitidos por dígito; tres al terminar)
[CLEAR] para salir
```
4. Anotá en la ficha de la obra: modelo, versión, teclados, módulos de comunicación (IP150, IP180, PCS) y si hay StayD.
5. Si es SP4000 o SP65, marcalo en rojo: su reseteo es distinto (lo vemos en la lección 15).

⚠️ Si el código de instalador no es el de fábrica, no pruebes códigos al azar: la central puede bloquear los teclados y reportarlo a monitoreo. Los códigos de fábrica se cambian el primer día (lección 5).

**Regla para quedarse**
Antes de tocar una sección, sé qué central y qué versión tenés delante.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de instalación SP5500+/SP6000+/SP7000+ (programación, sección 980): https://www.paradox.com/Downloader/?ID=11662
- Guía de instalación EVOHD+ (programación con secciones de cuatro dígitos): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Reseteo manual de SP y MG, incluido SP4000/SP65 (TremTech): https://blog.tremtech.com/blog/manually-resetting-paradox-sp-and-mg-alarm-panels/
- Ficha de la M25 / M25 LTE: https://www.paradox.com/web/product/m25-m25-lte/
