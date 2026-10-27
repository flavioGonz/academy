# Lección 8. Nunca dormir

**Escuchá:** nunca-dormir.mp3 (2 min)

**La idea, en tres líneas**
- En un equipo 24/7, suspensión, hibernación y apagado de disco en "nunca" (valor 0 en powercfg) y el inicio rápido apagado.
- La vuelta tras un corte se configura en el BIOS: Restore on AC Power Loss o After Power Failure.
- "Last State" no vuelve si la UPS apagó el equipo en orden; con UPS conviene "Power On".

**Impacto:** puestos que no amanecen suspendidos y servidores que vuelven solos después del corte.

**Quién lo dice:** 2 de 3 fuentes coinciden (SS64 en energía, ServeTheHome en BIOS; woshub aporta el evento 6008 para confirmar el corte); ServeTheHome marca la contra de "Power On": enciende también lo que estaba apagado a propósito.

**Laboratorio** · Rápido · 10 min
En una VM o PC de banco, consola como administrador:
1. Plan activo y estados de suspensión disponibles:
```text
powercfg /getactivescheme
powercfg /a
```
2. Todo en "nunca" con corriente (el monitor se puede apagar):
```text
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change disk-timeout-ac 0
powercfg /change monitor-timeout-ac 15
```
3. Hibernación e inicio rápido apagados:
```text
powercfg /hibernate off
```
4. Qué está pidiendo mantener despierto o despertando el equipo:
```text
powercfg /requests
powercfg /lastwake
```
5. En el equipo de banco, entrá al BIOS o UEFI y buscá la opción en Power, Advanced, Chipset o ACPI. Anotá cómo se llama en esa marca y ponela en Power On.
6. Probá: con el equipo encendido, cortá la energía unos segundos y volvé a darla. Al volver, confirmá el corte con:
```powershell
Get-WinEvent -FilterHashtable @{LogName='System'; Id=6008} -MaxEvents 3
```

⚠️ Hacé la prueba de corte en un equipo de banco, nunca en un servidor en producción con discos girando.

**Regla para quedarse**
Un equipo 24/7 no duerme y vuelve solo cuando vuelve la luz.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Referencia de powercfg: https://ss64.com/nt/powercfg.html
- BIOS y encendido tras corte (Last State vs Power On): https://www.servethehome.com/keeping-servers-bios-setup-availability/
