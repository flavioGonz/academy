# Lección 11. Padrón y reportes

**Escuchá:** padron-y-reportes.mp3 (2 min)

**La idea, en tres líneas**
- El padrón es una cadena: Unidad (Unidades / Lotes) → Usuario (Usuarios & Residentes) → Credencial (matrícula, tarjeta, rostro) → Grupo de acceso (por dónde y cuándo). Una matrícula suelta, sin usuario ni unidad, abre igual pero después no se puede responder "¿qué autos tiene el lote 12?".
- Vehículos / Matrículas muestra cada vehículo con su dueño y su última detección. Para que la cámara también abra sola, Dispositivos → Sincronizar matrículas a las cámaras: Incremental aplica solo las diferencias; Reemplazo total borra y recarga, solo para reparar.
- Las visitas van por Invitados (pase con patente y vigencia; si el barrio tiene WhatsApp configurado, avisa al anfitrión) y el reporte del mes sale de Historial de Acceso → Exportar (Excel / PDF), con la portada de Configuración → Branding → Reportes Exportables.

**Impacto:** "no me abre" deja de ser un misterio y el cierre de mes sale en un PDF con la marca del cliente.

**Quién lo dice:** el Manual del Administrador describe la cadena, los estados y las tareas de cierre de mes; el código confirma la sincronización con las cámaras, los pases de invitado y la exportación (en esta versión el menú Reportes aparece en modo Filas; en LPR el reporte sale del Historial). La web aporta el costo oculto: gatesentry calcula 20 a 80 horas de carga al migrar un barrio de 500 casas, y cada auto nuevo es otra alta.

**Laboratorio** · Admin · 20 min
En una instalación de prueba, con datos inventados.
1. Unidades / Lotes: creá "Lote 99 (prueba)".
2. Usuarios & Residentes → nuevo usuario "Residente Prueba", unidad Lote 99, dos credenciales de matrícula `SBA1234` y `SCD5678`, grupo de acceso Residentes. Guardá.
3. Vehículos / Matrículas: buscá `SBA1234` y confirmá dueño, unidad y última detección.
4. Dispositivos → vista Cámaras LPR → Sincronizar matrículas a las cámaras → Analizar. Leé por cámara cuántas hay A agregar y A quitar. Elegí Incremental y confirmá.
5. Invitados → Nuevo pase de visita: nombre "Visita prueba", patente `SAB1234`, validez rápida Mañana. Mirá el QR y el aviso a las garitas.
6. Historial de Acceso → Exportar (Excel / PDF): período del mes pasado, todos los eventos, formato PDF. Revisá la portada.
7. Al terminar, pasá el usuario de prueba a Suspendido (no lo elimines) y volvé a sincronizar.
⚠️ Reemplazo total deja a cada cámara sin lista mientras recarga: se usa solo para reparar y fuera del horario de mayor tránsito.

**Regla para quedarse**
Cargo siempre la cadena completa (unidad, usuario, matrícula y grupo) y sincronizo las cámaras en modo Incremental.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- El costo de mantener el padrón y el auto que no está cargado: https://gatesentry.com/blog/license-plate-recognition-hoa-gates/
- Límite de matrículas en la lista de la cámara Hikvision: https://syscom.mx/blog/hikvision-anpr-reconocimiento-de-placas
- La patente Mercosur en Uruguay (formato de tres letras y cuatro números): https://www.autoblog.com.uy/2015/04/ya-circulan-las-primeras-patentes.html
