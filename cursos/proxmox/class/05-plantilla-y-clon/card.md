# Lección 5. Plantilla y clon

**Escuchá:** plantilla-y-clon.mp3 (2 min)

**La idea, en tres líneas**
- Imagen cloud oficial, disco importado, unidad **cloud-init**, y la VM se convierte en **plantilla**.
- Usuario, clave SSH e IP se configuran desde Proxmox; la VM los aplica en el primer arranque.
- **Full clone** para producción; **linked clone** solo para laboratorio, porque depende de la plantilla.

**Impacto:** una VM Linux lista en minutos en vez de media hora de instalador, y todas iguales.

**Quién lo dice:** 4 de 4 fuentes coinciden en la receta; la wiki oficial destaca los linked clones, mientras computingforgeeks y croit recomiendan full clone para lo que va a producción.

**Laboratorio** · Foco · 20 min
1. En el host, bajá la imagen `debian-13-genericcloud-amd64.qcow2` desde `cloud.debian.org/images/cloud/trixie/latest/` a `/root/`.
2. Creá la VM base, importá el disco y agregá cloud-init:
```bash
qm create 9000 --name debian13-tpl --memory 2048 --cores 2 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-single --agent 1
qm set 9000 --scsi0 local-lvm:0,import-from=/root/debian-13-genericcloud-amd64.qcow2
qm set 9000 --ide2 local-lvm:cloudinit
qm set 9000 --boot order=scsi0
qm set 9000 --serial0 socket --vga serial0
qm template 9000
```
3. Si no tenés clave SSH en el host, creala con `ssh-keygen`. Clonás y configurás (rango de documentación):
```bash
qm clone 9000 201 --name prueba-ci --full 1
qm set 201 --ciuser tecnico --sshkeys /root/.ssh/id_ed25519.pub --ipconfig0 ip=10.10.10.201/24,gw=10.10.10.1
qm resize 201 scsi0 +10G
qm start 201
```
4. Mirá el arranque en la consola **xterm.js** y entrá con `ssh tecnico@10.10.10.201`.
5. Si cambiás algo de cloud-init después, regenerá el CD con `qm cloudinit update 201`.

**Regla para quedarse**
Producción en full clone desde plantilla; linked clone solo para laboratorio.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cloud-init en Proxmox, wiki oficial: https://pve.proxmox.com/wiki/Cloud-Init_Support
- Plantillas desde imágenes cloud, full contra linked: https://computingforgeeks.com/create-proxmox-vm-templates-cloud-images/
- Paso a paso con Ubuntu 24.04: https://www.croit.io/blog/how-to-use-cloud-images-for-faster-vm-deployment-in-proxmox-ve
