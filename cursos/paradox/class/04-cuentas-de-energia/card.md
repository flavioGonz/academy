# Lección 4. Cuentas de energía

**Escuchá:** cuentas-de-energia.mp3 (2 min)

**La idea, en tres líneas**
- Transformador de 16,5 Vac y 40 VA mínimo, en un toma sin llave; batería de 12 V y 7 Ah (4 Ah admitida en SP+).
- Todo lo que cuelga de AUX se suma: en la SP5500+ el manual pide no pasar de 700 mA; si la salida corta, se sacan las cargas 10 segundos antes de reconectar.
- Umbrales de batería en SP+: falla a 10,5 V, desconexión de protección a 9,1 V, apagado a 8,5 V. Sin sirena, 1 kΩ en BELL evita la falla de campana.

**Impacto:** la central no se apaga a mitad de un corte de luz ni corta el auxiliar cuando suena todo junto.

**Quién lo dice:** 2 de 2 fuentes coinciden (guías SP+ y EVOHD+); evidencia fina pero con números del fabricante. No se encontró quien discrepe.

**Laboratorio** · Admin · 15 min
1. Armá la planilla con los consumos máximos de la tabla de la guía SP+ (los sensores, de la hoja de su fabricante):
```text
Equipo                 Cant.  mA máx c/u   Total
K32LCD+                2      86           172
TM70 (más zumbador)    1      250 + 80     330
ZX8                    1      31           31
IP150+                 1      100          100
Detectores (su hoja)   6      ...          ...
Suma AUX                                   ...
```
2. Compará la suma con el límite de tu central (SP5500+: 700 mA; mirá la guía para SP6000+ y SP7000+). Si te pasás, fuente auxiliar aparte para parte de las cargas.
3. Autonomía aproximada: horas = Ah de la batería / (consumo de la central + suma AUX en amperes). Ejemplo EVOHD+: 7 / (0,100 + 0,130) = unas 30 h, igual a la tabla del manual.
4. Si no hay sirena conectada, poné una resistencia de 1 kΩ entre BELL+ y BELL- y verificá con TBL que desaparece la falla de campana (grupo 3).
5. Con la central en batería, medí con el tester: anotá el valor y compará con los umbrales (10,5 V falla; 8,5 V apagado).

⚠️ Batería conectada al revés quema el fusible de batería. Verificá polaridad antes de cerrar el gabinete.

**Regla para quedarse**
Si no sumé el auxiliar, no energizo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Transformador, AUX, campana, batería y tabla de consumos de módulos (guía SP+): https://www.paradox.com/Downloader/?ID=11662
- Tabla de autonomía por batería y umbrales (guía EVOHD+): https://descargas.fiesa.com.ar/descargas/Paradox/Manuales%20y%20Documentos/Paneles/EVOHD+/EVOHD+%20-%20Manual%20de%20Instalaci%c3%b3n.pdf
