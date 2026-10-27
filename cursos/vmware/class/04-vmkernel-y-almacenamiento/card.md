# Lección 4. VMkernel y almacenamiento

**Escuchá:** vmkernel-y-almacenamiento.mp3 (2 min)

**La idea, en tres líneas**
- Los adaptadores VMkernel (vmk) son las IPs del propio host: gestión, vMotion, almacenamiento IP, backup. Uno por tipo de tráfico, cada uno con su VLAN y subred.
- El tráfico de vMotion viaja sin cifrar (lleva la memoria de la VM): va en una red privada solo para hosts.
- Datastores: VMFS sobre disco o LUN, NFS 3 o 4.1 contra un NAS. Si usás jumbo frames, MTU 9000 igual en vmk, vSwitch, switch físico y NAS.

**Impacto:** se terminan las latencias "fantasma" y los cortes intermitentes de almacenamiento por MTU desparejo.

**Quién lo dice:** 2 de 2 fuentes coinciden (documentación de Broadcom y phoenixNAP); evidencia escasa en cantidad, sin discrepancias.

**Laboratorio** · Foco · 20 min
En un ESXi de laboratorio, con un port group "Storage-VLAN30" ya creado (ver lección 3) y un NAS de prueba en 10.10.10.50:
```bash
# vSwitch y vmk con MTU 9000
esxcli network vswitch standard set -v vSwitch1 -m 9000
esxcli network ip interface add -i vmk1 -p Storage-VLAN30 -m 9000
esxcli network ip interface ipv4 set -i vmk1 -t static -I 10.10.10.21 -N 255.255.255.0

# probar MTU grande sin fragmentar (8972 = 9000 menos 28 de encabezados)
vmkping -I vmk1 -d -s 8972 10.10.10.50

# montar un export NFS de prueba como datastore
esxcli storage nfs add -H 10.10.10.50 -s /export/lab -v nfs-lab
esxcli storage filesystem list
```
Si el vmkping grande falla y el normal (`vmkping -I vmk1 10.10.10.50`) anda, hay un salto con MTU 1500 en el camino.

⚠️ Cambiar el MTU de un vSwitch con VMs de producción puede cortar tráfico un instante: hacelo en ventana de mantenimiento.

**Regla para quedarse**
Cada tráfico del host tiene su vmk, su VLAN y su prueba de vmkping.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Tipos de tráfico VMkernel y pilas TCP/IP (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/setting-up-vmkernel-networking/the-vmkernel-networking-layer.html
- iSCSI, NFS y jumbo frames en una instalación nueva: https://phoenixnap.com/kb/vmware-esxi
