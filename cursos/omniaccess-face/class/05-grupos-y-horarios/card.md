# Lección 5. Grupos y horarios

**Escuchá:** grupos-y-horarios.mp3 (2 min)

**La idea, en tres líneas**
- Grupos de Acceso junta personas y equipos ("Personas del grupo × equipos del grupo = quién pasa por dónde"); en la ficha de cada persona muestra a qué equipos alcanza su grupo.
- El grupo da el permiso, pero la cara llega al terminal por "A qué equipos se manda": en esta versión el grupo no copia nada solo.
- OmniAccess manda cada persona al Akuvox con el horario "siempre" del equipo; un horario por persona se configura en el propio terminal y conviene revisarlo cada vez que se reenvía la persona.

**Impacto:** el permiso queda ordenado y documentado en el sistema, y el horario que se cumple es uno que podés mostrar en el equipo.

**Quién lo dice:** el código de OmniAccess (grupos, envío al terminal, modelo de horarios sin pantalla) y la guía rápida de Hikvision, que recomienda combinar modos de autenticación cuando hace falta más seguridad; ninguna fuente leída describe horarios para Face dentro de OmniAccess.

**Laboratorio** · Admin · 20 min
Con la persona de prueba de la lección anterior (Ana Ejemplo) y el terminal Portería peatonal:
1. Creá el grupo:
```text
Gestión → Grupos de Acceso → Crear grupo
Nombre: Limpieza con horario
Personas: Ana Ejemplo
Equipos: Portería peatonal
Guardar
```
2. Abrí la ficha de Ana y mirá en "A qué equipos se manda" qué equipos alcanza el grupo. Compará con los terminales marcados en "Terminales de rostro": son dos listas distintas.
3. En la web del terminal, creá un horario de lunes a viernes de 8:00 a 17:00 y asignáselo a Ana (cómo se hace en el equipo: curso Porteros IP Akuvox, lección Usuarios y horarios).
4. Probá la cara dentro y fuera del horario (en el laboratorio podés correr el reloj del horario en lugar de esperar). Mirá qué evento llega al Monitor Facial en cada caso y anotalo.
5. Desde OmniAccess, cambiá algo de la ficha de Ana y volvé a mandarla al terminal. Revisá en la web del equipo si el horario sigue asignado.
6. Anotá en la ficha de la obra qué personas tienen horario en el terminal y quién lo cargó.

⚠️ OmniAccess manda a la persona con el horario "siempre" del equipo (1001 en Akuvox). Si el envío actualiza a alguien que ya existía en el terminal, puede pisar el horario que cargaste a mano: revisalo después de cada reenvío.

**Regla para quedarse**
El horario que se cumple es el que está en el terminal: documentalo y revisalo después de cada envío.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Guía rápida Hikvision: autenticación combinada cuando hace falta más seguridad: https://pinfo.hikvision.com/hkwsen/unzip/20260304161336_58290_doc/UD24344B-E_Baseline_DS-K1T343%20Series%20Face%20Recognition%20Terminal_Quick%20Start%20Guide_V1.1_20250107.pdf
- Parámetros del terminal Hikvision (seguridad 1:N y 1:1, intervalo, distancia): https://enpinfo.hikvision.com/hkwsen/unzip/20251224164304_81809_doc/GUID-9F07C169-0B01-4F3E-8729-0BD5189C7613.html
