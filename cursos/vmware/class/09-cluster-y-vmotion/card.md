# Lección 9. Clúster y vMotion

**Escuchá:** cluster-y-vmotion.mp3 (2 min)

**La idea, en tres líneas**
- vMotion mueve una VM encendida a otro host copiando memoria y estado; si solo cambia el host, el disco tiene que estar en almacenamiento compartido.
- HA detecta la caída de un host y reinicia sus VMs en otro: hay corte de minutos. Sigue funcionando aunque vCenter esté caído.
- DRS reparte carga por CPU y memoria y necesita vCenter. Crear el clúster es libre; activar HA o DRS depende de la licencia.

**Impacto:** le explicás al cliente qué protege y qué no, y no prometés "cero corte" con HA.

**Quién lo dice:** 2 de 4 fuentes sobre clúster coinciden (KB de Broadcom y TechTarget); evidencia moderada y TechTarget es de 2011, vale por los conceptos.

**Laboratorio** · Foco · 20 min
Necesita vCenter: uno de laboratorio con dos hosts anidados, o un Hands-On Lab de Broadcom.
1. Clic derecho en el datacenter > **New Cluster**, nombre `Cluster-Lab`. Activá **vSphere HA**. DRS en **Partially Automated** si la licencia lo permite.
2. Arrastrá los dos hosts al clúster. Verificá que cada uno tenga un vmk con el servicio **vMotion** habilitado (**Host > Configure > Networking > VMkernel adapters**), en su VLAN propia.
3. Elegí una VM de prueba encendida con disco en un datastore compartido. **Migrate > Change compute resource only**, destino el otro host.
4. Mientras migra, dejá un ping continuo a la VM desde tu notebook:
```powershell
ping -t 192.168.88.50
```
5. Revisá en **Monitor > Tasks** el tiempo de la migración y anotá cuántos pings se perdieron.
6. En **Cluster > Monitor > vSphere HA > Summary**, mirá qué host quedó como primario.

**Regla para quedarse**
A un cliente le digo "HA reinicia en otro host", nunca "no se cae".

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Cómo funciona vMotion (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-and-host-management/migrating-virtual-machines-host-management/migration-with-vmotion-host-management.html
- Crear un clúster con HA y DRS, y qué requiere licencia (KB de Broadcom): https://knowledge.broadcom.com/external/article/308413
- Conceptos de HA, control de admisión y DRS: https://www.techtarget.com/it-infrastructure/feature/Enabling-VMware-HA-DRS-Advanced-vSphere-features
