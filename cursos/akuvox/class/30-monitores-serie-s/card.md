# Lección 30. Monitores serie S

**Escuchá:** monitores-serie-s.mp3 (2 min)

**La idea, en tres líneas**
- S562 7" Linux, S563 8" Android, S567 10" Android (plástico y PoE según la guía de selección); S565 está en el menú pero no en la guía, así que tamaño y sistema no se afirman; S560 es el de auricular.
- S562, S563, S565 y S567: 1 RS485, 1 relé, 1 entrada de timbre; S562, S563 y S565 suman un RJ45 extra. Relé 30 V 2 A en S563, S565 y S567, y 30 V 1 A en el S562. El S560 no tiene RS485, relé ni timbre.
- IP: S562, S563 y S567 en `Settings > System Info > Network`; S565 en `More > Settings > System Info > Network`; S560 manteniendo `#` 5 s. S567: PoE 802.3af o 12 V 1,5 A.

**Impacto:** el relé del monitor se usa dentro de su capacidad y el S560 no se vende para algo que no puede hacer.

**Quién lo dice:** 4 de 7 fuentes coinciden en elegir el monitor por sistema, relés e interfaces (guía de selección, tablas de interfaces, relé y alimentación); ninguna discrepa. Sin ficha propia leída de los monitores.

**Laboratorio** · Foco · 15 min
1. Sacá la IP por el menú de tu modelo (o `#` 5 s en el S560) y entrá a la web.
2. `Status`: firmware `562.`, `563.`, `565.` o `567.`; anotalo.
3. Completá:
```text
Modelo  RS485  Relé (carga)   Timbre  RJ45 extra
S562    1      1 (30 V 1 A)   1       sí
S563    1      1 (30 V 2 A)   1       sí
S565    1      1 (30 V 2 A)   1       sí
S567    1      1 (30 V 2 A)   1       no
S560    -      -              -       no
```
4. Probá el relé con una lámpara de 12 V de banco, dentro de la carga del modelo.
5. Si vas a usar MK485 o RSAC-C1-R8, compará tu firmware con el mínimo de la guía de relés externos.
⚠️ Un portón o una cerradura de más de 1 A no va directo al relé del S562: relé auxiliar o fuente propia.

**Regla para quedarse**
Del monitor miro relé, RS485 y carga antes de prometer qué abre.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Interfaces de cada monitor: https://knowledge.akuvox.com/docs/interface-differences-of-akuvox-indoor-monitors
- Carga del relé por modelo: https://knowledge.akuvox.com/docs/relay-output-of-indoor-monitors
- Guía de selección de monitores: https://www.akuvox.com/productSelectionGuide?cid=4
