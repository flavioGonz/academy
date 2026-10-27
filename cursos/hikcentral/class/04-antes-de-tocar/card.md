# Lección 4. Antes de tocar

**Escuchá:** antes-de-tocar.mp3 (2 min)

**La idea, en tres líneas**
- En máquina física la licencia queda atada al hardware; migrar la VM del SYS también rompe la verificación de licencia.
- Antes de cambiar hardware, mover o actualizar: backup del sistema, copia fuera del SYS y licencia desactivada.
- El backup se programa en el Web Client (1 a 5 copias) y queda guardado en el propio servidor SYS, por eso se copia afuera.

**Impacto:** un cambio de disco o de servidor no termina en un SYS que no arranca ni en un sistema sin configuración.

**Quién lo dice:** 4 de 5 fuentes de licencias coinciden en desactivar antes de cambiar hardware (guía de requisitos, manual, FAQ, Quick Start, todas de Hikvision); sobre backups, 3 de 4, incluida VXG, que recuerda que esa carga queda del lado del integrador. Nadie discrepa.

**Laboratorio** · Admin · 15 min
1. Web Client > Maintenance and Management > Back Up and Restore System Data > pestaña Back Up (V2.6.1; en V3.x el nombre del menú puede variar).
2. En Type marcá configuración, imágenes, eventos y alarmas, y pasadas. How Often: semanal; When: domingo 03:00; Max. Number of Backups: 5. Clic en Save and Back Up Now.
3. Copiá la carpeta de backups a otra máquina (ruta de ejemplo, ajustala a la que muestra la pestaña):
```powershell
robocopy "D:\HikCentral\Backup" "\\192.168.88.20\backups\hcp" /E /R:2 /W:5
```
4. Escribí el checklist de cambio y pegalo en la carpeta de la obra:
```text
1. Backup del sistema ahora (Save and Back Up Now)
2. Copia del backup fuera del SYS y verificada
3. Licencia desactivada (online u offline)
4. Apagar, cambiar hardware o migrar
5. Encender, reactivar licencia, revisar Service Manager
```

⚠️ En producción, el paso 3 del checklist lo hace solo quien tiene los códigos de licencia y el visto bueno del cliente.

**Regla para quedarse**
Antes de tocar el servidor: backup afuera y licencia desactivada. Siempre.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Backup programado y dónde se guarda (manual del Web Client V2.6.1): https://pinfo.hikvision.com/hkwsen/unzip/20240822164538_35347_doc/GUID-1AF31681-DD4C-4819-B85A-74A0178F87E8.html
- Migración de VM y licencia (guía de requisitos V2.4.510): https://pinfo.hikvision.com/hkwsen/unzip/20230911113613_29615_doc/HikCentral%20Professional_System%20Requirements%20and%20Performance_V2.4.510_20230907.pdf
- SYS en loop y error 1108 (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
