# Lección 8. Visitas y bloqueos

**Escuchá:** visitas-y-bloqueos.mp3 (2 min)

**La idea, en tres líneas**
- Una visita frecuente (niñera, obrero de una reforma, familiar) se da de alta en la pestaña Visitas, se manda al terminal mientras dure y se le saca la cara cuando termina.
- Bloquear a alguien en Face es sacar su cara de la memoria del terminal (Memoria Flash → Directorio): marcarlo o cambiar el Modo Face cambia el registro, no la puerta.
- Borrar la ficha en OmniAccess no borra la cara del terminal ni su foto guardada: la baja va primero en el equipo y después en la ficha.

**Impacto:** nadie queda entrando meses después de terminar su trabajo, y cuando la administración pide un bloqueo, el bloqueo es real.

**Quién lo dice:** el código de OmniAccess (roles, Memoria Flash, borrado de fichas) y 2 de 2 fuentes que piden pensar el ciclo de vida completo de los datos: el Dictamen 3/023 de la URCDP y la guía de Synerion (consentimiento con período de retención).

**Laboratorio** · Admin · 20 min
En una demo con el terminal Portería peatonal:
1. Alta de la visita:
```text
Gestión → Usuarios & Residentes → pestaña Visitas → Nueva visita
Nombre: Obrero Ejemplo   Unidad: Lote 12
Foto: Subir foto (con el consentimiento de la lección 7)
A qué equipos se manda → Terminales de rostro: Portería peatonal
Guardar
```
2. En la ficha anotá en observaciones hasta cuándo dura el trabajo (por ejemplo "reforma hasta el 30/11"). Probá que el terminal lo reconoce.
3. Simulá el fin del trabajo. Primero sacalo del equipo:
```text
Gestión → Dispositivos Faciales → ⋯ → Memoria Flash → Directorio
Buscar: Obrero Ejemplo → eliminar  → "Rostro eliminado correctamente"
```
4. Probá la cara: el terminal ya no lo reconoce y, si cargaste la Action URL de Invalid Face, el evento llega como rostro desconocido.
5. Recién ahora decidí qué pasa con la ficha. Ojo: borrarla también borra sus eventos del Historial (la base los elimina junto con la persona). Si la administración necesita conservar ese historial, dejá la ficha sin terminales marcados.
6. Repetí el paso 3 para un "bloqueo": elegí una persona de prueba, sacala del terminal y comprobá que no abre aunque el Modo Face siga igual.

⚠️ En esta versión, Invitados (pases con QR o matrícula) aparece solo con el módulo LPR, y el QR que lee un Akuvox llega como "Código QR Válido" sin cruzarse con esas invitaciones: no prometas pases por QR en el terminal facial sin confirmarlo en tu instalación.

**Regla para quedarse**
La baja se hace primero en el terminal y después en la ficha.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- URCDP, Dictamen 3/023: ciclo de vida de los datos biométricos: https://www.gub.uy/unidad-reguladora-control-datos-personales/institucional/normativa/dictamen-n-3023-0
- Consentimiento con período de retención y qué hacer si alguien no acepta (Synerion): https://help.synerion.com/agile/knowledge-base/gt-installation-guidelines
