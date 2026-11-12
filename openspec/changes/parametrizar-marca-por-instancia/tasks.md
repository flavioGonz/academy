# Tasks

## 1. Tokenizar la paleta
- [ ] 1.1 Extraer la paleta actual (carmesí Infratec y azul IES) a `theme.<instancia>.css` con custom properties
- [ ] 1.2 Reescribir `styles.css` para consumir solo variables de tema (sin colores fijos)
- [ ] 1.3 Cargar el `theme.css` de la instancia antes de `styles.css` en `index.html`

## 2. Parametrizar textos y logos
- [ ] 2.1 Definir un manifiesto de marca (nombre, dominios, rutas de logo, textos legales)
- [ ] 2.2 Inyectar nombre, wordmark, favicon y pie desde el manifiesto en `app.js`
- [ ] 2.3 Barrido de literales "IES"/"Infratec" en `app.js` y `api/*.php` (conservar `X-IES`)

## 3. Unificar y verificar
- [ ] 3.1 Capturas antes/después en ambas marcas (desktop y mobile)
- [ ] 3.2 Verificar que ningún color/nombre/logo de la otra marca aparece
- [ ] 3.3 Confirmar que los contratos de API no cambiaron
- [ ] 3.4 Unificar en una sola rama `main` que sirva ambas instancias
