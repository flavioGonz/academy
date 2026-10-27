# Lección 6. Cada DID

**Escuchá:** cada-did.mp3 (2 min)

**La idea, en tres líneas**
- Una sola ruta entrante con patrón que agrupa los DIDs, destino ByDID y Strip, en lugar de una ruta por número.
- DID Mode del troncal define si el número llamado se lee de la Request-line o del To.
- El Strip se calcula con el número exacto que manda el proveedor, mirado en el CDR o en una captura.

**Impacto:** diez o cien números directos se mantienen con un patrón, y las entrantes que "no matchean" se resuelven mirando un dato.

**Quién lo dice:** 2 de 2 fuentes oficiales coinciden (guía de troncales SIP y manual del UCM630x); sin discrepancias. Evidencia delgada en cantidad.

**Laboratorio** · Rápido · 10 min
1. Creá la ruta entrante sobre tu troncal de prueba (números de ejemplo):
```text
Extension/Trunk > Inbound Routes > (elegí el troncal) > Add
Pattern: _2900XXXX
Default Destination: By DID
Strip: 4
```
Con esto, una llamada a 29001007 suena en la interna 1007.
2. En el troncal, revisá de dónde lee el DID:
```text
Extension/Trunk > VoIP Trunks > (troncal) > Advanced Settings > DID Mode: Request-line | To-header
```
3. Calculá el Strip para tres formatos del mismo número y anotalo (cada formato necesita además su propio patrón):
```text
29001007        -> Strip 4
59829001007     -> Strip 7
+59829001007    -> el + cuenta como carácter: Strip 8
```
4. Hacé una llamada de prueba y mirá en CDR qué número llegó realmente.
5. Opcional: agregá una condición de horario fuera de oficina con destino buzón o IVR.

**Regla para quedarse**
El Strip se calcula con el número que llega en la primera llamada de prueba, no con el que figura en la factura.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ejemplo oficial de DID con ByDID y Strip: https://documentation.grandstream.com/knowledge-base/sip-trunks-guide/
- Rutas entrantes, horarios y lista negra: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
