# Lección 11. Roles y cuentas

**Escuchá:** roles-y-cuentas.mp3 (2 min)

**La idea, en tres líneas**
- Administrator y Operator son fijos; los roles a medida definen vigencia, plantilla horaria de permisos, áreas visibles y permisos de recursos y configuración.
- Si el rol vence o queda fuera de horario, el usuario es expulsado: sirve para contratistas y turnos.
- Endurecé: contraseña mínima Strong (por defecto es Medium), HTTPS con certificado .pem propio y nada expuesto a internet sin necesidad.

**Impacto:** cada acción queda asociada a una persona y un operador solo ve lo que le toca.

**Quién lo dice:** 2 de 5 fuentes describen los roles así (manual del Web Client y FAQ) y 4 de 5 coinciden en endurecer el acceso (FAQ, soporte de Hikvision USA, Quick Start y learncctv). La voz crítica, learncctv, recuerda el historial de seguridad de Hikvision: un motivo más para no dejar el sistema con valores por defecto.

**Laboratorio** · Admin · 15 min
1. Web Client > Account and Security > Roles > Add (V2.x):
```text
Role name:                   Guardia
Effective period:            hoy a fin de año
Permission schedule:         nuevo, todos los días 19:00 a 07:00
Area display rule:           solo Depósito
Resource access:             vivo y reproducción de cámaras de Depósito
```
2. Users > Add: usuario "guardia.lab", contraseña de ejemplo `Turno.Noche.2026`, rol Guardia.
3. Security Settings: fuerza mínima de contraseña Strong.
4. Entrá con guardia.lab dentro y fuera del horario y compará lo que ves.
5. Opcional (HTTPS): con el certificado .crt de la CA y la clave privada en texto, armá un .pem así y subilo en System > Advanced > Transfer:
```text
-----BEGIN CERTIFICATE-----
(contenido del .crt)
-----END CERTIFICATE-----
-----BEGIN PRIVATE KEY-----
(clave privada exportada)
-----END PRIVATE KEY-----
```

⚠️ La clave privada no se manda por correo ni se pega en conversores online de terceros con datos de un cliente: convertila en una PC de confianza.

**Regla para quedarse**
Cada persona su usuario, cada usuario el rol mínimo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Roles, vigencia, horario de permisos y áreas visibles (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-6C43765F-0DD8-43CF-ADF0-5918B47787D1.html
- Certificado HTTPS en formato .pem (soporte de Hikvision USA): https://supportusa.hikvision.com/support/solutions/articles/17000110020-how-to-generate-and-install-https-certificate-for-hikcentral
- La mirada crítica sobre seguridad de Hikvision: https://learncctv.com/hikvision-cameras-removed-us-army-base-security-issues/
