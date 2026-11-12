# Design

## Context
Ya implementado en gran parte: `prefers-reduced-motion` global en `styles.css`,
foco visible (`:focus-visible`), números tabulares en cifras, `text-wrap: balance`,
`scroll-margin` bajo el header, barra de carga `#nprog` enganchada a `route()`, y
entrada de paneles con clase one-shot `tab-enter`. Esta propuesta fija ese
comportamiento como contrato para que no se degrade.

## Goals / Non-Goals
**Goals:**
- Que el movimiento sea una mejora, nunca un obstáculo (reduce-motion siempre gana).
- Retroalimentación de carga clara y foco siempre visible.

**Non-Goals:**
- Animaciones decorativas sin función.
- Rediseñar pantallas (eso es otra línea de trabajo).

## Decisions
- **Reduce-motion como interruptor maestro:** un bloque `@media (prefers-reduced-
  motion: reduce)` desactiva animaciones y oculta la barra de carga.
- **Entrada por clase, no por `hidden`:** la transición de pestaña se dispara con
  una clase one-shot al cambiar de tab, no con el toggle de visibilidad, para no
  re-animar en refrescos in-place. Alternativa descartada: `.panel:not([hidden])`
  (re-animaba en cada acción).
- **Barra de carga en el router:** `route()` inicia el indicador al comenzar y lo
  completa al terminar de renderizar; es el único punto de enganche.

## Risks / Trade-offs
- Las animaciones en refrescos frecuentes podrían distraer → resuelto con la clase
  one-shot y animaciones breves.
- La barra de carga sobre navegaciones muy rápidas podría parpadear → completar con
  un breve retardo de salida.

## Open Questions
- ¿Extender el cross-fade a los controles segmentados del panel de admin (filtros)?
