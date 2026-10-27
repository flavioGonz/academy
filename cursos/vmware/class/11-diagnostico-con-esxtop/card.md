# Lección 11. Diagnóstico con esxtop

**Escuchá:** diagnostico-con-esxtop.mp3 (2 min)

**La idea, en tres líneas**
- esxtop por SSH: `c` CPU, `m` memoria, `u` disco por dispositivo, `v` disco por VM, `n` red, `f` campos, `h` ayuda, `q` salir.
- %RDY es el tiempo que una VM esperó un procesador físico: alto significa fila, no falta de vCPU. En disco, GAVG = DAVG (almacenamiento) + KAVG (host); KAVG debería estar cerca de cero.
- Logs del host en /var/run/log: vmkernel.log y vmkwarning.log son el primer lugar para buscar.

**Impacto:** "anda lento" pasa a ser un número que separa CPU, almacenamiento o cola del host.

**Quién lo dice:** 4 de 7 fuentes sobre troubleshooting coinciden en medir y leer logs antes de opinar; ninguna da un umbral universal para %RDY o DAVG, conviene comparar con un día normal.

**Laboratorio** · Foco · 15 min
Por SSH en un ESXi de laboratorio con alguna VM trabajando:
1. Abrí esxtop y recorré las pantallas:
```bash
esxtop
# c  CPU: mirá %RDY y %USED por VM
# m  memoria: MCTLSZ (balloon) y SWCUR (swap)
# u  disco por dispositivo: DAVG/cmd, KAVG/cmd, GAVG/cmd
# n  red: %DRPTX y %DRPRX (paquetes descartados)
# q  salir
```
2. Grabá un minuto en modo batch al datastore (12 muestras cada 5 segundos):
```bash
esxtop -b -a -d 5 -n 12 > /vmfs/volumes/datastore1/esxtop-$(hostname)-$(date +%Y%m%d-%H%M).csv
```
3. Buscá errores recientes en los logs del host:
```bash
tail -n 200 /var/run/log/vmkernel.log
grep -i -E "error|fail|lost" /var/run/log/vmkernel.log | tail -n 30
tail -n 50 /var/run/log/vmkwarning.log
```
4. Anotá en la ficha del cliente los valores normales de %RDY y DAVG: esa es tu línea base.

**Regla para quedarse**
No diagnostico "lentitud" sin un minuto de esxtop guardado y una mirada a vmkernel.log.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cada métrica de esxtop explicada (KB de Broadcom): https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html
- Guía práctica de esxtop: https://www.virtualizationhowto.com/2023/07/esxtop-commands-the-ultimate-guide/
- Hardware fuera de lista y logs con warnings (comentarios en William Lam): https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
