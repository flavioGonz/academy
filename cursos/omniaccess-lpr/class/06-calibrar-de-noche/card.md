# Lección 6. Calibrar de noche

**Escuchá:** calibrar-de-noche.mp3 (2 min)

**La idea, en tres líneas**
- Dispositivos → Calibrar ANPR abre el video en vivo de la cámara con su región editable: la Zona de lectura de patente por carril y la Línea de captura, donde la patente se ve derecha y grande. Se guarda en la cámara y se puede revertir.
- La Auto-calibración aplica el Perfil ANPR barrio-noche, pensado para 20 a 30 km/h y faros de frente: obturador 1/500, anti-brillo de patente en 60, WDR y HLC apagados, ganancia máxima 40, filtro e iluminador IR en automático y foco semiautomático.
- La Tasa de lectura (leídas contra no leídas) se mira por cámara y por hora: más de 95 % es correcta, 85 a 95 % aceptable, menos de 85 % es un problema de emplazamiento o de luz.

**Impacto:** la cámara que de día lee todo deja de perder las patentes de las tres de la mañana, que son las que después se buscan.

**Quién lo dice:** las guías de Hikvision, Omada y Milestone coinciden en zona solo sobre el carril, IR para patentes retrorreflectivas y probar de noche. Discrepan en el obturador (Hikvision propone del orden de 1/1000 para cortar faros; el perfil de OmniAccess usa 1/500 porque en un barrio se anda despacio) y en el WDR (Omada sugiere probar con y sin; el perfil lo apaga).

**Laboratorio** · Foco · 25 min
Conviene hacerlo de noche, en una cámara Hikvision de prueba o en la peor cámara de un barrio con permiso del cliente.
1. Dispositivos → vista Cámaras LPR → Tasa de lectura. Anotá la tasa global, la peor cámara y las horas por debajo de 85 %.
2. En esa cámara, Calibrar ANPR. Con el video en vivo, arrastrá los puntos de la Zona de lectura para que cubra solo el carril, sin vereda ni calle de afuera.
3. Mové la Línea de captura al punto donde la patente se ve derecha y del tamaño medido en la obra. Guardar línea de captura → Sí, guardar.
4. Auto-calibración → Perfil ANPR barrio-noche: leé la lista de pasos y anotá los valores actuales antes de aplicar.
5. Aplicá. Algunos ajustes reinician la cámara: esperá a que vuelva el video.
6. Pasá un auto con las luces prendidas y mirá el recorte de la patente en el Monitor LPR: legible, sin brillo blanco y sin movimiento.
7. A la semana, volvé a la Tasa de lectura y compará la franja de la noche.
```text
tasa = leídas / (leídas + no leídas)
> 95 %  correcta · 85 a 95 % aceptable (revisar horas malas) · < 85 % emplazamiento o luz
```
⚠️ La auto-calibración es solo para Hikvision y cambia parámetros de imagen: hacela con los valores anteriores anotados para poder volver.

**Regla para quedarse**
La calibración se mide por hora y se prueba de noche, nunca con el promedio del día.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Obturador para cortar faros y "esperá la noche": https://cdn.connectec.uk/Files/Products/CCTV/Camera/Hikvision_Trade/installation_guide_of_hikvision_lpr_camera.pdf
- Zona de reconocimiento, línea de disparo, WDR y obturador: https://www.omadanetworks.com/au/support/faq/4723/
- IR y patentes retrorreflectivas: https://www.milestonesys.com/globalassets/techcomm/ltsb/provms/english-united-states/10900.htm
