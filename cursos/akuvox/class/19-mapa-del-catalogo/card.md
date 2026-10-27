# Lección 19. Mapa del catálogo

**Escuchá:** mapa-del-catalogo.mp3 (2 min)

**La idea, en tres líneas**
- Lo vigente sale del menú de productos de akuvox.com; los datos transversales (alimentación, relé, métodos de acceso, 12 V, interfaces) salen de las tablas de la Knowledge Base.
- El menú ordena por tipo (porteros, monitores, panel AKClaw, casa inteligente, cuidado de mayores, 2 hilos, kits, acceso, teléfono Android, teléfonos IP, cámara, software, accesorios) y lista versiones: el sufijo (R29S, R29C-L, X915P, E16P) cambia funciones.
- E16 y C316 siguen en el menú al 27 de octubre de 2026; E11, C315 o IT83 están en tablas de la Knowledge Base pero no en el menú. No hay lista oficial de discontinuados en lo leído.

**Impacto:** cada cotización y cada reemplazo arranca de una planilla verificada, no de memoria.

**Quién lo dice:** 3 de 7 fuentes coinciden en separar catálogo vigente y parque instalado (menú de akuvox.com, guía de firmware de Akuvox, ejemplo de ComfortClick); ninguna discrepa.

**Laboratorio** · Admin · 15 min
1. Abrí el menú de productos de akuvox.com y copiá los modelos por tipo.
2. Armá la planilla:
```text
Modelo | Tipo     | Serie | Sistema | PoE (tabla)  | Relé (tabla) | En el menú hoy
R29    | Portero  | R     | Android | 802.3at      | 30 V 3 A     | sí
E16C   | Portero  | E     | Linux   | 802.3af      | 30 V 2 A     | sí
C315   | Monitor  | C     | (ver)   | (ver)        | 30 V 2 A     | no
```
3. Completá `PoE` con la tabla de alimentación y `Relé` con la de carga resistiva; si un dato no aparece, escribí "sin dato", no lo supongas.
4. Marcá en otro color las versiones con sufijo que cambian funciones (LTE, huella, palma, HID).
⚠️ "No está en el menú" no es lo mismo que "sin soporte": antes de decírselo a un cliente, consultá al distribuidor.

**Regla para quedarse**
Vigente es lo que está en el menú del fabricante el día que cotizo; todo lo demás es parque instalado.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Menú de productos de Akuvox: https://www.akuvox.com/products
- Códigos de modelo en el firmware, incluidos los viejos: https://knowledge.akuvox.com/docs/upgrade-devices
- Alimentación por modelo: https://knowledge.akuvox.com/docs/power-supply-for-intercom-devices
