# Lección 5. Tres formas de alta

**Escuchá:** tres-formas-de-alta.mp3 (2 min)

**La idea, en tres líneas**
- IP o dominio cuando hay IP fija y ruta al equipo: protocolo privado Hikvision, puerto 8000 (8443 con Encrypted Add); ONVIF para terceros.
- ISUP (ex EHome) cuando el equipo no tiene IP fija: el equipo registra hacia el SYS (puerto 7660) con Device ID y clave.
- Hik-Connect DDNS como atajo con serie y código de verificación, pero esos equipos no graban en Hybrid SAN ni Cloud Storage.

**Impacto:** cada sitio entra con el método que corresponde y no se abren puertos de más en el router del cliente.

**Quién lo dice:** IP 3 de 7, ISUP 2 de 7 y Hik-Connect 2 de 7 fuentes de alta de dispositivos, todas de Hikvision (manual del Web Client, Communication Matrix V2.4.1, FAQ). Discrepa learncctv, que enseña port forwarding directo de los puertos del equipo.

**Laboratorio** · Campo · 20 min
1. SYS de laboratorio en 192.168.88.10. Web Client > System > Network > Device Access Protocol: activá Allow ISUP Registration y guardá (ruta de V2.x).
2. En la cámara de laboratorio (su web local): Configuración > Red > Avanzado > Platform Access, tipo ISUP. Cargá:
```text
Server address:  192.168.88.10
Port:            7660
Device ID:       LAB-CAM-01
Key / password:  Ejemplo.2026!
```
3. En HikCentral: Device > Encoding Device > Add > Access Protocol: Hikvision ISUP Protocol > Device ID: LAB-CAM-01, misma clave (ISUP 5.0).
4. Activá Add Resource to Area y elegí o creá un área.
5. Si no aparece online, probá el puerto desde una PC de la misma red:
```powershell
Test-NetConnection 192.168.88.10 -Port 7660
```
6. Para comparar, agregá otra cámara por IP: Access Protocol Hikvision Private Protocol, Device Address 192.168.88.21, puerto 8000.

⚠️ No abras el 8000 ni el 80 del equipo a internet para "probar rápido": si hace falta acceso remoto, VPN o ISUP.

**Regla para quedarse**
IP fija, por IP; sin IP fija, ISUP; Hik-Connect solo si aceptás sus límites de grabación.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Alta por Device ID con ISUP (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-5A97A28D-C1DB-4653-B440-FAAC67F3FDE2.html
- Alta por IP o dominio, puertos 8000 y 8443 (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-76D11646-EA40-4EDA-88DD-38821CB5826E.html
- Alta por Hik-Connect DDNS: https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-8F21FBEB-1F47-4246-A13A-0804154D9DFE.html
