# Lección 2. ESXi bien instalado

**Escuchá:** esxi-bien-instalado.mp3 (2 min)

**La idea, en tres líneas**
- Primero el modelo en la Broadcom Compatibility Guide (la ex HCL): CPU, NIC y controladora. Si no está, no hay soporte.
- ESXi 8 pide 2 núcleos, 8 GB de RAM (12 GB en producción), NX/XD y VT habilitados en BIOS, NIC gigabit soportada y arranque UEFI.
- Disco de arranque persistente: 32 GB mínimo, 128 GB óptimo, idealmente RAID 1. SD y USB quedan solo para arranque y están en retirada. ESXi 9 deja afuera CPUs Skylake y anteriores.

**Impacto:** menos servidores que se cuelgan "sin motivo" y cero instalaciones sin soporte en clientes.

**Quién lo dice:** 3 de 3 fuentes de hardware coinciden en usar la Compatibility Guide; William Lam documenta cómo forzar CPUs viejas, solo para laboratorio y sin soporte.

**Laboratorio** · Campo · 15 min
1. Anotá marca, modelo, CPU, NICs y controladora del servidor y buscalos en la Broadcom Compatibility Guide para ESXi 8.0 U3 (y para 9.0 si el cliente piensa actualizar).
2. Entrá al BIOS: habilitá VT-x o AMD-V, NX/XD y modo de arranque UEFI.
3. Booteá el instalador ESXi 8 desde un USB o desde la consola remota (iLO, iDRAC) **sin instalar**. Si hay CPU o dispositivos no soportados, el instalador lo avisa.
4. Si instalás, elegí un disco persistente (no la SD). Al reiniciar, en la DCUI:
```text
F2 > Configure Management Network
  IPv4 Configuration: Static
    IP 192.168.88.20 / 255.255.255.0 / Gateway 192.168.88.1
  DNS Configuration: 192.168.88.1, hostname esxi-lab01
Esc > Y (reinicia la red de gestión)
```
5. En el navegador abrí la IP del host con /ui (acá 192.168.88.20/ui, por HTTPS) y entrá con root al Host Client.

⚠️ Parámetros como allowLegacyCPU=true permiten instalar en CPUs fuera de soporte: solo en laboratorio, nunca en un cliente.

**Regla para quedarse**
Ningún ESXi se instala en hardware que no chequeé en la Compatibility Guide ni en un pendrive.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Requisitos de hardware de ESXi 8.0 (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esx-installation-and-setup/installing-and-setting-up-esxi-install/esxi-requirements-install/esxi-hardware-requirements-install.html
- CPUs que quedan fuera en ESXi 9 (William Lam): https://williamlam.com/2025/06/ultimate-lab-resource-for-vcf-9-0.html
- Instalación y DCUI paso a paso: https://phoenixnap.com/kb/vmware-esxi
