# Lección 5. Quince voltios

**Escuchá:** quince-voltios.mp3 (2 min)

**La idea, en tres líneas**
- El lazo sale con 30 V y al último elemento tienen que llegarle al menos 15 V; el cálculo del manual supone todos los elementos al final del cable (peor caso).
- Largo máximo: 1600 m con LSN 0300 A y 3000 m con LSN 1500 A; el cable no aislado (entradas de FLM, línea NAC, indicadores remotos) suma como máximo 500 m.
- Según los gráficos del manual: 120 elementos de 0,5 mA llegan a unos 1950 m con LSN 1500 A, pero a 2 mA en 1000 m entran unos 73. El cálculo oficial se hace en Safety Systems Designer.

**Impacto:** detectás en el escritorio el lazo que en obra iba a dar averías intermitentes por baja tensión.

**Quién lo dice:** 1 de 1 fuente (System manual AVENAR, primaria); evidencia escasa en número pero sin discrepancias. La TI 2716 de 2026 confirma que Bosch exige SSD para planificar.

**Laboratorio** · Foco · 20 min
Cuenta de banco (aproximada, siempre pesimista) con los parámetros que lista el manual:
```text
Datos: L = largo del lazo (m), n = elementos, i = consumo medio por elemento (A)
Parámetros del manual: 30 V en bornes, 15 V mínimo, cable 0,8 mm = 0,503 mm2,
  rho cobre = 0,0178 ohm mm2/m, R interna por elemento improved = 0,35 ohm,
  corriente de transmisión 0,012 A, corriente de destello 0,018 A

R_cable  = 2 x L x 0,0178 / 0,503        (ida y vuelta del par)
R_equip  = n x 0,35
I_total  = n x i + 0,012 + 0,018
Caída    = I_total x (R_cable + R_equip)
Queda    = 30 - Caída   -> tiene que dar 15 V o más
```
1. Armá la planilla con esas fórmulas.
2. Probá con L = 600 m, n = 60, i = 0,0005 A. Anotá cuánto queda.
3. Subí i a 0,002 A (lazo con sirenas y módulos) y repetí.
4. Buscá el largo donde la tensión final cae a 15 V para cada caso.
5. Compará con los ejemplos del manual: si tu cuenta da más largo que el gráfico, confiá en el gráfico y en SSD.
⚠️ Esta cuenta no reemplaza a SSD ni al cálculo del proyecto: sirve para detectar lazos en el límite antes de tirar cable.

**Regla para quedarse**
Ningún lazo sin cálculo de caída guardado en la carpeta de obra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Largo alcanzable con LSN 0300 A y LSN 1500 A, gráficos y ejemplos (System manual): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- SSD obligatorio para planificar con zonas de energía (TI 2716): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2716_2026_TI_EN_AVENAR_Panel_Energy_Information.pdf?collection=bosch-bt-lifesafetysystems
