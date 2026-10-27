# Lección 6. DTMF que abre

**Escuchá:** dtmf-que-abre.mp3 (2 min)

**La idea, en tres líneas**
- Para abrir por DTMF, el tipo (RFC 2833, SIP INFO o inband) y el código tienen que ser iguales en portero, central y monitor.
- RFC 2833 es la opción más compatible; inband se degrada con codecs comprimidos y SIP INFO no siempre lo pasa la central.
- El código de fábrica se cambia y la lista blanca DTMF limita quién puede abrir.

**Impacto:** se terminan los "atiendo, veo a la persona y no abre", que son la mitad de los llamados de soporte de portería.

**Quién lo dice:** 5 de 5 fuentes coinciden en "mismo tipo y mismo código"; 3 de 5 prefieren RFC 2833. Akuvox presenta SIP INFO como confiable y 3CX lo desaconseja.

**Laboratorio** · Foco · 15 min
1. Portero (web):
```text
Account > Advanced > DTMF        Type: RFC2833
Access Control > Relay           Relay A, DTMF Mode: 3 dígitos, código: 731
Access Control > Relay > Open Relay Via DTMF   Only Contacts List
```
2. Monitor (web):
```text
Account > Advanced > DTMF                         Type: RFC2833
Device > Relay > Relay Setting > Remote Relay     código: 731
Device > Relay > SoftKey In Talking Page          tecla tipo Remote Relay DTMF = 731
```
3. Si hay central, poné la extensión del portero y la del monitor también en RFC 2833.
4. Llamá, atendé y abrí con la tecla. Después marcá 731 en el teclado.
5. Pasá solo el monitor a SIP INFO y probá: tiene que fallar. Volvé a RFC2833.
6. Llamá desde un número que no esté en contactos del portero y verificá que el código no abre.

**Regla para quedarse**
RFC 2833 en las tres puntas, código propio y lista blanca: así se abre siempre y solo quien corresponde.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Receta oficial de DTMF portero y monitor: https://knowledge.akuvox.com/docs/how-to-open-the-door-via-dtmf-on-the-indoor-monitor
- Tipos de DTMF y lista blanca en la guía del E16: https://knowledge.akuvox.com/docs/door-unlock-configuration-8
- Por qué 3CX no recomienda SIP INFO: https://www.3cx.com/blog/voip-howto/dtmf-rfc2833/
