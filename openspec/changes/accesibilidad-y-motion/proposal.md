# Proposal

## Why

Se incorporaron transiciones premium (entrada de paneles al cambiar de pestaña,
animación de página en cada navegación y una barra de carga superior) y un pase de
accesibilidad (foco visible, números tabulares, equilibrado de títulos). Falta
fijar ese comportamiento como contrato para que no se degrade con el tiempo: que el
movimiento siempre respete a quien pide menos animación, que el foco sea siempre
visible, y que la navegación dé retroalimentación de carga. Sin spec, un cambio
futuro puede reintroducir animaciones que mareen o un foco invisible.

## What Changes

- Se especifica que **todo el movimiento respeta `prefers-reduced-motion`**: con la
  preferencia activa no hay animaciones ni barra de carga.
- Se especifica la **retroalimentación de navegación** (indicador de carga entre
  páginas) y la **entrada de paneles** al cambiar de pestaña, sin re-animar en
  refrescos internos.
- Se fija el **piso de accesibilidad**: foco visible en todo elemento interactivo,
  anclajes que no quedan tapados por el header, y cifras con números tabulares.

## Capabilities

### New Capabilities
- `ui-motion`: contrato de movimiento, retroalimentación de carga y piso de
  accesibilidad de la interfaz.

## Impact

- Afecta: `site/assets/styles.css` (animaciones, foco, tabular, reduce-motion),
  `site/assets/app.js` (barra de carga, entrada por cambio de pestaña), `index.html`.
- Sin impacto en datos ni en la API.
