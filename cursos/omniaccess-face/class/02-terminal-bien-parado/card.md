# Lección 2. Terminal bien parado

**Escuchá:** terminal-bien-parado.mp3 (2 min)

**La idea, en tres líneas**
- El terminal se monta a la altura que pide la ficha del modelo, pensada para que la cámara vea de frente a personas de 1,50 a 1,90 m paradas a unos 50 cm.
- Nada de sol directo ni de ventana o puerta vidriada detrás de la persona: el contraluz deja la cara en sombra y el equipo no la encuentra.
- Luz frontal pareja, WDR si hay mezcla de sol y sombra, y la ventana de la cámara limpia.

**Impacto:** menos llamadas de "no me reconoce a la tarde" y menos visitas para mover un equipo ya cableado.

**Quién lo dice:** 4 de 4 fuentes de instalación dan una altura fija para un rango de estaturas, pero discrepan en el número: ClockRite 1,1 m mirando hacia abajo, Control iD 1,30 m, Synerion cámara a 1,48 m; Hikvision pide personas de 1,4 a 1,9 m a 0,5 m. 5 de 5 piden evitar sol y contraluz.

**Laboratorio** · Campo · 20 min
Con un terminal facial de banco o el de la obra, una cinta métrica y dos personas de estaturas distintas:
1. Buscá en la ficha o guía rápida del modelo la altura de montaje y la distancia de reconocimiento. Si no la encontrás, partí de la cámara entre 1,30 y 1,48 m del piso.
2. Medí desde el piso hasta la cámara (no hasta el borde del equipo) y anotalo en la ficha de la obra.
3. Pará a cada persona a unos 50 cm, de frente, y probá el reconocimiento:
```text
Persona más baja → ¿reconoce sin agacharse?
Persona más alta → ¿reconoce sin agacharse?
A 30 cm, a 50 cm y a 1 m → ¿desde dónde dispara?
```
4. Mirá qué hay detrás de la persona cuando está frente al equipo: ventana, puerta de vidrio, sol de la tarde. Si hay, marcá la obra como "contraluz".
5. En el menú del terminal buscá las opciones de imagen (WDR, distancia de reconocimiento, luz de relleno). En Hikvision están en System → Biometric; en Akuvox, según el modelo (curso Porteros IP Akuvox, fichas de cada familia).
6. Limpiá la ventana de la cámara con un paño sin pelusa y repetí la prueba con la persona que más falló.

⚠️ Si para que reconozca a alguien hay que subir la sensibilidad o bajar el umbral, el problema suele ser la luz o la altura: corregí eso primero.

**Regla para quedarse**
El terminal se monta para la luz de la peor hora del día, no para la del momento en que lo instalás.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Alturas, contraluz, luz frontal y limpieza en terminales faciales (Synerion): https://help.synerion.com/agile/knowledge-base/gt-installation-guidelines
- Recomendaciones de instalación y de fotos (Control iD): https://www.controlid.com.br/docs/access-api-en/facial-recognition/recommendations-photos-install/
- Guía rápida de un terminal facial Hikvision (DS-K1T343): https://pinfo.hikvision.com/hkwsen/unzip/20260304161336_58290_doc/UD24344B-E_Baseline_DS-K1T343%20Series%20Face%20Recognition%20Terminal_Quick%20Start%20Guide_V1.1_20250107.pdf
- Ángulos máximos de giro e inclinación de la cara (Senstar): https://xnet.senstar.com/webhelp/Symphony/8.0/en/topic_reference/air_face_settings_8.html
