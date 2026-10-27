# Lección 3. Lazo LSN

**Escuchá:** lazo-lsn.mp3 (2 min)

**La idea, en tres líneas**
- LSN improved admite hasta 254 elementos por módulo de lazo; con un solo elemento LSN classic, el lazo baja a 127 y se pierden los T-tap.
- LSN 0300 A: 300 mA y hasta 1600 m. LSN 1500 A: hasta 1500 mA (con elementos improved) y hasta 3000 m.
- Llaves rotativas: 000 automático (de fábrica, sin T-tap), 001 a 254 manual (permite T-tap), CL 0 0 classic. Con dirección manual se marca T-tap en FSP-5000-RPS sea cual sea la topología.

**Impacto:** ampliaciones sin sorpresas de capacidad y lazos que cualquier técnico puede encontrar en el plano.

**Quién lo dice:** 2 de 2 fuentes coinciden (System manual AVENAR y guía de operación del AVENAR detector 4000); es regla del fabricante, sin discrepancias.

**Laboratorio** · Foco · 15 min
Material: panel AVENAR o FPA de banco, un LSN 0300 A, tres detectores FAP-425-O-R con bases, laptop con FSP-5000-RPS.
1. Poné las tres perillas de cada detector en `000` y cablealos en lazo (a y b de salida y retorno).
2. En RPS, lanzá la autodetección del lazo y anotá la dirección que el panel asignó a cada detector.
3. Desenergizá el lazo y cambiá las perillas a:
```text
Detector 1: 0 0 1
Detector 2: 0 0 2
Detector 3: 0 0 3
(centenas a la izquierda, decenas al centro, unidades a la derecha)
```
4. En la configuración del lazo en RPS, marcá T-tap y volvé a autodetectar.
5. Compará las dos tablas: automático numera por orden de cable; manual respeta lo que pusiste.
⚠️ Una dirección mayor a 254 no está permitida, y mezclar automático con manual en el mismo lazo no funciona: con manual, todos del 1 al 254.

**Regla para quedarse**
Lazo con T-tap: todo en dirección manual, marcado en RPS y anotado en el plano.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Límites de LSN, llaves rotativas y topologías (System manual AVENAR): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- Direccionamiento y prueba del AVENAR detector 4000: https://armosystems.ru/upload/iblock/a58/a58a375f59a20cf60064da272d2b6fd9.pdf
