# Lección 8. Registro y guardia

**Escuchá:** registro-y-guardia.mp3 (2 min)

**La idea, en tres líneas**
- Todo queda registrado. En el **Monitor Intrusión**, **Historial** lista las detecciones (filtros Intrusión+, Intrusión, Línea, Movim., Todo) y **Evidencia** las muestra en grilla con filtros de cámara, estado (Pendientes, Revisadas) y rango de fechas; cada tarjeta dice **Pendiente**, **Real** o **Falsa**.
- Una detección se corrige sola, sin tocar las demás, desde la ficha de la detección en la vista de pared: **Era falsa alarma**, **Era real** o **Fue real**. Las fotos viven en el bucket de intrusión con la retención de **Configuración → Almacenamiento**.
- La tablet del guardia no recibe la alarma de intrusión en esta versión. El puesto ve a cada guardia en el **Mapa** (posición cada 10 s con la app en pantalla) y lo manda por radio a la zona de la línea en rojo.

**Impacto:** el administrador encuentra cualquier evento de anoche con su foto y su decisión, y el guardia llega al lugar correcto.

**Quién lo dice:** 2 de 2 fuentes piden guardar la evidencia de lo que vio el operador con retención definida; 2 de 4 alertan sobre la fatiga del operador, que se nota en el registro como pendientes acumuladas.

**Laboratorio** · Admin · 15 min
1. **Monitor Intrusión → Evidencia**. Filtrá **Cámara**: "Perímetro Norte 12", **Estado**: Pendientes, **Rango de fechas**: anoche de 22:00 a 06:00.
2. Pasá el mouse 3 segundos sobre una tarjeta: reproduce el clip del NVR. Abrila para ver la ficha.
3. En la vista de pared (**Monitores → Intrusión → Abrir**, con sesión del panel), abrí esa misma detección en **Últimas detecciones** y corregila: **Falsa alarma** o **Fue real**. Volvé a Evidencia y mirá que pasó a Revisadas.
4. **Historial**: elegí **Línea** y recorré las páginas. Anotá cuántas hubo en la semana en esa cámara.
5. **Configuración → Almacenamiento → Políticas de Retención**: anotá los días del **Bucket Intrusión** y compará con lo que pidió el cliente.
6. Abrí el **Mapa** con la capa de guardias: ubicá al guardia más cercano a la línea de "Perímetro Norte 12" y practicá el mensaje por radio: cámara, lugar, qué se vio y hace cuánto.

⚠️ Bajar la retención borra fotos viejas para siempre: acordalo por escrito con el administrador.

**Regla para quedarse**
Ninguna detección termina el turno como pendiente.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Grabar lo que vio el operador y turnos para evitar la fatiga (SDM): https://www.sdmmag.com/articles/89047-video-monitoring-best-practices
- Vencimiento automático de objetos en MinIO, la base de la retención: https://min.io/docs/minio/linux/administration/object-management/object-lifecycle-management.html
