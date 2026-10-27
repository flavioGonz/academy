# Lección 5. Patrón y privilegio

**Escuchá:** patron-privilegio.mp3 (2 min)

**La idea, en tres líneas**
- Patrones con guion bajo: X (0 a 9), Z (1 a 9), N (2 a 9), punto (uno o más). Strip saca el prefijo de salida.
- Privilegios Internal < Local < National < International: la extensión usa la ruta si su nivel es igual o mayor.
- La ruta internacional lleva PIN y privilegio International; y un troncal de failover por si el principal cae.

**Impacto:** el fraude con una extensión robada choca contra el privilegio y el PIN, y las salientes siguen si cae un troncal.

**Quién lo dice:** 4 de 5 fuentes coinciden en privilegio y PIN en rutas caras; Simtex y el manual difieren en el orden de rutas (primera que matchea contra Outgoing Routing Priority configurable).

**Laboratorio** · Foco · 15 min
1. Ruta nacional (ejemplo con numeración uruguaya: fijos de 8 dígitos que empiezan con 2 o 4, celulares 09 más 7 dígitos; ajustá a tu plan):
```text
Extension/Trunk > Outbound Routes > Add
Outbound Rule Name: nacional
Pattern: _[24]XXXXXXX
         _09XXXXXXX
Privilege Level: National
Trunk: Proveedor_Lab
```
2. Ruta internacional con PIN:
```text
Outbound Rule Name: internacional
Pattern: _00X.
Privilege Level: International
Password Settings: PIN Groups (creá antes el grupo en Outbound Routes > PIN Groups)
```
3. Si el cliente marca 9 para salir: patrón `_9NXXXXXXX` con Strip 1.
4. Agregá un troncal de failover en la ruta nacional, si tenés un segundo troncal de prueba.
5. Revisá cómo prioriza tu central: botón Outgoing Routing Priority en la página de Outbound Routes.
6. Poné una extensión en privilegio Local y marcá un número internacional: tiene que rechazarse.

**Regla para quedarse**
La ruta internacional nace con PIN y privilegio International, nunca con un patrón que agarre todo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Permisos de rutas salientes y fraude de peaje: https://documentation.grandstream.com/knowledge-base/ucm6xxx-security-manual/
- Patrones, strip y failover con ejemplos: https://support.telnyx.com/en/articles/5748258-grandstream-configuring-sip-trunks-on-your-grandstream-ucm6xxx-series
- Rutas salientes y Outgoing Routing Priority: https://documentation.grandstream.com/knowledge-base/ucm630x-series-user-manual/
