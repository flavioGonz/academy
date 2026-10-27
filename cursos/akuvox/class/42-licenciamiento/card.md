# Lección 42. Licencias Akuvox

**Escuchá:** licenciamiento.mp3 (2 min)

**La idea, en tres líneas**
- Sin licencia, en la red local: SIP directo, llamada por IP al monitor, relés, RTSP al NVR y apertura por HTTP. En las páginas leídas no hay licencias por función dentro del equipo (2N sí las tiene).
- Se paga la nube, por servicio (SmartPlus en viviendas y Smart Access en oficinas, misma plataforma): app maestra por apartamento, app del administrador, familiares por encima de los gratis (3 según la guía de la app V7.5.2), extras como desvío a teléfono, cámaras de terceros, video en la nube, QR dinámico o ascensor, cerraduras de terceros y Apple Wallet; en oficinas, por puerta con la primera gratis. En PC: ACMS Pro 1.0.0.4 es prueba de 180 días y SDMC pide licencia USB por encima de 500 equipos.
- Paga el distribuidor, o el instalador si el distribuidor lo habilita (`Pay by Installer`); se renueva en automático cada 30 días o a mano. Ningún precio oficial publicado: se cotiza por escrito con el distribuidor. Las cuentas de instalador las crea el distribuidor, así que un traspaso de obra se coordina con él.

**Impacto:** el presupuesto separa equipo (una vez) de nube (recurrente) y nadie descubre en la entrega que la app se paga, ni al año que venció.

**Quién lo dice:** 5 de 8 fuentes sobre el cobro coinciden (Knowledge Base de Akuvox, agosto a octubre de 2026: cobro por servicio con vencimiento y renovación); discrepan un distribuidor canadiense (licencia única de por vida por apartamento), un revendedor británico (con monitor interior no se paga) y un foro alemán de 2024 (activación única).

**Laboratorio** · Admin · 15 min
1. En el portero de laboratorio, `Account > Basic`: si está en la nube, la cuenta 1 muestra el número SIP de SmartPlus; si dice `Failed`, no registra.
2. En `Network > Advanced`, sección `Connect Setting`: anotá el tipo de conexión (`Cloud` si lo administra la nube, SDMC si lo administra el software local).
3. Armá la planilla de un edificio de ejemplo: 24 apartamentos con monitor, 6 quieren desvío al celular, la administración usa app.
```text
Función                               Sin licencia (LAN)   Servicio de nube que se cobra
Llamada portero -> monitor                  sí               ninguno
Apertura desde monitor, PIN, tarjeta        sí               ninguno
RTSP al NVR, HTTP local, relés              sí               ninguno
Llamada a la app del residente              no               App (maestra, x24)
Familiares por encima de los gratis         no               Additional App
Desvío a teléfono o celular                 no               Landline (x6)
App de la administración                    no               PM App
Video guardado en la nube                   no               Video Storage (si lo piden)
```
4. Repetí para una casa: App maestra, familiares extra y, si los piden, Landline o Video Storage.
5. Pedile al distribuidor la cotización por escrito con esas cantidades, el período y la fecha (su portal tiene una calculadora de cargo único y mensual), y pasala a dos renglones:
```text
Equipos e instalación (una vez):  portero, monitores, fuente, mano de obra
Nube SmartPlus (recurrente):      servicios de la planilla, período, vencimiento,
                                  quién renueva (distribuidor, instalador o cliente)
Si no se renueva:                 la app deja de llamar; portero, monitor,
                                  PIN y tarjeta siguen en la red local
```
6. Desconectá el WAN del router de laboratorio, probá cada fila marcada "sí" y volvé a conectar.
⚠️ Cortar el WAN en un edificio habitado deja a los residentes sin app: el ensayo va en laboratorio o con aviso previo.

**Regla para quedarse**
El equipo se cobra una vez, la nube se cotiza por servicio y por escrito con el distribuidor, y la puerta abre igual sin licencia.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué servicios se cobran por tipo de proyecto y cómo se renuevan: https://knowledge.akuvox.com/docs/for-distributors
- Cobro por servicio en comunidades: https://knowledge.akuvox.com/docs/service-based-charging-configuration-for-community-projects
- Calculadora de cotización y el ejemplo de 120 unidades: https://knowledge.akuvox.com/docs/how-to-generate-project-quotations
- Licencia de prueba de ACMS Pro: https://knowledge.akuvox.com/docs/akuvox-acms-pro-administrator-guide
