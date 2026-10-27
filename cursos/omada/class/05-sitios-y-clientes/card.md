# Lección 5. Sitios y clientes

**Escuchá:** sitios-y-clientes.mp3 (2 min)

**La idea, en tres líneas**
- Un sitio adopta un solo gateway: cada sede con su router es un sitio. El roaming y los perfiles WiFi son por sitio, y la VPN automática une sitios del mismo controlador.
- Para varios clientes, modo MSP (Global Settings > Controller Settings): disponible en Software Controller y Omada Central Standard; no en Essentials ni en los OC, según la comparación oficial.
- Roles en dos niveles (MSP y Customer), cada uno con Main Administrator, Administrator y Viewer; un usuario por persona.

**Impacto:** cuando llega el segundo gateway o el segundo cliente, no hay que rehacer la estructura.

**Quién lo dice:** 2 de 3 fuentes sobre sitios y MSP coinciden; no se encontró discrepancia. Límite de clientes MSP según la guía: 100 en v5, 500 en v6.

**Laboratorio** · Admin · 10 min
En tu controlador de laboratorio (v6):
1. **Global View > Dashboard > Site List**: creá el sitio `Central` y el sitio `Sucursal`, cada uno con región Uruguay y zona horaria `America/Montevideo`.
2. **Global View > Account**: creá un usuario `viewer-sucursal` (clave de ejemplo `Visor-Lab-2026`) con rol **Viewer** y acceso solo al sitio `Sucursal`.
3. Cerrá sesión y entrá con ese usuario: tiene que ver solo `Sucursal` y no poder cambiar nada.
4. Opcional, si es Software Controller: activá **MSP Mode** en **Global Settings > Controller Settings**, creá un cliente de prueba y mirá cómo cambian las vistas. Desactivalo al terminar si no lo vas a usar.
```text
Regla de diseño
Cliente (MSP) -> Sitio por sede con gateway -> Equipos de esa sede
Una cuenta por técnico. Viewer para el cliente. Main Administrator solo para la empresa.
```

**Regla para quedarse**
Un sitio por sede con gateway, una cuenta por persona, y MSP solo donde el controlador lo soporta.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo configurar el modo MSP en el controlador v6: https://www.tp-link.com/de/support/faq/4276
- Qué controlador soporta MSP (tabla comparativa oficial): https://support.omadanetworks.com/en/document/13150/
- Un gateway por sitio y adopción de sucursales: https://support.omadanetworks.com/de/document/124358/
