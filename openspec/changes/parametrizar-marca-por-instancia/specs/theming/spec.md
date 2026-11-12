# Spec Delta

## Purpose
Definir cómo la plataforma resuelve y aplica la identidad de marca de cada
instancia (IES, Infratec u otra futura) desde una única fuente de verdad, para
que un mismo código sirva varias marcas sin duplicar ramas ni hardcodear valores.

## ADDED Requirements

### Requirement: Fuente única de tema por instancia
El sistema SHALL obtener toda la identidad de marca (nombre visible, dominios,
paleta de color, tipografías, logo claro/oscuro, monograma/favicon y textos
legales) de un único recurso de tema asociado a la instancia, resuelto en tiempo
de ejecución.

#### Scenario: La instancia define su marca
- **WHEN** la aplicación arranca en una instancia con un tema configurado
- **THEN** la UI muestra el nombre, los colores, los logos y los textos de ese
  tema, sin requerir cambios en el código de la aplicación

#### Scenario: Instancia sin tema propio
- **WHEN** no hay tema configurado para la instancia
- **THEN** el sistema aplica un tema por defecto documentado y registra una
  advertencia, sin romper la carga de la página

### Requirement: Sin valores de marca hardcodeados
El código de presentación (HTML, CSS, JS) y los endpoints SHALL tomar los valores
de marca del tema en lugar de literales fijos, de modo que ninguna cadena, color o
logo de una marca aparezca embebido fuera del recurso de tema.

#### Scenario: Rebrand sin tocar el motor
- **WHEN** se cambia un color, el nombre o un logo en el recurso de tema
- **THEN** el cambio se refleja en toda la UI sin editar `styles.css`, `app.js`
  ni los archivos PHP

#### Scenario: No se filtra la marca equivocada
- **WHEN** se renderiza cualquier pantalla de una instancia
- **THEN** no aparece ningún nombre, color ni logo de otra marca

### Requirement: El contrato funcional no depende de la marca
Los identificadores técnicos que la API necesita para operar (por ejemplo el
encabezado `X-IES` de las llamadas) SHALL permanecer estables e independientes de
la marca visible, para no romper el backend al rebrandear.

#### Scenario: Cambiar la marca no cambia el contrato
- **WHEN** se aplica un tema distinto a una instancia
- **THEN** los contratos de la API (encabezados, nombres de campos, rutas) siguen
  funcionando sin cambios
