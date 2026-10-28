# Lección 45. Configuración de botones

**Escuchá:** botones-llamadas.mp3 (2 min)

**La idea, en tres líneas**
- Cada botón marca un destino: una IP por `Intercom > Basic > Direct IP` (Enabled y Port 5060, igual en las dos puntas; en el E12 está en `Intercom > Call Feature > Direct IP`) o un número SIP por la cuenta de `Account > Basic` (con las dos registradas, Auto usa la 1). Dónde se carga el destino depende de la familia: tecla de Recepción en `Intercom > Basic > Key Setting` (E16 y E18: Reception Enabled, Name, Number), Speed Dial en `Setting > Key/Display` (R29 y X915) y el pulsador en `Intercom > Basic > Manager Dial` (E12, serie R20, E13).
- Con varios destinos hay dos modos. Sequence Call llama de a uno: si no atienden en el Call Timeout pasa al siguiente, y si rechazan, When Refused decide (`Do Not Call Next` corta, `Call Next` sigue). Group Call hace sonar todos a la vez: si uno rechaza, `End This Call Only` corta solo a ese y `End All Calls` corta a todos. En los táctiles, la secuencia es un grupo de `Directory > User > Group` con Priority of Call (Primary, Secondary, Tertiary).
- `Intercom > Dial Plan` cambia un número corto por hasta 5 IP o SIP que suenan juntas (1.000 reglas en E16 y E18, 1.500 en R29, 500 en R20K). `Intercom > Call Feature` tiene Auto Answer de las llamadas IP, Max Call Time, Max Dial Time (Dial In Time y Dial Out Time) y Hang Up After Open Door.

**Impacto:** el timbre suena donde tiene que sonar y, si nadie atiende o alguien rechaza, el portero hace lo que el cliente espera: pasar al siguiente, seguir sonando en los demás o cortar.

**Quién lo dice:** 12 de 12 páginas de la Knowledge Base de Akuvox coinciden en el mecanismo (guías de E16, E18, E12, R20A/B, R20K, R29 y X915, y las notas de Sequence Call y Group Call de septiembre de 2026); cambian el menú por familia y la redacción de End This Call Only. Un hilo de FreePBX muestra el mismo "suenan todos y atiende uno" armado en la central.

**Laboratorio** · Foco · 25 min
Un E16 (o un E18) y dos monitores en la mesa, todo por IP directa en la red de laboratorio:
```text
Portero E16     192.168.88.20
Monitor living  192.168.88.64
Monitor cocina  192.168.88.65
```
1. En los tres equipos: `Intercom > Basic > Direct IP`, Enabled y Port 5060. Submit.
2. En el portero, `Intercom > Basic > Key Setting`: Reception Enabled, Name `RECEPCION` y Number con los dos monitores. Submit, apretá Recepción en la pantalla y anotá si suenan juntos o de a uno.
```text
Number: 192.168.88.65,192.168.88.64
```
3. Armá un grupo: en `Directory > User > Group`, +Add y `Conserjeria`; en `Directory > User`, dos usuarios con Phone `192.168.88.64` y `192.168.88.65`, los dos en el grupo `Conserjeria`; en `Directory > Directory Setting`, Contacts Display Mode en `Groups Only`. Tocá el grupo en el directorio del portero: suenan los dos.
4. Rechazá en el monitor de la cocina con `Intercom > Basic > Group Call` en `End This Call Only`: el living sigue sonando. Pasalo a `End All Calls` y repetí: se corta todo.
5. Secuencia: en los dos usuarios, Priority of Call `Primary` para el .64 y `Secondary` para el .65; en `Intercom > Basic > Sequence Call`, Call Timeout 20 y When Refused `Call Next`. Llamá al grupo sin atender: a los 20 segundos pasa a la cocina. Rechazá en el living: con `Call Next` suena la cocina; con `Do Not Call Next`, se corta ahí.
6. Número corto: `Intercom > Dial Plan`, +Add, Account `Auto`, Prefix `100`, Replace 1 `192.168.88.64` y Replace 2 `192.168.88.65`. Marcá 100 en el teclado del portero: suenan los dos.
7. Tiempos en `Intercom > Call Feature`: Max Dial Time (Dial Out Time) para que no quede sonando en un monitor apagado, y Hang Up After Open Door con el método que abre la puerta (en DTMF que abre, el código DTMF).
8. Si el portero es de botón o de teclado, el menú es otro:
```text
E12, R20A, R20B, E13 : Intercom > Basic > Manager Dial  (Call Type: Sequence Call o Group Call, un número por casilla)
R20K (teclado)       : Intercom > Basic > Speed Dial    (un número SIP o IP por casilla)
R29 (táctil)         : Setting > Key/Display            (Speed Dial Theme, en Villa u Office)
X915 (táctil)        : Setting > Key/Display > Speed Dial Setting
```
⚠️ Con SmartPlus, secuencia y grupo los define la app: la casilla Group Call Number(Local) queda vacía y en el E12 la secuencia local desaparece. Con central, Max Call Time y Max Dial Time no superan los de la central.

**Regla para quedarse**
Cada botón se prueba con un monitor que no atiende y otro que rechaza antes de irme de la obra.

**Saltear** · no cuesta nada. La lección siguiente es simplemente la siguiente.

**Para profundizar (opcional)**
- Llamadas del E16 (Recepción, Sequence Call, Group Call, Dial Plan y tiempos): https://knowledge.akuvox.com/docs/call-settings-10
- Secuencia local y de nube por familia de modelos: https://knowledge.akuvox.com/docs/configure-sequence-call
- Grupo local y de nube por familia de modelos: https://knowledge.akuvox.com/docs/configure-group-call
- Contactos, grupos y prioridad en el E16: https://knowledge.akuvox.com/docs/contact-list-configuration-4
- Manager Dial y tiempos en el E12: https://knowledge.akuvox.com/docs/call-settings-7
