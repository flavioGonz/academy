# Tasks

## 1. Tokenizar la paleta
- [x] 1.1 Extraer la paleta de marca a `theme.<instancia>.css` con custom properties (`assets/theme.infratec.css`)
- [x] 1.2 Quitar los tokens de marca hardcodeados de `styles.css` (la paleta vive solo en el theme)
- [x] 1.3 Cargar el `theme.css` de la instancia después de `styles.css` en `index.html`

## 2. Parametrizar textos y logos
- [x] 2.1 Definir un manifiesto de marca (`assets/brand.js`: nombre, unidad, dominio, sitio)
- [x] 2.2 Inyectar el wordmark (header y footer) y el título desde el manifiesto
- [ ] 2.3 Barrido completo de literales "IES"/"Infratec" en `app.js` y `api/*.php` (conservar `X-IES`)

## 3. Unificar y verificar
- [x] 3.1 Capturas antes/después en Infratec (sin regresión visual) — pendiente el A/B con IES
- [ ] 3.2 Verificar que ningún color/nombre/logo de la otra marca aparece (tras el barrido 2.3)
- [ ] 3.3 Confirmar que los contratos de API no cambiaron (X-IES intacto)
- [ ] 3.4 Unificar en una sola rama `main` que sirva ambas instancias

> Base implementada y en producción: color y nombre salen de una fuente única
> (theme.infratec.css + brand.js), sin regresión visual. Falta el barrido completo
> de literales (2.3) y el QA A/B con la instancia IES, que son la parte grande y
> conviene hacer con revisión sobre ambas marcas.
