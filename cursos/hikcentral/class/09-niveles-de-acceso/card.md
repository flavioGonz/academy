# Lección 9. Niveles de acceso

**Escuchá:** niveles-de-acceso.mp3 (2 min)

**La idea, en tres líneas**
- Persona con credencial (tarjeta, huella, rostro, PIN o QR) + nivel de acceso (puertas + plantilla de horario) + asignación a persona o departamento.
- Nada llega a la puerta hasta aplicar a los dispositivos: "aplicar cambios" manda solo lo modificado; "Apply (Initial)" borra y reescribe todo.
- Durante el Apply (Initial) los dispositivos quedan offline y nadie pasa: fuera de horario.

**Impacto:** se terminan los "le di permiso y no le abre" y nadie deja un hall trancado en hora pico.

**Quién lo dice:** 1 de 3 fuentes de control de acceso describe el aplicado (manual del Web Client) y el FAQ suma usar una sola fuente de alta de personas; ambas de Hikvision, evidencia fina. No se encontró quien discrepe.

**Laboratorio** · Campo · 20 min
1. Persona de prueba: Person > Add. Nombre "Prueba Lab", ID 9001, tarjeta 0001234567 (o la que tengas en la mano).
2. Plantilla de horario de acceso: lunes a viernes, 08:00 a 19:00.
3. Access Level > Add: nombre "Oficina hábil", puerta de la controladora de laboratorio, plantilla anterior. Asignalo a "Prueba Lab".
4. Aplicá (en V2.x: Passing Management > Access Control > Access Level > Apply Access Level Settings):
```text
Persons:                 Specified Persons > Prueba Lab
Specified Access Point:  on > Puerta Lab
Apply (Initial):         sin marcar
```
5. Pasá la tarjeta dentro y fuera del horario y mirá el registro de acceso.
6. Cambiá el horario a 08:00 a 12:00, fijate el ícono de pendiente junto a Apply y aplicá de nuevo. Si falla, Access Control Test.

⚠️ Apply (Initial) deja las controladoras offline mientras reescribe: solo fuera de horario y con aviso al cliente.

**Regla para quedarse**
Nada cambia en la puerta hasta que aplicás, y el aplicado inicial va fuera de horario.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Aplicar niveles de acceso a dispositivos, inicial y por cambios (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-3F50D8C7-95C9-478B-B4D5-189A09C3D708.html
- Una sola fuente de personas y reglas de ID (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
- Credenciales y funciones de la línea de acceso (ficha de HikCentral Access Control): https://www.securityinformed.com/hikvision-hikcentral-access-control-software-technical-details.html
