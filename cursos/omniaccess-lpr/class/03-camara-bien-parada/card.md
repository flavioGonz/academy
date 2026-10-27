# Lección 3. Cámara bien parada

**Escuchá:** camara-bien-parada.mp3 (2 min)

**La idea, en tres líneas**
- Ángulo: hasta 30° vertical (contra el piso) y 30° horizontal (contra el sentido de marcha). Más allá la lectura cae rápido.
- Tamaño: la patente ocupa entre 100 y 300 píxeles de ancho en la imagen (Hikvision pide al menos 130 y recomienda 150 a 200). En la práctica, 4 a 8 metros del punto donde el auto frena.
- Un carril por cámara, leer donde el vehículo va lento (antes de la barrera, no después), poste firme y sin sol de frente al amanecer o al atardecer.

**Impacto:** la tasa de lectura se gana en la obra, antes de tirar un cable; lo que se coloca mal no lo arregla ningún ajuste del panel.

**Quién lo dice:** 4 de 4 fuentes coinciden en los 30° (guía de Hikvision, DTK, guía de instalación UK y el Manual del Instalador). En el mínimo de píxeles discrepan: DTK y el manual dicen 100, Hikvision 130.

**Laboratorio** · Campo · 20 min
En un acceso de prueba (o en el estacionamiento del taller), con un auto quieto en el punto donde se va a leer.
1. Medí con cinta la altura de la cámara (H), la altura de la patente (h, casi siempre 0,4 a 0,6 m) y la distancia horizontal entre la cámara y la patente (D).
2. Calculá el ángulo vertical y anotalo:
```text
ángulo vertical = arctan((H - h) / D)
ejemplo: H = 2,5 m, h = 0,5 m, D = 5 m  ->  arctan(2 / 5) = 22°  (bien)
ejemplo: H = 3,0 m, h = 0,5 m, D = 4 m  ->  arctan(2,5 / 4) = 32° (se pasa: alejar o bajar)
```
3. Sacá una captura desde la web de la cámara con el auto en el punto de lectura y abrila en un editor de imágenes.
4. Medí el ancho de la patente en píxeles con la herramienta de selección. Si da menos de 130, acercá con el zoom o mové el punto de lectura; si da más de 300, abrí el zoom.
5. Mirá el ángulo horizontal: parado detrás de la cámara, la línea al centro del carril no se aparta más de 30° del sentido de marcha.
6. Anotá en la ficha del acceso: H, D, ángulos, píxeles, carril y si da el sol de frente en algún horario.
⚠️ Una cámara que cubre entrada y salida a la vez lee mal las dos: si el acceso tiene dos carriles, van dos cámaras.

**Regla para quedarse**
La posición de la cámara no se arregla con software: la mido con cinta y con píxeles antes de fijarla.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía de instalación de cámaras LPR de Hikvision, con errores comunes: https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
- Ángulos, píxeles y distancia mínima según la altura: https://www.dtksoft.com/camera-installation
- Altura, distancia y velocidad en accesos residenciales: https://home-security-guide.readthedocs.io/en/latest/cctv/17-anpr-camera-installation-guide-uk/
