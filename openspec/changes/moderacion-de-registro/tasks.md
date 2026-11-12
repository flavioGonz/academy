# Tasks

## 1. Formalizar el contrato existente
- [x] 1.1 Verificar que el registro crea inactivo, sin auto-login, y responde "pendiente"
- [x] 1.2 Verificar que el login bloquea inactivos con mensaje de aprobación
- [x] 1.3 Cubrir el caso de correo duplicado con error claro

## 2. Cola de aprobación en el panel
- [x] 2.1 Filtro "Pendientes" en el listado de usuarios del admin
- [x] 2.2 Indicador con la cantidad de pendientes (badge en el sidebar + aviso en el Resumen + contador en el chip)
- [x] 2.3 Acciones de aprobar y rechazar desde la cola

## 3. Estado rechazada (aditivo)
- [x] 3.1 Migración aditiva (columnas `rejected`, `approved_at`) para distinguir pendiente / habilitada / desactivada / rechazada
- [x] 3.2 Reflejar el estado en el listado y en el login (mensaje propio para rechazada)

## 4. Avisos
- [x] 4.1 Señal clara a la persona cuando su cuenta queda habilitada (puede ingresar tras la aprobación)
- [ ] 4.2 (Opcional) aviso por correo al admin cuando entra un alta, si la instancia tiene envío

> Implementado y en producción. Backend: api/lib.php (migración idempotente),
> api/admin.php (user_update approve/reject, kpi.pending), api/auth.php (mensaje de rechazo).
> Frontend: app.js (filtro Pendientes, botones Aprobar/Rechazar, badge y aviso).
