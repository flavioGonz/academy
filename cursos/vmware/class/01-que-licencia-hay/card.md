# Lección 1. Qué licencia hay

**Escuchá:** que-licencia-hay.mp3 (2 min)

**La idea, en tres líneas**
- Desde 2024 VMware se vende solo por suscripción: vSphere Foundation (VVF) y Cloud Foundation (VCF). Standard y Enterprise Plus no pasan de 8.0 Update 3.
- Se licencia por núcleo físico, con un mínimo de 16 núcleos por CPU, y vCenter viene incluido.
- ESXi gratuito volvió con 8.0 U3e, pero sin vCenter, sin vMotion ni HA, sin backups por API (VADP) y sin soporte. vSphere 8 pierde soporte el 11 de octubre de 2027.

**Impacto:** dejás de prometer funciones que la licencia del cliente no tiene y le avisás a tiempo del fin de soporte.

**Quién lo dice:** 6 de 9 fuentes de licenciamiento coinciden en el cuadro; sobre el ESXi gratuito, la KB de Broadcom y phoenixNAP lo dan vigente y dos páginas anteriores (Thomas-Krenn, Introserv) lo dan por discontinuado.

**Laboratorio** · Admin · 10 min
1. Entrá al Host Client del ESXi (en el navegador, la IP del host seguida de /ui; en el ejemplo, 192.168.88.20/ui) y andá a **Manage > Licensing**. Anotá clave, producto, funciones y vencimiento.
2. Habilitá SSH un rato (**Host > Actions > Services > Enable Secure Shell**) y consultá versión y CPU:
```bash
vmware -vl
esxcli hardware cpu global get
```
3. "CPU Packages" es la cantidad de procesadores y "CPU Cores" el total de núcleos: núcleos por CPU = CPU Cores / CPU Packages. Calculá los licenciables: por cada CPU, el mayor entre sus núcleos reales y 16. Ejemplo: 2 CPU de 8 núcleos = 16 físicos, 32 licenciables.
4. Volcalo en una ficha del cliente: versión exacta, tipo de licencia, núcleos físicos, núcleos licenciables, fecha de fin de soporte (vSphere 8: 11/10/2027).
5. Deshabilitá SSH al terminar.

⚠️ Este laboratorio es para entender lo que tiene el cliente. La compra y renovación se hace por el canal oficial de Broadcom o su distribuidor.

**Regla para quedarse**
Antes de proponer una función de VMware, miro qué licencia y qué versión tiene el host.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- ESXi 8.0 U3e gratuito y sus límites (KB de Broadcom): https://knowledge.broadcom.com/external/article/399823/vmware-esxi-80-update-3e-now-available-a.html
- Fin de soporte de vSphere 8 y productos asociados: https://knowledge.broadcom.com/external/article/456708/upcoming-end-of-service-for-vsphere-8-vs.html
- Cuentas de núcleos y ediciones vigentes en 2026: https://introserv.com/blog/migrating-from-vmware-in-2026-the-end-of-perpetual-licenses-vsphere-8-end-of-support-and-replacement-options/
