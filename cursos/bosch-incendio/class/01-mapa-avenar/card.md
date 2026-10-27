# Lección 1. Mapa AVENAR

**Escuchá:** mapa-avenar.mp3 (2 min)

**La idea, en tres líneas**
- AVENAR panel 2000: 6 módulos y hasta 4 lazos. AVENAR panel 8000: 46 módulos y hasta 32 lazos. FPA-5000 y FPA-1200 son la generación anterior y comparten el lazo LSN.
- La licencia standard o premium viene grabada en el controlador y no se cambia: premium habilita BMS, panel jerárquico UGM, evacuación por voz y, en el 2000, la red con otros paneles.
- Firmware 4.x solo en redes 100 % AVENAR (vigente: 4.8.1, junio 2026); una red con FPA corre toda el mismo 3.x, que ya salió de mantenimiento.

**Impacto:** cotizás ampliaciones e integraciones sin descubrir en obra que al panel le falta licencia o firmware.

**Quién lo dice:** 3 de 3 fuentes coinciden (System manual, TI 2715 de firmware, nota de la venta a Triton); nadie discrepa, pero licencias y ramas las documenta solo el fabricante.

**Laboratorio** · Admin · 10 min
1. Leé la etiqueta del controlador. Los modelos SPC son licencia standard y los PPC son premium:
```text
FPE-2000-SPC  AVENAR panel 2000, standard
FPE-2000-PPC  AVENAR panel 2000, premium
FPE-8000-SPC  AVENAR panel 8000, standard
FPE-8000-PPC  AVENAR panel 8000, premium
FPE-8000-FMR  AVENAR keypad 8000
```
2. Tocá el logo de Bosch en la pantalla para ver la versión de firmware.
3. Contá los módulos del riel y anotá cuáles son de lazo (LSN 0300 A o LSN 1500 A) y cuál es el de baterías.
4. Completá la ficha:
```text
Panel: AVENAR 2000 / AVENAR 8000 / FPA-5000 / FPA-1200
Licencia: standard / premium
Firmware: ______ (exacto)
Módulos: LSN 0300 A x _  LSN 1500 A x _  BCM x _  otros: ______
En red: no / sí (nodos: __)   Ethernet conectado: no / sí
```
5. Si encontrás firmware 3.x con el panel en Ethernet, marcalo para evaluación de riesgo con el cliente.
⚠️ Para apagar un controlador AVENAR se usa su botón de encendido antes de quitar la alimentación; cortar la energía con el sistema andando puede dañarlo.

**Regla para quedarse**
Antes de cotizar una ampliación, anoto licencia y firmware de cada panel.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Licencias, módulos y ramas de firmware (System manual AVENAR): https://media.boschsecurity.com/fs/media/pb/media/extranet/fire_alarm_system/documentation/avenar_panel_system_information/BDL_SYM_AVENAR_panel_F01U378910_05_en.pdf
- Firmware 4.8.1 y RPS 5.15.27, novedades y fin de soporte: https://media.boschbuildingtechnologies.com/fs/media/pb/media/extranet/fire_alarm_system/tech_info_en/2715_2026_TI_AVENAR_FW-4.8.1__FSO-5000-RPS_5.15.27.pdf?collection=bosch-bt-lifesafetysystems
- Bosch vende seguridad pero se queda con incendio: https://www.securityinfowatch.com/industry-news/article/55249385/bosch-sells-security-and-communications-technology-business-to-triton-partners
