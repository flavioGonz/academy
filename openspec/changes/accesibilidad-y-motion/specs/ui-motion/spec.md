# Spec Delta

## Purpose
Definir cómo se comporta el movimiento de la interfaz y su piso de accesibilidad:
transiciones con sentido, retroalimentación de carga, y respeto por las preferencias
de reducción de movimiento.

## ADDED Requirements

### Requirement: Respeto por la reducción de movimiento
Cuando el sistema del usuario indica `prefers-reduced-motion: reduce`, la interfaz
SHALL desactivar las animaciones de transición y SHALL NOT mostrar la barra de
carga animada, dejando los cambios de estado de forma instantánea.

#### Scenario: Usuario con reducción de movimiento
- **WHEN** el usuario tiene activada la preferencia de reducir movimiento
- **THEN** las pestañas y las páginas cambian sin animación y sin barra de carga

#### Scenario: Usuario sin la preferencia
- **WHEN** el usuario no reduce el movimiento
- **THEN** ve las transiciones de entrada y la barra de carga entre páginas

### Requirement: Retroalimentación de carga entre páginas
Al navegar entre páginas, el sistema SHALL mostrar un indicador de carga que inicia
con la navegación y se completa al terminar de renderizar.

#### Scenario: Navegar a otra página
- **WHEN** el usuario navega a una ruta distinta
- **THEN** aparece un indicador de carga que progresa y se completa al cargar la página

### Requirement: Entrada de paneles al cambiar de pestaña
Al cambiar de pestaña, el panel entrante SHALL reproducir una transición de entrada;
el sistema SHALL NOT repetir esa transición cuando el contenido se refresca por una
acción interna de la misma pestaña (por ejemplo marcar una lección o responder el quiz).

#### Scenario: Cambio de pestaña
- **WHEN** el usuario cambia de una pestaña a otra
- **THEN** el panel nuevo entra con su transición

#### Scenario: Acción interna sin cambiar de pestaña
- **WHEN** el usuario realiza una acción que refresca la pestaña actual
- **THEN** el panel no vuelve a animar su entrada

### Requirement: Piso de accesibilidad
Todo elemento interactivo SHALL exponer un indicador de foco visible al navegar por
teclado; los anclajes dentro del contenido SHALL quedar visibles y no tapados por el
encabezado fijo; y los datos numéricos SHALL usar cifras tabulares para alinear
columnas.

#### Scenario: Navegación por teclado
- **WHEN** el usuario recorre la interfaz con el teclado
- **THEN** el elemento enfocado muestra un anillo de foco visible

#### Scenario: Salto a un anclaje
- **WHEN** el usuario sigue un enlace a una sección dentro de la página
- **THEN** la sección queda visible, no oculta bajo el encabezado fijo
