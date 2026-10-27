# Lección 3. El terminal avisa

**Escuchá:** el-terminal-avisa.mp3 (2 min)

**La idea, en tres líneas**
- El terminal se da de alta en Dispositivos como Acceso Facial, con su IP, su MAC, el usuario y la clave de su API y el Sentido del Flujo (Entrada o Salida): la MAC es la que une cada aviso con el equipo.
- El terminal avisa cada evento con una Action URL al servidor de eventos de OmniAccess, puerto 10000; la URL se copia del configurador del propio sistema. La foto no viaja en el aviso: el servidor la va a buscar al registro del terminal.
- El botón Relé de la lista de dispositivos abre a pedido; lo demás lo abre el terminal cuando reconoce.

**Impacto:** el evento aparece en el monitor con equipo, sentido y foto desde el primer día, y sabés por qué cuando no aparece.

**Quién lo dice:** el código de OmniAccess (servidor de eventos y configurador de Action URLs) y 2 de 2 fuentes sobre webhooks (Wikipedia, CIE sobre Akuvox) coinciden en el modelo "el equipo llama a una URL cuando pasa algo"; CIE describe además la variante en la nube de Akuvox, que OmniAccess no usa.

**Laboratorio** · Foco · 25 min
Datos de ejemplo: servidor OmniAccess 192.0.2.10, terminal Akuvox 192.0.2.21, MAC 00:00:5E:00:53:21.
1. En la web del terminal anotá IP y MAC, y dejá la API HTTP con un usuario propio para OmniAccess (cómo se hace en el equipo: curso Porteros IP Akuvox, lección Quién puede abrir).
2. En OmniAccess:
```text
Gestión → Dispositivos Faciales → Agregar
Tipo: Acceso Facial    Fabricante: Akuvox    Modelo Hardware: el del equipo
Host / IP: 192.0.2.21   Hardware ID (MAC): 00:00:5E:00:53:21
Usuario Manager / API Password: el usuario de API del paso 1
Sentido del Flujo: ENTRADA (Ingreso)   Ubicación Física: Portería peatonal
```
3. Guardá y mirá la fila del equipo: los contadores Faces y Tags y el ícono Pull en verde dicen que OmniAccess pudo consultarlo.
4. Abrí el menú de la fila y copiá la URL de Valid Face (empieza con http y apunta al servidor, puerto 10000):
```text
⋯ → Webhooks (Action URL) → Valid Face → Copiar URL
192.0.2.10:10000/api/webhooks/akuvox?event=face_valid&mac=$mac&user=$user_name&userid=$userid&FaceUrl=$FaceUrl&PicUrl=$pic_url&time=$time
```
5. Pegala en la Action URL de rostro válido del terminal (dónde está en cada familia: curso Porteros IP Akuvox, lección El portero avisa). Repetí con Invalid Face y Relay Output.
6. Pasá una cara enrolada frente al equipo y abrí el registro de avisos:
```text
Configuración → Sistema → Webhooks → fuente Akuvox
```
Tiene que figurar el aviso con la MAC y el nombre del dispositivo, no "Dispositivo Desconocido". El ícono Push (azul) de la fila se prende.
7. Tocá el botón Relé de la fila y verificá que la cerradura se mueve y que llega un evento de puerta abierta.

⚠️ La URL va al puerto 10000 (servidor de eventos), no al puerto del panel: la ruta del panel responde OK pero no procesa nada. Y el terminal tiene que poder llegar a ese puerto a través del firewall.

**Regla para quedarse**
Sin la MAC cargada no hay evento, y sin camino de vuelta del servidor al terminal no hay foto.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Qué es un webhook y cómo se usa: https://en.wikipedia.org/wiki/Webhook
- Reglas por evento y webhooks en Akuvox Smart Access: https://cie-group.com/news/what-are-akuvox-event-trigger-rules-and-how-do-they-work
