# Lección 14. Troncal analógica

**Escuchá:** troncal-analogica.mp3 (2 min)

**La idea, en tres líneas**
- Extension/Trunk > Analog Trunks: se eligen los canales FXO y un nombre sin el número real (Antel_Linea1, Antel_Linea2).
- Una troncal por línea cuando cada línea entra a un lugar distinto; varias FXO en una troncal cuando son iguales y se quiere salir por la primera libre (DAHDI Out Line Selection: Ascend, Poll o Descend).
- Antes de entregar: FXO Opermode con el país de la línea y PCMA Override en PCMA (fuera de Norteamérica), con reinicio.

**Impacto:** troncales con nombres que se pueden mostrar, rutas que se arman sin rehacer nada y un Dashboard que el técnico de soporte lee de un vistazo.

**Quién lo dice:** 3 de 3 fuentes coinciden en que la ruta entrante analógica va por troncal porque no llega número llamado (manual del UCM630x, guía de líneas analógicas de Grandstream y la comunidad de Asterisk); en los colores, la guía dice verde para libre y el firmware actual muestra azul.

**Laboratorio** · Foco · 15 min
1. Revisá el hardware analógico. Si en la lista de FXO Opermode no está Uruguay, anotá qué quedó y seguí: la impedancia se afina en la lección del identificador y el audio.
```text
PBX Settings > Interface Settings > Analog Hardware
FXO Opermode: (el país de la línea, si está en la lista)
PCMA Override: PCMA      (pide reinicio)
```
2. Creá una troncal por línea:
```text
Extension/Trunk > Analog Trunks > Create New Analog Trunk
FXO Port: 1         Trunk Name: Antel_Linea1
FXO Port: 2         Trunk Name: Antel_Linea2
```
Si las dos líneas van al mismo destino, la alternativa es una sola troncal:
```text
FXO Port: 1, 2      Trunk Name: Antel_Grupo
DAHDI Out Line Selection: Ascend
```
3. Guardá y aplicá. En System Status > Dashboard mirá Interface Status (FXO1 y FXO2 libres) y Trunks (las troncales como Available).
4. Desconectá el cable del FXO2 y mirá qué estado muestra; volvé a conectarlo.
5. Descolgá el teléfono de prueba en paralelo con la línea 1 y mirá qué muestra el Dashboard para el FXO1. Anotalo: es tu referencia para el diagnóstico de la lección Diagnóstico de línea.
⚠️ PCMA Override reinicia la central: en una obra con el comercio abierto, coordiná el horario.

**Regla para quedarse**
Una troncal por línea si cada línea entra a un lugar distinto; una troncal para varias líneas solo si todas son iguales.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de líneas analógicas de Grandstream: https://documentation.grandstream.com/knowledge-base/manage-analog-lines/
- Manual del UCM630x, troncales analógicas y Analog Hardware: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Por qué en analógico no hay DID: https://community.asterisk.org/t/receiving-calls-from-pstn-s-extension-or-dialed-number/40772
