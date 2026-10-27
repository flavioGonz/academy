# Lección 1. Quién decide la puerta

**Escuchá:** quien-decide-la-puerta.mp3 (2 min)

**La idea, en tres líneas**
- El terminal facial (Akuvox u Hikvision) reconoce la cara y abre el relé por su cuenta: la decisión física vive en el equipo.
- OmniAccess Face recibe el evento por la red, le pone Permitido o Denegado según el Modo Face (Lista Blanca o Lista Negra), guarda la foto y lo muestra en el Monitor Facial.
- El modo se activa en Configuración → Modos: con OmniAccess Face prendido cambian el menú, la pantalla de inicio y el Monitor en Vivo.

**Impacto:** dejás de prometerle al cliente que "el sistema bloquea" cuando lo que bloquea es la memoria del terminal, y sabés dónde tocar cuando algo abre de más.

**Quién lo dice:** el código de OmniAccess y 2 de 2 fuentes externas (Hikvision y CIE sobre Akuvox) ubican la decisión en el equipo; ninguna fuente leída dice lo contrario.

**Laboratorio** · Rápido · 10 min
En una instalación de demo o de prueba, con un usuario administrador:
1. Abrí la configuración de modos:
```text
Configuración → Modos → Modos (LPR / Face / Cola) → pestaña Modo Face
```
2. Mirá el banner de arriba: si dice "Activar este modo", el módulo OmniAccess Face (MODULE_FACE) está apagado. En una demo, tocá Activar: la aplicación se recarga con la interfaz del modo.
3. Leé las tres opciones del Modo Face y anotá qué dice cada una:
```text
Lista Negra   → las capturas identificadas se registran DENEGADAS
Lista Blanca  → las capturas identificadas se registran PERMITIDAS
Aprendizaje   → deshabilitado (en desarrollo)
```
4. Buscá en la explicación del modo la frase sobre la apertura física. Es la que vas a repetirle al cliente.
5. Volvé al menú lateral y anotá qué cambió: "Monitor en Vivo" ahora abre el Monitor Facial y aparece la sección Face con "Dispositivos Faciales".
6. Si tu sistema tiene también LPR, fijate que "Invitados" sigue apareciendo solo con el módulo LPR prendido.

⚠️ En producción no cambies de modo sin avisar: recarga la interfaz de todos los puestos y cambia cómo se registran los eventos desde ese momento.

**Regla para quedarse**
La puerta la abre el terminal; OmniAccess la cuenta, la clasifica y la guarda.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Parámetros biométricos de un terminal Hikvision, donde vive el umbral de coincidencia: https://enpinfo.hikvision.com/hkwsen/unzip/20251224164304_81809_doc/GUID-9F07C169-0B01-4F3E-8729-0BD5189C7613.html
- Reglas por evento en Akuvox Smart Access (la alternativa en la nube): https://cie-group.com/news/what-are-akuvox-event-trigger-rules-and-how-do-they-work
- Qué es un webhook: https://en.wikipedia.org/wiki/Webhook
