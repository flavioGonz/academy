# Lección 41. Parque instalado

**Escuchá:** parque-instalado.mp3 (2 min)

**La idea, en tres líneas**
- En tablas de Akuvox pero no en el menú de octubre de 2026: porteros E11, R27, R26, DB01 y E20; monitores C315, C310 e IT83; controladora A092. No hay lista oficial de discontinuados en lo leído, y el C317 no aparece en ninguna página leída.
- Se reconocen por el primer bloque del firmware: `111.` E11, `120.` E20, `27.` R27, `83.` IT83, `115.` C315, `310.` C310, `92.` A092/A094.
- En soporte: los tipo IT83 abren por Open Relay via HTTP y no por la API JSON; en el C315S el relé del monitor se abría con `DoorNum=0`; SR01, patentes y otras funciones piden firmware mínimo que un equipo viejo puede no tener.

**Impacto:** el técnico identifica un equipo viejo en un minuto, lo deja seguro y propone un reemplazo equivalente con datos.

**Quién lo dice:** 3 de 7 fuentes coinciden en separar vigente y parque instalado (menú de productos, guía de firmware de Akuvox, ejemplo de ComfortClick con E11R y C315S); ninguna discrepa.

**Laboratorio** · Campo · 20 min
1. En un equipo viejo, sacá la IP (E11: botón 5 s; C315: `More > System Info > Network`; C310: `Settings > Status > Network`; R27: `*2396#` y `1`).
2. Web: firmware A.B.C.D; identificá el modelo por el bloque A y si el C es 10 o más.
3. Completá:
```text
Equipo  Firmware        Alta seguridad  Falta (SR01, LPR, HTTP nuevo...)  Reemplazo vigente (mismo tipo)
E11R    111.__.__.__    sí / no         ________                          ________
C315S   115.__.__.__    sí / no         ________                          ________
```
4. Para el reemplazo, buscá en el menú un modelo del mismo tipo y verificá credenciales (tabla de métodos) y alimentación (tabla de PoE).
5. Mientras siga instalado: firmware al día, clave propia y VLAN de porteros (lección 11).
⚠️ El E11 es el modelo de las vulnerabilidades publicadas en 2023 (lección 11): si sigue en una pared, va primero en la lista de revisión.

**Regla para quedarse**
Antes de cambiar un equipo viejo, leo su código de firmware y busco su par vigente por función.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Códigos de firmware de modelos vigentes y viejos: https://knowledge.akuvox.com/docs/upgrade-devices
- La pareja E11R y C315S integrada por HTTP: https://www.comfortclick.com/Support/ExampleDetails/Akuvox
- Las vulnerabilidades del E11: https://claroty.com/team82/research/akuvox-smart-intercom-vulnerabilities-leave-privacy-ajar
