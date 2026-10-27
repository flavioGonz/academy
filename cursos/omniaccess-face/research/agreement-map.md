# Mapa de acuerdos (versión compacta)

Conteos sobre las fuentes web que tocan cada tema. El producto (código y manuales de OmniAccess) es la fuente de verdad para pantallas y flujos y no entra en el conteo.

1. **El terminal decide y abre; la plataforma registra.** Producto (textos de Modo Face: "La cámara controla la apertura física"). Web: Hikvision Biometric (el umbral vive en el equipo), CIE (las reglas actúan sobre eventos del equipo). 2 de 2. Nivel inicial.
2. **Altura del terminal.** Control iD 1,30 m; Synerion cámara a 1,48 m para 1,50 a 2,00 m; Hikvision personas de 1,4 a 1,9 m a 0,5 m; ClockRite 1,1 m mirando hacia abajo. 4 de 4 dan altura fija pensada para un rango de estaturas; discrepan en el número (1,1 a 1,48 m).
3. **Sin sol ni contraluz, con luz frontal.** Control iD, Synerion, ClockRite, Hikvision QSG, Hikvision Biometric (WDR afuera). 5 de 5.
4. **Distancia de reconocimiento de unos 0,5 m.** Synerion (50 cm, disparo a ~35 cm), ClockRite (0,5 m), Hikvision QSG (0,5 m), Hikvision Biometric (distancia configurable). 4 de 4.
5. **Ángulo del rostro limitado.** Senstar (giro 45°, inclinación 20°), Control iD (mirando de frente), Hikvision QSG (postura). 3 de 3.
6. **Foto de alta frontal, una sola cara, luz pareja, sin lentes oscuros ni gorro.** Control iD, Hikvision Import Data, Synerion, ClockRite (sin barbijo), Hikvision QSG. 5 de 5.
7. **Tamaño y formato de la foto.** Hikvision 40 a 200 KB y 640x480 a 2160x3840; Hikvision ZIP hasta 200 KB; Control iD 160x160 a 1920x1080 sin límite de peso dado; Speco menos de 70 KB. 4 de 4 piden JPG; discrepan en peso y resolución: cada equipo tiene su límite. Producto: Akuvox JPG < 200 KB, mínimo 640x480.
8. **Verificar que el equipo reconoce la foto al cargarla.** Hikvision Import Person Pictures (Verify by Device), Hikvision QSG (ver la captura antes de guardar). 2 de 2.
9. **Volver a enrolar cuando cambia la cara.** Synerion (barba), ClockRite (barbijo). 2 de 2.
10. **Umbral: subirlo baja falsas aceptaciones y sube falsos rechazos.** Hikvision Biometric, AWS, NIST FRTE (definición de FMR y FNMR). 3 de 3.
11. **El valor del umbral depende del uso.** AWS (80 % fotos familiares, 99 % policial), Hikvision (nivel 1:N y 1:1 separados). 2 de 2. Ningún valor universal.
12. **Antisuplantación ayuda pero no es infalible.** Synerion ("no atrapa todo"), Hikvision QSG ("no 100 %", combinar modos), Senstar (apagada por defecto). 3 de 3.
13. **Diferencias demográficas en los algoritmos.** NIST 2019, infodocket. 2 de 2; los mejores algoritmos son también los más equitativos. Voz crítica.
14. **Webhook: el equipo avisa por HTTP a una URL.** Wikipedia, CIE (webhooks de Smart Access). 2 de 2. Producto: Action URL con variables al puerto 10000.
15. **Cloud contra local para eventos.** CIE describe reglas en Smart Access Cloud; el producto usa Action URL local. División: decidir por dónde vive el servidor.
16. **Video en vivo por un servidor de streams.** go2rtc README (MJPEG, snapshot, FFmpeg). 1 de 1. Producto: stream face_<id>.
17. **Push web con permiso del usuario.** MDN. 1 de 1. Producto: la PWA se suscribe; no hay envío por eventos faciales en esta versión.
18. **Dato biométrico definido por ley en Uruguay.** IMPO art. 4 lit. Ñ (Ley 19.924, 2020), Dictamen URCDP 3/023. 2 de 2.
19. **Consentimiento libre, previo, expreso, informado y documentado.** IMPO art. 9, Dictamen 3/023, Synerion (consentimiento con plazo de retención). 3 de 3.
20. **Evaluación de impacto previa con biometría (art. 18 bis) e inscripción de la base.** Dictamen 3/023. 1 de 1, del regulador.
21. **Datos sensibles: nadie obligado, consentimiento escrito.** IMPO art. 18. 1 de 1. Que el dato facial de acceso sea sensible no lo dice ninguna fuente leída: no se afirma.
22. **El consentimiento laboral no alcanza solo.** CSO Online (GDPR): hace falta alternativa sin castigo. 1 de 1. Discrepa de "firma y listo".
23. **Retención automática por días.** MinIO (expire-days sobre bucket o ruta), Synerion (período de retención). 2 de 2. Producto: la regla del Bucket FACE cubre todo el bucket.
24. **Ciclo de vida completo: alta, uso, baja, borrado.** Dictamen 3/023 (análisis del ciclo de vida), Synerion. 2 de 2. Producto: borrar la ficha no borra la cara del terminal ni la foto.
25. **Varios factores para más seguridad.** Hikvision QSG. 1 de 1. Producto: el usuario Akuvox lleva tarjeta y PIN junto con la cara.
26. **Limpieza de la ventana de la cámara.** Synerion. 1 de 1.
27. **Accesibilidad: alturas y sillas de ruedas.** Synerion (brazo VESA). 1 de 1.

## Divisiones
- Altura de montaje: 1,1 m (ClockRite) contra 1,30 m (Control iD) contra cámara a 1,48 m (Synerion). Decidir con la ficha del modelo y probar con la persona más baja y la más alta del lugar.
- Peso de la foto: 70 KB (Speco) contra 200 KB (Hikvision, Akuvox). Decidir por el equipo destino; en OmniAccess conviene quedar por debajo de 200 KB.
- Consentimiento como base suficiente: Ley 18.331 lo pone como regla general con excepciones; CSO (GDPR) advierte que en relación laboral no es libre. Decidir con el responsable de la base y su asesor: ofrecer alternativa (tarjeta o PIN).
- Eventos en nube (Smart Access) o locales (Action URL): OmniAccess usa local; la nube depende de la suscripción del cliente.
