# Lección 2. Bus de a grupos

**Escuchá:** bus-de-a-grupos.mp3 (2 min)

**La idea, en tres líneas**
- El bus de 4 hilos alimenta y comunica teclados y módulos: hasta 15 módulos en las SP+, hasta 254 y 914 m de cable total en la EVOHD+ (según sus guías).
- Los módulos se conectan sin energía (red y batería desconectadas) y de a grupos, mirando las fallas después de cada grupo.
- Cada teclado tiene una entrada de zona; un inalámbrico aprendido en el mismo número pisa a la zona de teclado o cableada.

**Impacto:** una falla de bus aparece en el grupo que acabás de sumar, no en una búsqueda a ciegas por todo el edificio.

**Quién lo dice:** 1 de 3 fuentes describe el procedimiento por grupos (guía EVOHD+); las otras dos (guía SP+ y ficha M25) no lo contradicen. La regla de que el inalámbrico pisa la zona cableada sale solo de la guía SP+.

**Laboratorio** · Campo · 20 min
Material: central SP+ o MG de banco, un teclado (K32+, K32LCD+ o K35) y un expansor ZX8.
1. Desconectá la red de 16,5 Vac y la batería.
2. Conectá el teclado a los cuatro bornes del bus respetando la serigrafía. Energizá.
3. Mirá las fallas: en SP/MG con la tecla TBL. Lo esperable en una central nueva es pérdida de reloj (grupo 8) y, si no hay sirena, campana (grupo 3).
4. Desenergizá otra vez, sumá el ZX8, energizá y repetí el paso 3. Cualquier falla nueva es del ZX8 o de su cableado.
5. Asigná la zona del teclado (SP+):
```text
[ENTER] + código de instalador
mantener 3 s la tecla de acción (la que vale F en la tabla hexadecimal)
05            (zona 05, dos dígitos en K32+/K32LCD+)
[ENTER]       guarda y sale
```
6. Si sacaste un módulo del bus, borrá la falla que queda:
```text
[ENTER] + código de instalador + [955]
```
7. En EVO, la sección [4000] lista los módulos que la central ve, y la [4005] se usa después de quitar módulos.

⚠️ En obra con el sistema en servicio, avisá a monitoreo antes de desenergizar: la central puede reportar falla de AC o tamper.

**Regla para quedarse**
Un módulo por vez, sin energía, y TBL después de cada uno.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Puesta en marcha recomendada, bus Digiplex y cable blindado (guía EVOHD+): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
- Zona de teclado, tabla de reconocimiento de zonas y sección 955 (guía SP+): https://www.paradox.com/Downloader/?ID=11662
