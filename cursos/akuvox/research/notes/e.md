# Notes: batch e (licenciamiento, lección 42)
Pages read: 12. With notes: 12. Skipped: 1 (https://knowledge.akuvox.com/docs/invalid-mac-address, 51 palabras, el scraper no la guardó; su texto se leyó en la versión .md de la Knowledge Base y no se cita).

Nota de lectura: las páginas de la Knowledge Base se guardaron "undated" pero traen fecha de actualización propia: for-distributors 2 de septiembre de 2026; service-based charging y quotations 4 de agosto de 2026; guía del instalador de comunidades y guía de la app SmartPlus V7.5.2, octubre de 2026; guía de ACMS Pro (servidor 1.0.0.4) 21 de octubre de 2026; guía de SDMC (6.0.0.77) 22 de septiembre de 2026. Ninguna página oficial publica precios.

## T25 Licencias y suscripciones
- e:N1. SmartPlus (residencial) y Smart Access (comercial) son la misma plataforma de nube con dos tipos de proyecto. Tres tipos de proyecto con cobro distinto: Community, Single-Family House, Commercial.
  - Source: https://knowledge.akuvox.com/docs/for-distributors  Quote: "Every Commercial project includes one free door"
  - Kind: definition
  - Level: foundation
- e:N2. Lo que se cobra en un proyecto Community: App (cuenta maestra de la app), PM App (app del administrador), Additional App (familiares por encima de los gratis, "the free number varies by project"), Third Party Lock (iTec, Dormakaba), Premium Plan (Package Room, cámara de terceros, Bookings, ascensor, Smart Parking, QR dinámico, Video Storage, Landline), Sensor Detection Call Alert (MR01), Apple Wallet Pass (1 a 5 años) e Integration (PMS). En casa: App, Additional App, Third Party Lock, Premium Plan (Landline, cámara de terceros, QR dinámico, Video Storage) y alertas de sensor. En comercial: Door (la primera puerta gratis), Personnel App con intercom, Admin App, Premium (asistencia, ascensor), alertas y Apple Wallet.
  - Source: https://knowledge.akuvox.com/docs/for-distributors  Quote: "The free number varies by project."
  - Kind: definition
  - Level: core
- e:N3. Pago: Community y casa con "Regular Payment" (Stripe, PayPal o cupón); comercial creado desde el 1 de junio de 2025 con créditos comprados a Akuvox. El distribuidor decide si el instalador puede pagar (campo Pay by Installer: No Permission, Stripe/PayPal/Coupon, Credit). Ruta: Subscription, instalador y tipo de proyecto, Activate o Renew, sitio y servicio; Auto Renew renueva cada 30 días y corre 30 días el vencimiento; Manual Renew elige fecha.
  - Source: https://knowledge.akuvox.com/docs/for-distributors  Quote: "renewal occurs every 30 days and extends the account's upcoming expiration date by 30 days"
  - Kind: technique
  - Level: core
- e:N4. Cobro por servicios en comunidades: "en lugar de elegir planes predefinidos" se prende cada servicio por comunidad y algunos por apartamento. Infraestructura: With Indoor Monitor (por defecto: cada apartamento con al menos un monitor o un MR01; "afecta el cargo de la app") y Landline (llamada a teléfono fijo o celular, premium). Valor agregado: PM App, Landline para PM, cámara de terceros, Booking, Video Storage, Package Room, QR dinámico, Smart Parking, ascensor. La configuración por apartamento la habilita Akuvox para cada distribuidor.
  - Source: https://knowledge.akuvox.com/docs/service-based-charging-configuration-for-community-projects  Quote: "Instead of selecting predefined plans, you can now"
  - Kind: technique
  - Level: core
- e:N5. Generador de cotizaciones del portal (ícono de calculadora): cargo único y mensual por proyecto, "solo como estimación". En comunidad, cuatro tipos de apartamento (con o sin monitor, con o sin Landline); ejemplo oficial de 120 unidades: 80 con monitor y Landline, 30 con monitor sin Landline, 10 solo app. Comercial: la puerta es la unidad principal de cobro. Casa: con monitor, apps extra, Landline, cámara de terceros, Video Storage (más días, más mensual).
  - Source: https://knowledge.akuvox.com/docs/how-to-generate-project-quotations  Quote: "The generated quotation is for estimation purposes only."
  - Kind: example
  - Level: core
- e:N6. App del residente: tres cuentas de familiar gratis por la maestra, más requiere activación y pago (guía de la app V7.5.2). Si la app no llama o no ve imagen, la FAQ manda a revisar que la cuenta esté activada y la renovación paga. La guía no describe qué pasa en el equipo al vencer.
  - Source: https://knowledge.akuvox.com/docs/akuvox-smartplus-app-user-guide  Quote: "make sure you've paid the renewal fee"
  - Kind: number
  - Level: core
- e:N7. Reset contra borrado de apartamento (inquilino que se va): el reset borra familiares, credenciales y logs pero conserva el estado de suscripción de la cuenta maestra (inactiva o vencida) y los familiares gratis; crear una cuenta nueva tras el reset es gratis, tras borrar se cobra.
  - Source: https://knowledge.akuvox.com/docs/akuvox-smartplus-installer-guide-community  Quote: "It is free to create a new account in the family after resetting, while it charges after deleting."
  - Kind: technique
  - Level: advanced
- e:N8. Software local: ACMS Pro servidor 1.0.0.4 es una versión de prueba gratuita de 180 días desde la instalación, contada con el reloj del servidor; al vencer, todos los usuarios quedan afuera hasta renovar la licencia. SDMC 6.0.0.77: sin licencia USB no importa archivos si los equipos superarían 500.
  - Source: https://knowledge.akuvox.com/docs/akuvox-acms-pro-administrator-guide  Quote: "free trial version, valid for 180 days from installation"
  - Also: https://knowledge.akuvox.com/docs/sdmc-adminitrator-guide-20211225  Quote: "Without using a USB license"
  - Kind: number
  - Level: core
- e:N9. Del lado del equipo: la cuenta SmartPlus aparece en Account > Basic ("Failed" si no registra) y el tipo de conexión en Network > Advanced > Connect Setting (pasa solo a Cloud; en modo SDMC puede no pasar). Lista de puertos salientes que usa la nube (443, 5070, 8501, 9999, RTP).
  - Source: https://knowledge.akuvox.com/docs/device-offline-on-the-smartplus-cloud  Quote: "The connect type will switch to Cloud automatically"
  - Kind: technique
  - Level: core
- e:N10. Un distribuidor canadiense (noviembre de 2025) vende SmartPlus como licencia única por apartamento "de por vida", sin mensualidad, con app y teléfono y cuatro usuarios.
  - Source: https://pipl.systems/guides/akuvox-canada-distribution  Quote: "each unit is covered by a lifetime license"
  - Kind: claim
  - Level: core
- e:N11. Un revendedor británico vende "Akuvox Cloud Subscription" por unidad y dice que con monitor interior no hace falta; sin monitor, una por vivienda o empresa. No dice período.
  - Source: https://firstfence.co.uk/akuvox-cloud-subscription  Quote: "if an indoor monitor is installed, a Cloud Subscription is not required"
  - Kind: claim
  - Level: core
- e:N12. Foro KNX alemán, junio de 2024: usuarios discuten si la app sigue "sin abono", citan una respuesta vieja de soporte con activación única y Festnetz aparte, y otro dice que la cuenta venía incluida con el equipo vía el importador. Uno usa el portero solo offline, sin app.
  - Source: https://knx-user-forum.de/forum/%C3%B6ffentlicher-bereich/geb%C3%A4udetechnik-ohne-knx-eib/1732380-akuvox?p=1960134  Quote: "Ist die Smart-App immer noch abofrei?"
  - Kind: story
  - Level: core
- e:N13. Contraste: 2N licencia funciones en el propio portero (licencia estándar incluida, funciones extra pagas). En las páginas de Akuvox leídas no aparece una licencia por función instalada en el equipo: lo pago vive en la nube o en el software de PC.
  - Source: https://wiki.2n.com/hip/conf/latest/en/3-rozdily-mezi-modely-a-licencovani-funkci/3-2-licencovani-funkci  Quote: "functions that are subject to a paid license"
  - Kind: claim
  - Level: foundation

## Disagreements seen
- Modelo de cobro de la app: la documentación oficial muestra renovación, Auto Renew cada 30 días y "Expiration Time" (https://knowledge.akuvox.com/docs/for-distributors); un distribuidor canadiense vende licencia única de por vida (https://pipl.systems/guides/akuvox-canada-distribution); un revendedor británico dice que con monitor no se paga (https://firstfence.co.uk/akuvox-cloud-subscription). Cómo decidir: vale lo que diga por escrito el distribuidor que da de alta la cuenta de instalador en esta región, con fecha.

## Best stories
- El ejemplo oficial de 120 unidades del generador de cotizaciones (https://knowledge.akuvox.com/docs/how-to-generate-project-quotations).
- ACMS Pro que saca a todos los usuarios a los 180 días si nadie renovó (https://knowledge.akuvox.com/docs/akuvox-acms-pro-administrator-guide).
- "¿Sigue sin abono?": el foro KNX de 2024 (https://knx-user-forum.de/forum/%C3%B6ffentlicher-bereich/geb%C3%A4udetechnik-ohne-knx-eib/1732380-akuvox?p=1960134).

## Huecos
- Ningún precio oficial publicado. No se encontró una página que diga qué deja de andar en el equipo cuando vence la app; lo local se apoya en la lección 10.
- No hay procedimiento publicado para pasar un proyecto de un instalador a otro; lo documentado: el distribuidor crea y administra las cuentas de instalador, ve y borra equipos de proyectos, y un MAC que no cargó tu distribuidor da "Invalid MAC address or already exists".
- No se confirmó el modelo de licencia de MySmart Local Server ni el de ACMS (no Pro).
