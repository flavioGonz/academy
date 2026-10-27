# Lección 7. Backup que restaura

**Escuchá:** backup-que-restaura.mp3 (2 min)

**La idea, en tres líneas**
- Backup de VMs con un producto que use las APIs de vSphere (VADP) y Changed Block Tracking, más la regla 3-2-1: tres copias, dos medios, una fuera del sitio.
- Por dentro: snapshot, copia por NBD (red de gestión), HotAdd (proxy virtual) o SAN (proxy físico), y borrado del snapshot.
- El ESXi gratuito no expone VADP: ahí solo queda el backup con agente dentro del sistema operativo. Un backup que nunca se restauró no está probado.

**Impacto:** el día que se rompe algo sabés cuánto tarda la restauración y que funciona.

**Quién lo dice:** 5 de 8 fuentes sobre backups coinciden en VADP/CBT, 3-2-1 y elegir el modo de transporte; la cifra de 10 a 20 MB/s en NBD sobre 1 GbE es de la guía de Veeam v9, antigua.

**Laboratorio** · Foco · 20 min
Con el producto de backup que use el cliente (Veeam, Nakivo, Altaro u otro), en un entorno de laboratorio o con autorización:
1. Creá en el host un port group aislado, sin uplinks:
```bash
esxcli network vswitch standard add -v vSwitch-Aislado
esxcli network vswitch standard portgroup add -p Restore-Aislado -v vSwitch-Aislado
```
2. Restaurá una VM respaldada **con otro nombre** (por ejemplo `srv-prueba-restore`) y conectá su placa de red a `Restore-Aislado`.
3. Prendela, entrá por la consola y verificá datos y servicios.
4. Anotá: tiempo total de restauración, modo de transporte usado (en el log del job: NBD, HotAdd o SAN) y tamaño.
5. Borrá la VM restaurada y confirmá que el job no dejó snapshots colgados en la VM original.

⚠️ Nunca restaures sobre la VM original ni la conectes a la red de producción: duplicarías IP y nombre.

**Regla para quedarse**
Un backup cuenta cuando lo restauré al menos una vez en un lugar aislado y sé cuánto tardó.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Modos de transporte SAN, HotAdd y NBD (documentación de VDDK de Broadcom): https://developer.broadcom.com/xapis/virtual-disk-api/latest/vddkBkupVadp.9.5.html
- Modo red de Veeam, pros y contras: https://veeam-best-practices-guide-v9.readthedocs.io/resource_planning/network_mode.html
- Límites del ESXi gratuito, incluido VADP: https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html
