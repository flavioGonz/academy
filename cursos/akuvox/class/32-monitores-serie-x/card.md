# Lección 32. Monitores serie X

**Escuchá:** monitores-serie-x.mp3 (2 min)

**La idea, en tres líneas**
- X933: 7", Android, plástico (guía de selección); 2 relés de 24 V 1 A, 1 RS485, 1 timbre, PoE. X937: 15,6", aluminio, Android 14; 2 relés de 30 V 2 A, 1 RS485, 1 timbre, PoE y 2 RJ45 extra.
- El X937 pide PoE+ 802.3at o fuente de 12 V 2 A; el X933 figura con el grupo de 12 V 1 A. IP en `Settings > System Info > Network`; firmware `933.` o `937.`.
- AKClaw Panel figura en el menú como categoría aparte ("Agentic Panel"); sin ficha leída, no se afirman datos.

**Impacto:** el X937 no se instala en un puerto que no le da energía, y el relé del X933 no recibe una carga que no aguanta.

**Quién lo dice:** 4 de 7 fuentes coinciden en mirar sistema, relés e interfaces (guía de selección, tablas de interfaces, relé y alimentación); ninguna discrepa. Sin ficha propia leída.

**Laboratorio** · Admin · 10 min
1. Para una obra con X937, revisá el puerto del switch:
```text
X937  -> PoE+ 802.3at en el puerto, o fuente 12 V 2 A
X933  -> PoE, o fuente 12 V 1 A
```
2. Completá qué maneja cada relé:
```text
X937 relé 1: ______ (máx. 30 V 2 A)   relé 2: ______
X933 relé 1: ______ (máx. 24 V 1 A)   relé 2: ______
```
3. Si van relés externos por RS485, verificá el firmware mínimo: X933 933.30.13.702, X937 937.30.13.122.
⚠️ Cualquier carga de más de 24 V o 1 A en un X933 va con relé auxiliar.

**Regla para quedarse**
En los X interiores, PoE+ para el grande y 24 V 1 A como techo para el chico.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de selección de monitores: https://www.akuvox.com/productSelectionGuide?cid=4
- Alimentación por modelo (X937 con PoE+): https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
- Interfaces por modelo: https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors
