# Lección 9. Historial y reportes

**Escuchá:** historial-y-reportes.mp3 (2 min)

**La idea, en tres líneas**
- Historial de Acceso responde preguntas con filtros: Rostros, Permitidos o Denegados, Entrada o Salida, rango de fecha y hora y búsqueda por persona, lote o equipo; después se exporta a Excel o PDF.
- Auditoría Hardware trae los registros que quedaron en la memoria del terminal y no llegaron por aviso (corte de red, Action URL mal cargada) y los suma como eventos de sincronización.
- La retención del Bucket FACE (Almacenamiento) borra por antigüedad todo lo que hay en ese bucket: capturas y también fotos de alta.

**Impacto:** el reporte que pide la administración sale en minutos, sin huecos por cortes de red, y nadie pierde fotos de alta por una regla de retención mal pensada.

**Quién lo dice:** el código de OmniAccess (Historial, Auditoría Hardware, Almacenamiento) y 2 de 2 fuentes sobre retención automática por días (documentación de MinIO y Synerion); el Dictamen 3/023 de la URCDP pide analizar el ciclo de vida de los datos. Ninguna fuente discrepa.

**Laboratorio** · Admin · 20 min
En una demo con eventos de al menos una semana:
1. Armá el reporte de la pregunta "¿quién fue rechazado en la portería peatonal esta semana?":
```text
Menú → Historial de Acceso
Tipo: Rostros   Resultado: Denegados   Sentido: Entrada
Rango: lunes 00:00 a hoy
Buscar: Portería peatonal
```
2. Exportá con el botón "Exportar (Excel / PDF)" y abrí el archivo. Anotá cuántos son y cuántos dicen "Desconocido".
3. Ahora traé lo que el terminal registró sin avisar (esta sincronización existe para terminales Akuvox):
```text
Configuración → Avanzado → Auditoría Hardware
Portería peatonal → Sincronizar memoria
```
Leé el aviso "Sincronizados N eventos (Door: …, Call: …)" y volvé al Historial: los eventos traídos así llevan "SINCRO_HW" en el detalle.
4. Revisá la retención:
```text
Configuración → Sistema → Almacenamiento → Bucket FACE
Días de retención antes de borrar. (0 = nunca)
```
Anotá el valor actual y quién lo definió. Si está en 0, las fotos no se borran nunca.
5. Con la administración, escribí en una línea cuánto tiempo se guardan las capturas y cómo se resguardan las fotos de alta antes de poner un número.

⚠️ La regla de retención del Bucket FACE se aplica a todo el bucket, sin distinguir capturas de fotos de alta: con 30 días, a los 30 días también desaparecen las fotos de alta más viejas y la ficha queda sin foto para reenviar al terminal.

**Regla para quedarse**
Un reporte empieza por la pregunta, y una retención empieza por saber qué se borra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Vencimiento automático de objetos por días en MinIO: https://docs.min.io/community/minio-object-store/administration/object-management/create-lifecycle-management-expiration-rule.html
- Gestión del ciclo de vida de objetos en MinIO: https://docs.min.io/community/minio-object-store/administration/object-management/object-lifecycle-management.html
- URCDP, Dictamen 3/023 (ciclo de vida y seguridad de datos biométricos): https://www.gub.uy/unidad-reguladora-control-datos-personales/institucional/normativa/dictamen-n-3023-0
