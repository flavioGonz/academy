# Lección 7. Enrolar en portería

**Escuchá:** enrolar-en-porteria.mp3 (2 min)

**La idea, en tres líneas**
- Desde un evento, el botón Registrar abre una ficha nueva con la foto de la captura; si esa foto no sirve (de costado, oscura, con gorro), se cambia por una nueva antes de mandarla al terminal.
- La cara es un dato biométrico según la Ley 18.331 (art. 4, literal Ñ): la persona sabe para qué se usa, quién la guarda y cómo pedir que se borre, y da su consentimiento antes de sacar la foto.
- Siempre hay una alternativa sin cara (tarjeta, PIN o portería) para quien no acepta.

**Impacto:** el alta en portería sale en cinco minutos, con una foto que reconoce a la primera y con el consentimiento guardado.

**Quién lo dice:** 5 de 5 fuentes de fabricantes coinciden en la foto de calidad; 3 de 3 (Ley 18.331 art. 9 en IMPO, Dictamen 3/023 de la URCDP y Synerion) piden consentimiento informado y documentado. CSO Online discrepa de que alcance con una firma: en una relación laboral el consentimiento no es libre si no hay alternativa sin castigo.

**Laboratorio** · Foco · 20 min
En una demo, con un compañero que acepta hacer de visitante frecuente:
1. Leele el texto de consentimiento del lugar (si no existe, este borrador sirve para el laboratorio y lo revisa la administración del barrio):
```text
"Barrio Ejemplo usa reconocimiento facial en la portería peatonal.
Su foto se guarda en el sistema de control de acceso y en el terminal,
solo para abrir esta puerta y registrar los ingresos.
Puede pedir la baja y el borrado en la administración.
Si no acepta, puede entrar con tarjeta o por portería."
```
2. Anotá en la planilla de la portería: nombre, fecha, quién lo leyó y que aceptó.
3. Hacé que pase por el terminal sin estar enrolado y abrí el evento Denegado en el Monitor Facial.
4. En la ficha del evento tocá Registrar: se abre la ficha nueva con la foto de la captura.
5. Mirá la foto con ojo crítico: ¿de frente, una sola cara, luz pareja, sin lentes oscuros? Si no, tocá Cambiar y sacá una nueva.
6. Completá nombre y unidad, y en "A qué equipos se manda" marcá el terminal. Guardá y seguí los pasos hasta "Enviar el rostro".
7. Que vuelva a pasar: el evento tiene que salir Permitido con su nombre.

⚠️ La app Control Facial (/pwa/face) también tiene "Registrar rostro", pero ese registro rápido crea a la persona como visita y no la manda a ningún terminal: para que abra, falta completar la ficha y mandarla.

**Regla para quedarse**
Sin consentimiento informado no se saca la foto, y sin alternativa no se obliga a nadie a dar la cara.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Ley 18.331, art. 4 (definiciones, literal Ñ: datos biométricos): https://www.impo.com.uy/bases/leyes/18331-2008/4
- Ley 18.331, art. 9 (consentimiento previo informado): https://www.impo.com.uy/bases/leyes/18331-2008/9
- URCDP, Dictamen 3/023 sobre biometría facial (evaluación de impacto e inscripción de la base): https://www.gub.uy/unidad-reguladora-control-datos-personales/institucional/normativa/dictamen-n-3023-0
- Consentimiento y biometría en el trabajo (una mirada crítica, GDPR): https://www.csoonline.com/article/565080/biometrics-in-the-workplace-what-about-consent-and-legitimate-interest.html
