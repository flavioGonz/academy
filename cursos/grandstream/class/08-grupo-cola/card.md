# Lección 8. Grupo o cola

**Escuchá:** grupo-cola.mp3 (2 min)

**La idea, en tres líneas**
- Grupo de llamada: suena en todos a la vez o en orden (60 s por miembro por defecto), sin espera.
- Cola: retiene, reparte con estrategia (Ring All por defecto, Least Recent, Fewest Calls y otras) y necesita largo máximo y destino de desborde.
- Buzón con PIN no trivial (1234 y 1111 se rechazan), envío a correo con SMTP configurado.

**Impacto:** el cliente elige la herramienta correcta y ninguna llamada queda atrapada en música infinita.

**Quién lo dice:** 2 de 2 fuentes coinciden (manual del UCM630x y blog de Grandstream sobre call center); sin discrepancias. Evidencia delgada en cantidad.

**Laboratorio** · Foco · 15 min
1. Grupo de llamada:
```text
Basic Call Features > Ring Group > Add
Extension: 6000   Members: 1001, 1002
Ring Strategy: Ring Simultaneously
Skip Busy Agent: Sí
```
2. Cola:
```text
Basic Call Features > Call Queue > Add
Extension: 6500   Strategy: Least Recent
Agentes estáticos: 1001, 1002, 1003
Agent Ring Time: 30   Retry Time: 5   Agent Rest Time: 10
Max Queue Length: 5
Failover Destination: Ring Group 6000
```
3. Buzón: marcá *97 desde la 1001 y cambiá el PIN por uno no secuencial.
4. Si tenés SMTP de prueba, activá Send Voicemail to Email en la 1001.
5. Llamá a la cola desde dos teléfonos a la vez con un agente ocupado y mirá el reparto.

**Regla para quedarse**
Ninguna cola sin largo máximo y destino de desborde.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Grupos, colas y buzón en el manual: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
- Funciones de call center (devolución, estadísticas): https://blog.grandstream.com/company/news/blog/how-to-use-the-ucm-ip-pbxs-call-center-features
