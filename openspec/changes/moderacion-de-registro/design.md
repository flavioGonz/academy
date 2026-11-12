# Design

## Context
Ya existe la base: `auth.php` crea con `active=0` y sin sesión, el login bloquea
inactivos, y `admin.php?a=user_update {id, active}` alterna el estado. Falta la cola
dedicada, el indicador y, opcionalmente, un estado "rechazada" distinto de inactiva.

## Goals / Non-Goals
**Goals:**
- Contrato claro del alta moderada (ya implementado) y cola de aprobación usable.
- Que ningún alta quede olvidada: indicador de pendientes para el admin.

**Non-Goals:**
- Auto-aprobación por dominio de correo (posible futuro, fuera de alcance).
- Flujo de recuperación de contraseña (es otra capability).

## Decisions
- **Reusar `users.active`** para pendiente(0)/habilitada(1). Para "rechazada" se
  evalúa una marca adicional (p. ej. columna `rejected` o un valor de estado), para
  no confundir una cuenta desactivada a mano con una rechazada en el alta.
- **Cola como filtro del listado de usuarios** existente (`a=users`), más un
  contador de pendientes en la navegación del panel. Alternativa descartada: una
  pantalla separada nueva (más código, menos coherente con el panel actual).
- **Aviso mínimo primero**: indicador en el panel; el correo al admin queda como
  mejora posterior (depende de tener envío de correo disponible en la instancia).

## Risks / Trade-offs
- Introducir un estado "rechazada" toca el esquema → migración aditiva, con valor
  por defecto compatible con las cuentas existentes.
- Avisos por correo dependen de infraestructura de la instancia → se deja opcional.

## Open Questions
- ¿"Rechazada" borra la cuenta o la conserva marcada para auditoría? (Propuesto:
  conservar marcada.)
- ¿El indicador de pendientes va en el sidebar del admin o en el resumen?
