# Lección 8. Zona de energía

**Escuchá:** zona-energia.mp3 (2 min)

**La idea, en tres líneas**
- Desde el 02/05/2026 las instalaciones AVENAR nuevas usan zonas de energía con FPE-8000-BCM: no se mezcla con BCM-0000-B en un panel, pide firmware 4.7.0 o más, RPS 5.14.17 o más y SSD 3.6 o más.
- Batería = (I reposo x horas + I alarma x tiempo de alarma) x factor. Las fuentes discrepan: 24 h, 5 min y 1,20 (guía NFPA 72) contra factor 1,25 (Security Sales); la IT-11 uruguaya de 2010 pide 15 min de alarma. RPS trae 30 h por defecto.
- RPS valida la autonomía con corriente de alarma y marca sobrecorriente falsa en zonas con muchas sirenas: el truco temporal de Bosch (1 h y 26 Ah) se documenta y se deshace cuando salga la corrección.

**Impacto:** la central aguanta lo que dice el proyecto y el cálculo se puede defender en una inspección.

**Quién lo dice:** 3 de 3 fuentes coinciden en la forma del cálculo; discrepan en el factor (1,20 contra 1,25) y en el tiempo de alarma según la norma que se adopte.

**Laboratorio** · Foco · 15 min
```text
Datos de ejemplo: I reposo = 0,6 A   I alarma = 2,5 A

Variante A (guía NFPA 72): (0,6 x 24 + 2,5 x 5/60) x 1,20 = ____ Ah
Variante B (más exigente):  (0,6 x 30 + 2,5 x 15/60) x 1,25 = ____ Ah

Batería elegida (2 x 12 V en serie): ____ Ah   Norma del proyecto: ____
Fecha de fabricación de las baterías: ____
```
1. Calculá las dos variantes y redondeá hacia arriba a una capacidad comercial.
2. Anotá cuál pide el proyecto firmado.
3. En la próxima puesta en marcha, medí cada batería (12,0 a 14,1 V) y probá por separado falta de red y falta de batería: el aviso de batería puede demorar hasta 15 minutos.
⚠️ Si usás el truco temporal de la TI 2739 para poder descargar, dejalo escrito en la carpeta de obra y en el panel, y volvé a los valores reales con la versión corregida de RPS.

**Regla para quedarse**
La batería se calcula con la norma que pide el proyecto, con margen, y se rotula con su fecha de fabricación.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Zonas de energía y FPE-8000-BCM (TI 2716): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2716_2026_TI_EN_AVENAR_Panel_Energy_Information.pdf?collection=bosch-bt-lifesafetysystems
- La falsa sobrecorriente de RPS y su truco temporal (TI 2739): https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2739_2026_TI_2739_2026_TI_FSP-5000-RPS_EN.pdf?collection=bosch-bt-lifesafetysystems
- Baterías con factor 1,25 y cómo probarlas: https://www.securitysales.com/insights/proper-backup-power-best-practices/130905/
