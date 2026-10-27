# Lección 8. vCenter y permisos

**Escuchá:** vcenter-y-permisos.mp3 (2 min)

**La idea, en tres líneas**
- vCenter es un appliance (VCSA) que gestiona varios hosts y habilita clúster, vMotion, HA y DRS. Pide RAM en serio: en vSphere 8 el tamaño Tiny pide 14 GB.
- El acceso pasa por vCenter Single Sign-On; dominio por defecto vsphere.local. administrator@vsphere.local es la llave maestra: se guarda, no se usa a diario.
- Permiso = usuario o grupo + rol (conjunto de privilegios) + objeto del inventario. Cada técnico con su usuario y un rol acotado.

**Impacto:** cada cambio queda a nombre de quien lo hizo y un error de un usuario de soporte no puede tumbar todo.

**Quién lo dice:** 2 de 4 fuentes sobre vCenter coinciden en dimensionar la VCSA; 2 de 3 sobre permisos en el modelo usuario + rol + objeto. Lam reporta Tiny con 10 GB en laboratorio, fuera de soporte.

**Laboratorio** · Admin · 15 min
En un vCenter de laboratorio (o un Hands-On Lab de Broadcom):
1. **Administration > Single Sign On > Users and Groups > Users**, dominio vsphere.local: creá `tecnico.prueba` con una contraseña de ejemplo como `Lab-Ejemplo-2026!`.
2. **Administration > Access Control > Roles**: elegí **Read-only**, **Clone**, nombre `Soporte-Lectura`. Agregale solo el privilegio **Virtual machine > Interaction > Console interaction**.
3. En **Hosts and Clusters**, clic derecho sobre una carpeta o clúster de prueba > **Add Permission**: usuario `tecnico.prueba`, rol `Soporte-Lectura`, marcá **Propagate to children**.
4. Cerrá sesión, entrá como `tecnico.prueba@vsphere.local` y verificá qué ves y qué no podés cambiar.
5. Por SSH en la VCSA (si está habilitado), mirá dónde quedan los logs: `ls /var/log/vmware/`.

⚠️ En un cliente, la contraseña de administrator@vsphere.local va al gestor de contraseñas de la empresa; no se comparte por chat.

**Regla para quedarse**
Nadie entra a vCenter con administrator@vsphere.local para tareas del día a día.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Permisos, roles y SSO (Broadcom TechDocs): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-security/vsphere-permissions-and-user-management-tasks.html
- RAM de la VCSA en vSphere 8 y otros cambios (William Lam): https://williamlam.com/2022/09/homelab-considerations-for-vsphere-8.html
