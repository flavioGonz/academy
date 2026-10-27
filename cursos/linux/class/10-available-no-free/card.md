# Lección 10. Available, no free

**Escuchá:** available-no-free.mp3 (2 min)

**La idea, en tres líneas**
- En `free -h`, la columna que importa es **available**: lo que se puede dar a un programa sin ir a swap, contando caché liberable. "free" bajo es normal.
- `top` o `htop` muestran quién consume: Shift+M ordena por memoria, Shift+P por CPU.
- `kill PID` (señal 15, termina prolijo) antes que `kill -9` (no se puede ignorar, no guarda nada); a un servicio, `systemctl restart`.

**Impacto:** dejás de pedir RAM o de reiniciar servidores por una columna mal leída, y encontrás al proceso que de verdad consume.

**Quién lo dice:** 2 de 3 fuentes coinciden (Debian Reference, linuxblog.io). linuxblog.io advierte que muchas herramientas de monitoreo alertan mirando "free" y no "available", y marcan falsos problemas.

**Laboratorio** · Rápido · 10 min
En cualquier VM:
1. Memoria y carga:
```bash
free -h            # compará las columnas free y available
uptime             # load average de 1, 5 y 15 minutos
nproc              # núcleos: carga sostenida por encima de este número es saturación
```
2. ¿Quién consume?
```bash
top                # Shift+M memoria, Shift+P CPU, q sale
ps aux | sort -rnk 4 | head -5   # ordenado por %MEM
```
3. Señales, con un proceso de prueba:
```bash
sleep 600 &
pgrep -a sleep           # anotá el PID
kill 12345               # SIGTERM (15); poné el PID que viste
pgrep -a sleep           # ya no está
```
Si no terminara: `kill -9 PID` como último recurso.
4. Si el que consume es un servicio:
```bash
systemctl status nombre-del-servicio
sudo systemctl restart nombre-del-servicio
```
Opcional: `sudo apt install htop` para una vista más cómoda.

**Regla para quedarse**
Miro available y la carga antes de decir que falta RAM, y uso kill -9 solo si el kill normal no alcanza.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Free contra available, con el ejemplo de los dos servidores: https://linuxblog.io/free-vs-available
- Señales, top y lsof en la Debian Reference: https://www.debian.org/doc/manuals/debian-reference/ch09.en.html
