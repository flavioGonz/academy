# Proposal

## Why

El acceso a las lecciones es para técnicos autorizados, pero el alta era abierta y
auto-logueaba. Ya se introdujo un registro *moderado* (alta con `active=0`, sin
auto-login, pantalla de "cuenta pendiente"), y el admin aprueba con el toggle de
`active`. Falta formalizar ese comportamiento como contrato y cerrar los huecos:
el admin no tiene una cola clara de pendientes, no hay aviso cuando llega un alta,
y las personas no saben cuándo quedaron habilitadas. Sin esto, un alta puede
quedar olvidada días y el técnico sin acceso.

## What Changes

- Se especifica el **registro moderado** como contrato: alta inactiva, sin sesión,
  respuesta de "pendiente", y login bloqueado hasta la aprobación.
- Se agrega una **cola de aprobación** en el panel: lista de pendientes separada,
  contador/indicador, y acciones de aprobar o rechazar.
- Aviso al administrador cuando entra un alta nueva, y señal clara a la persona de
  que su cuenta quedó habilitada.

## Capabilities

### New Capabilities
- `user-registration`: alta de cuentas moderada por un administrador, con estados
  (pendiente, habilitada, rechazada), cola de aprobación y avisos.

## Impact

- Afecta: `site/api/auth.php` (register/login), `site/api/admin.php` (cola y
  acciones), `site/assets/app.js` (pantalla de pendiente, badge de pendientes).
- Reutiliza la columna existente `users.active`; puede sumar un estado "rechazada".
- Sin impacto en el contenido de cursos ni en el progreso.
