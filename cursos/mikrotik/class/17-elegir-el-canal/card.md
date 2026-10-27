# Lección 17. Elegir el canal

**Escuchá:** elegir-el-canal.mp3 (2 min)

**La idea, en tres líneas**
- **long-term**: sale poco, solo arreglos críticos, sin funciones nuevas en su rama. **stable**: cada pocos meses, con funciones nuevas probadas. **testing**: cada pocas semanas, no va en producción. **development**: para probar lo último.
- En sitios de clientes, long-term por defecto; stable solo si necesitás una función nueva y la probaste en el banco; testing y development, nunca.
- El canal se cambia en Check for Updates o con `/system/package/update/set channel=`; si el canal ofrece una versión más vieja, también sirve para bajar.

**Impacto:** menos sorpresas después de actualizar y una flota que se comporta igual en todos los clientes.

**Quién lo dice:** 2 de 3 fuentes coinciden en dejar testing fuera de producción y preferir la rama conservadora; la documentación de MikroTik describe los canales sin elegir y ofrece un script de actualización automática, mientras el distribuidor LinITX recomienda la rama de solo arreglos (hoy long-term) para producción.

**Laboratorio** · Admin · 10 min
En un router de laboratorio con RouterOS 7 y salida a internet:
1. Canal y versión actuales:
```routeros
/system/package/update/print
```
Anotá `channel`, `installed-version` y `latest-version`.
2. Compará lo que ofrece cada canal sin instalar nada:
```routeros
/system/package/update/set channel=long-term
/system/package/update/check-for-updates
/system/package/update/print
/system/package/update/set channel=stable
/system/package/update/check-for-updates
/system/package/update/print
```
3. Decidí con esta tabla y dejá el canal elegido:
```text
Sitio de cliente que se visita poco          -> long-term
Necesito una función que solo trae stable    -> stable, probado antes en el banco
Banco de pruebas propio                      -> testing o development
```
```routeros
/system/package/update/set channel=long-term
```
4. Anotá en el legajo del cliente: canal, versión y fecha. Si el cliente tiene varios equipos, todos en el mismo canal.
5. Si un equipo quedó en stable y lo querés en long-term, cambiá el canal, `check-for-updates` y, con backup antes (lección 16), instalá la versión que ofrezca.

⚠️ El script de actualización automática de la documentación instala lo que salga en el canal sin que lo pruebes: en clientes, mejor no.

**Regla para quedarse**
Long-term en clientes; lo nuevo, primero en mi banco.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Canales de RouterOS y actualización estándar: https://help.mikrotik.com/docs/spaces/ROS/pages/328142/Upgrading+and+installation
- Qué canal usar en producción, según un distribuidor (con los nombres viejos de los canales): https://blog.linitx.com/mikrotik-routeros-package-channel-bugfix-only-current-release-candidate-legacy/
- Paquetes y downgrade: https://manual.mikrotik.com/docs/7.25/getting-started/installation-and-upgrade/packages/
