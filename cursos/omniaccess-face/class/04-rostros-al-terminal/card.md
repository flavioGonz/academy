# Lección 4. Rostros al terminal

**Escuchá:** rostros-al-terminal.mp3 (2 min)

**La idea, en tres líneas**
- La ficha de la persona (Usuarios & Residentes) guarda la foto; la sección "A qué equipos se manda → Terminales de rostro" la copia a la memoria de cada terminal elegido.
- La foto sirve si es frontal, de una sola cara, con luz pareja, sin lentes oscuros ni gorro; para Akuvox, JPG de menos de 200 KB y al menos 640x480.
- Memoria Flash muestra lo que el terminal tiene de verdad: el Directorio, la inyección de personas, el volcado de toda la base y la importación desde el equipo.

**Impacto:** la persona entra el mismo día que se la da de alta, y cuando no entra sabés si el problema es la foto, la copia o el equipo.

**Quién lo dice:** 5 de 5 fuentes (Control iD, Hikvision, Synerion, ClockRite, guía rápida Hikvision) coinciden en la foto frontal con luz pareja; 4 de 4 piden JPG pero discrepan en peso y resolución (Speco menos de 70 KB, Hikvision 40 a 200 KB, Control iD hasta 1920x1080).

**Laboratorio** · Foco · 20 min
Con el terminal del laboratorio anterior dado de alta y una persona de prueba que aceptó participar:
1. Sacá la foto: de frente, a la altura de los ojos, fondo claro, sin contraluz. Bajala a JPG de menos de 200 KB.
2. Creá la ficha:
```text
Gestión → Usuarios & Residentes → pestaña Residentes → Nuevo residente
Nombre: Ana Ejemplo    Unidad: Lote 12 (Barrio Ejemplo)
Foto: Subir foto
A qué equipos se manda → Terminales de rostro: Portería peatonal
Guardar
```
3. Mirá los pasos que muestra el cajón al guardar: "Crear la ficha", "Subir la foto", "Enviar el rostro a Portería peatonal". Si el último falla ("El terminal no aceptó el rostro."), el cajón queda abierto con el error.
4. Abrí la memoria del equipo y buscala:
```text
Gestión → Dispositivos Faciales → ⋯ → Memoria Flash → Directorio
```
Tiene que aparecer con foto. El ID en el equipo es un número de 9 dígitos que OmniAccess calcula a partir de la ficha: no lo cambies a mano en el terminal.
5. Volvé a la lista de dispositivos: el contador Faces subió en uno.
6. Probá la cara en el terminal y mirá el evento en el Monitor Facial.
7. Opcional, en demo: en Memoria Flash probá "Descargar Equipo a App" (Modo Importación Inteligente) para ver qué identidades tiene el equipo que la base no tiene.

⚠️ "Volcar Base de Datos a Equipo" (Modo Sobrescritura) manda a ese terminal a todas las personas con foto o tarjeta de la base. En un barrio con varios accesos puede cargar gente donde no corresponde: usalo solo cuando ese terminal es para todos.

**Regla para quedarse**
La persona está enrolada cuando aparece en la memoria del terminal, no cuando se guardó la ficha.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Requisitos de la foto de alta en un terminal Hikvision (formato, resolución y peso): https://enpinfo.hikvision.com/unzip/20201102205526_84041_doc/GUID-1C74D204-C508-44DA-B19A-411FF9D7C050.html
- Importar fotos por lote y "Verify by Device" (Hikvision): https://enpinfo.hikvision.com/unzip/20201102205526_84041_doc/GUID-981B3FAD-F5BA-4E59-8D03-58DB01122125.html
- Fotos de enrolamiento: una cara, de frente, luz pareja (Control iD): https://www.controlid.com.br/docs/access-api-en/facial-recognition/recommendations-photos-install/
- Otro fabricante, otro límite de peso (Speco): https://info.specotech.com/how-to-upload-images-for-facial-recognition
