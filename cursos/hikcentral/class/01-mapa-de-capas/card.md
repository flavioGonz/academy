# Lección 1. Mapa de capas

**Escuchá:** mapa-de-capas.mp3 (2 min)

**La idea, en tres líneas**
- El SYS (System Management Service) gestiona usuarios, roles, dispositivos y la base de datos, y trae adentro un Streaming Gateway para el video.
- El Web Client configura, el Control Client opera (vivo, PTZ, reproducción, alarmas) y el Mobile Client acompaña en el celular.
- Professional es el producto grande de la familia; HikCentral Lite y HikCentral Access Control cubren sitios chicos, y Connect y FocSign apuntan a otros usos (nube y cartelería).

**Impacto:** el diagnóstico arranca en la capa correcta y se ahorran vueltas en soporte.

**Quién lo dice:** 3 de 4 fuentes de arquitectura coinciden, todas de Hikvision (Quick Start, FAQ, guía de requisitos); no se encontró quien discrepe. Aplica a la documentación V2.x; en V3.x los componentes son los mismos.

**Laboratorio** · Rápido · 10 min
1. En una hoja, dibujá las capas de una obra real:
```text
Cámaras, NVR, controladoras
        |
SYS + Streaming Gateway (hasta ~200 cámaras reenviadas, según el FAQ)
        |
Streaming Server en otra máquina (solo si hace falta)
        |
Web Client (configura) · Control Client (opera) · Mobile Client
```
2. Al lado de cada capa, anotá quién la mantiene (vos, el cliente, IT).
3. Si tenés un SYS de laboratorio (por ejemplo 192.168.88.10), abrí Service Manager con clic derecho > Ejecutar como administrador y anotá cada servicio, su estado y su puerto. Un puerto en rojo indica conflicto.
4. Mirá qué escucha el servidor desde PowerShell:
```powershell
Get-NetTCPConnection -State Listen | Where-Object LocalPort -in 80,443,554,559,7660 | Select-Object LocalPort, OwningProcess
```
5. Compará la versión del SYS (Web Client, página de inicio) con la del Control Client instalado en el puesto. Si no coinciden, ese es el error VSM217.

⚠️ Service Manager permite detener servicios: en un servidor en producción, solo mirar.

**Regla para quedarse**
Antes de diagnosticar, ubicá la capa: equipo, SYS, streaming o cliente.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Componentes, paquetes de instalación y Service Manager (Quick Start Guide): https://pinfo.hikvision.com/hkwsen/unzip/20230911113416_60121_doc/pdf.pdf
- Streaming Gateway, Control Client en VM y error VSM217 (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
