# Design

## Context
La marca vive hoy en tres capas: CSS (override de `:root` con la paleta carmesí),
HTML/JS (nombre, wordmark de texto, textos "IES/Infratec") y PHP (algunos textos).
Los logos son archivos en `assets/`. No hay una fuente única; por eso hay dos ramas.
El sitio es estático servido (sin build), así que la solución no puede depender de
un bundler.

## Goals / Non-Goals
**Goals:**
- Una sola fuente de verdad de marca por instancia, legible sin build.
- Quitar literales de marca del motor (CSS/JS/PHP).
- `main` única para ambas instancias.

**Non-Goals:**
- Un selector de tema en vivo para el usuario final (es por instancia, no por sesión).
- Rediseñar la identidad; solo parametrizar la existente.

## Decisions
- **Tokens CSS como capa de aplicación.** El tema define custom properties
  (`--brand-ink`, `--brand-accent`, familias tipográficas, etc.) en un único
  archivo `theme.css` por instancia, cargado antes de `styles.css`. `styles.css`
  deja de hardcodear la paleta y consume solo variables.
- **Manifiesto de marca para textos y logos.** Un `brand.json` (o constantes en
  `config.php`, no versionado) con nombre, dominios, rutas de logo y textos; el
  front lo lee al iniciar y rellena nombre, wordmark, favicon y pie. Alternativa
  descartada: seguir con literales en JS (no elimina el fork).
- **Identificadores técnicos congelados.** `X-IES` y los nombres de campos/rutas
  quedan como contrato y no se renombran con la marca.

## Risks / Trade-offs
- Regresión visual al mover colores a variables → mitigar con capturas A/B en ambas
  marcas y una pasada de QA por pantalla.
- Un tema mal formado podría dejar la UI sin estilo → tema por defecto de respaldo.

## Migration Plan
1. Extraer la paleta actual a `theme.infratec.css` y `theme.ies.css` (tokens).
2. Reescribir `styles.css` para consumir variables; sin cambios visuales.
3. Mover nombre/logos/textos a `brand.json`; el front los inyecta.
4. Barrido de literales "IES"/"Infratec" en JS/PHP (excepto `X-IES`).
5. QA A/B en las dos instancias; unificar en `main`.

## Open Questions
- ¿El tema se sirve como archivo estático o se inyecta desde `config.php`?
- ¿Se soporta tema oscuro por instancia en esta etapa o queda para después?
