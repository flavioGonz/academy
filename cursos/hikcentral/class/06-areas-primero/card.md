# Lección 6. Áreas primero

**Escuchá:** areas-primero.mp3 (2 min)

**La idea, en tres líneas**
- Un equipo agregado sin importar sus canales a un área no tiene vivo, reproducción ni eventos.
- Las cámaras de un área hija no aparecen al abrir el área madre: cada recurso va en el área donde se usa.
- Vistas públicas para el puesto de monitoreo, privadas por operador; E-map para planos fijos, GIS para mapas geográficos vivos.

**Impacto:** cámaras que aparecen donde el operador las busca y permisos por área que se arman solos.

**Quién lo dice:** 3 de 7 fuentes de alta de equipos coinciden en importar a un área (manual del Web Client); lo del área hija, las vistas y los mapas sale solo del FAQ V2.5.500 (evidencia fina, oficial). No se encontró quien discrepe.

**Laboratorio** · Rápido · 15 min
1. En papel, diseñá el árbol antes del alta:
```text
Sitio Ejemplo
├── Depósito
│   ├── Nave 1   (CAM-01..04, Puerta N1)
│   └── Nave 2   (CAM-05..08, Puerta N2)
└── Oficinas     (CAM-09..10, Puerta OF)
```
2. Web Client > Area Management > Add Area: creá las áreas del dibujo (nombre del menú según V2.x).
3. En cada equipo ya agregado: importá sus canales al área que corresponde (Add Resource to Area o Import en el área).
4. En el Control Client > Monitoring: creá una vista pública de 4 ventanas con las cámaras de Nave 1.
5. Doble clic en Depósito: si dice que no hay cámaras, recordá que están en las hijas.
6. Opcional: cargá un plano JPG de la planta como E-map del área y ubicá cada cámara como punto caliente.

**Regla para quedarse**
El árbol de áreas se diseña antes de dar de alta el primer equipo.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Importar recursos a un área al dar de alta (manual del Web Client): https://enpinfo.hikvision.com/hkwsen/unzip/20230830144955_12918_doc/GUID-76D11646-EA40-4EDA-88DD-38821CB5826E.html
- Áreas hijas, vistas públicas y privadas, E-map y GIS (FAQ V2.5.500): https://pinfo.hikvision.com/hkwsen/unzip/20240603152919_44907_doc/UD38113B_HikCentral%20Professional%20V2.5.500_FAQ_V2.5.500_20240603.pdf
