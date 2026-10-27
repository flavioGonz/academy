# Lección 3. Llamada directa

**Escuchá:** llamada-directa.mp3 (2 min)

**La idea, en tres líneas**
- Una llamada IP directa va del portero al monitor por IP, sin servidor ni central, con los dos en la misma red.
- Se configura en `Intercom > Basic > Direct IP`; puerto 5060 por defecto, igual en ambos extremos.
- Cada equipo que se agrega en el medio es una función más que se puede romper: la central se pone cuando suma.

**Impacto:** casas y locales chicos quedan andando con menos piezas, y menos piezas son menos visitas de soporte.

**Quién lo dice:** 2 de 2 fuentes coinciden (guía de llamadas del E16 y un caso en la comunidad FreePBX); evidencia escasa, nadie discrepa.

**Laboratorio** · Rápido · 10 min
1. Poné IP fija (o reserva DHCP) a los dos equipos:
```text
Portero  192.168.88.21/24  gw 192.168.88.1
Monitor  192.168.88.31/24  gw 192.168.88.1
```
2. En los dos: `Intercom > Basic > Direct IP`, puerto 5060 (dejalo igual en ambos).
3. En el portero, configurá el botón de llamada (o el contacto) para marcar `192.168.88.31`.
4. Apretá el botón, atendé en el monitor y abrí con la tecla de apertura.
5. Desenchufá el monitor 30 segundos, volvé a enchufarlo y repetí la llamada.
6. Si la llamada no entra, revisá que los dos estén en la misma subred y que nada filtre el 5060 entre ellos.

**Regla para quedarse**
Casa con un portero y monitores en la misma red: llamada directa e IP fija; la central solo si alguien atiende desde afuera.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- IP directa y cuentas SIP en la guía del E16: https://knowledge.akuvox.com/docs/intercom-call-configuration-8
- La vista previa que andaba directo y no a través de FreePBX: https://community.freepbx.org/t/early-media-doorphone-video-preview/99698
