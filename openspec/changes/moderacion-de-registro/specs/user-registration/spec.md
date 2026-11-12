# Spec Delta

## Purpose
Definir el alta de cuentas moderada: una persona se registra, queda pendiente, y un
administrador la habilita o rechaza antes de que pueda acceder al contenido.

## ADDED Requirements

### Requirement: Alta queda pendiente de aprobación
Al registrarse, el sistema SHALL crear la cuenta en estado inactivo, SHALL NOT
iniciar sesión automáticamente, y SHALL responder indicando que la cuenta quedó
pendiente de aprobación.

#### Scenario: Registro de una persona nueva
- **WHEN** una persona completa el formulario de registro con datos válidos
- **THEN** se crea la cuenta como inactiva, no se inicia sesión, y se muestra un
  mensaje de "cuenta pendiente de aprobación"

#### Scenario: Correo ya registrado
- **WHEN** el correo ya existe
- **THEN** el sistema rechaza el alta con un error claro y no crea una cuenta duplicada

### Requirement: Login bloqueado hasta la aprobación
El sistema SHALL impedir el inicio de sesión de una cuenta inactiva y SHALL informar
que está a la espera de aprobación de un administrador.

#### Scenario: Intento de ingreso con cuenta pendiente
- **WHEN** una persona con cuenta inactiva intenta ingresar con credenciales correctas
- **THEN** el acceso se rechaza con un mensaje que explica que falta la habilitación

#### Scenario: Ingreso tras la aprobación
- **WHEN** un administrador habilita la cuenta y la persona vuelve a ingresar
- **THEN** el acceso se concede y ve el contenido para usuarios habilitados

### Requirement: Cola de aprobación para el administrador
El panel de administración SHALL presentar las cuentas pendientes en una vista
diferenciada, con un indicador de cuántas hay, y SHALL permitir aprobarlas o
rechazarlas.

#### Scenario: Hay altas pendientes
- **WHEN** existen cuentas pendientes y el administrador abre el panel
- **THEN** ve un indicador con la cantidad y puede listar solo las pendientes

#### Scenario: Aprobar una cuenta
- **WHEN** el administrador aprueba una cuenta pendiente
- **THEN** la cuenta pasa a habilitada y la persona puede ingresar

#### Scenario: Rechazar una cuenta
- **WHEN** el administrador rechaza una cuenta pendiente
- **THEN** la cuenta no queda habilitada y se distingue de una simple cuenta inactiva

### Requirement: Avisos del ciclo de alta
El sistema SHALL avisar al administrador de que hay una aprobación pendiente cuando
entra un alta nueva, y SHOULD dar a la persona una señal clara cuando su cuenta
queda habilitada.

#### Scenario: Llega un alta nueva
- **WHEN** se registra una persona
- **THEN** el administrador recibe una señal (indicador en el panel o aviso) de que
  hay una aprobación pendiente
