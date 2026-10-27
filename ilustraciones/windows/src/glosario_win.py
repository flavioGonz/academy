"""Genera ilustraciones/windows/glosario-propuesta.json y lo prueba sobre una copia combinada del glosario.

  python3 glosario_win.py            # escribe la propuesta y valida la copia en /tmp/claude-0/glosario-windows.json

terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes.
modificar: campos a reemplazar en entradas existentes (vacío). No toca site2/data/glosario.json.
"""
import json, subprocess, sys

H, S, R, SV = "Herramientas", "Seguridad", "Redes", "Servidores y almacenamiento"


def t(id_, term, aliases, cat, short, long, case=True, year=None):
    e = {"id": id_, "term": term, "aliases": aliases, "cat": cat, "short": short, "long": long, "case": case}
    if year:
        e["year"] = year
    return e


T = [
    t("rdp", "RDP", ["Remote Desktop Protocol", "escritorio remoto de Windows"], R,
      "Remote Desktop Protocol: el protocolo del escritorio remoto de Windows, en el puerto TCP 3389.",
      "Nació con Windows NT 4.0 Terminal Server Edition, en 1998. Da control total del equipo: por eso el 3389 nunca se abre a internet. Se entra por VPN o gateway de escritorio remoto, con NLA activa y la regla del firewall limitada a la subred de gestión."),
    t("nla", "NLA", ["Network Level Authentication", "autenticación a nivel de red"], S,
      "Network Level Authentication: el escritorio remoto pide las credenciales antes de crear la sesión.",
      "Llegó con Windows Vista y Server 2008 y viene activada en todas las versiones soportadas. Usa CredSSP sobre TLS. El error \"requiere NLA\" casi siempre es DNS, controlador de dominio, relación de confianza u hora, y conectar por IP en vez de nombre puede impedir Kerberos."),
    t("credssp", "CredSSP", ["Credential Security Support Provider"], S,
      "Credential Security Support Provider: el mecanismo con el que NLA manda las credenciales antes de abrir la sesión de escritorio remoto.",
      "Viaja dentro del canal TLS del escritorio remoto. Según el caso, autentica con Kerberos o con NTLM."),
    t("laps", "Windows LAPS", ["LAPS", "Local Administrator Password Solution"], S,
      "Local Administrator Password Solution: una contraseña de administrador local única, aleatoria y rotada para cada equipo.",
      "El equipo la genera y la guarda en Active Directory o Entra ID, donde solo la leen las cuentas autorizadas. Evita el movimiento lateral con una clave repetida. Viene integrado en Windows 11 y Server 2019 a 2025 con las actualizaciones de abril de 2023; el LAPS heredado de 2015 quedó en desuso."),
    t("iops", "IOPS", ["operaciones de entrada y salida por segundo"], SV,
      "Operaciones de entrada y salida por segundo que hace un disco.",
      "En Windows es el contador Disk Transfers/sec. Se mira junto con la latencia (Avg. Disk sec/Transfer) y la cola (Avg. Disk Queue Length): cola es aproximadamente IOPS por latencia."),
    t("dsrm", "DSRM", ["Directory Services Restore Mode", "modo de restauración de servicios de directorio"], S,
      "Directory Services Restore Mode: el modo de arranque de emergencia de un controlador de dominio, con su propia contraseña.",
      "La contraseña se define al crear el controlador de dominio y existe desde Active Directory en Windows 2000. Nunca se escribe en texto plano en un script ni en un ticket."),
    t("bios", "BIOS", ["Basic Input/Output System"], SV,
      "Basic Input/Output System: el firmware que arranca la placa madre antes que el sistema operativo.",
      "En los equipos actuales su lugar lo ocupa UEFI, aunque en obra se le sigue diciendo BIOS. Ahí está la opción de vuelta tras corte, Restore on AC Power Loss o After Power Failure: en un servidor con UPS conviene Power On."),
    t("acpi", "ACPI", ["Advanced Configuration and Power Interface"], SV,
      "Advanced Configuration and Power Interface: la norma con la que el sistema operativo maneja la energía del equipo.",
      "La presentaron Intel, Microsoft y Toshiba en 1996. Define los estados S3 (suspensión), S4 (hibernación) y S5 (apagado) que Windows configura con powercfg.", year=1996),
    t("tpm", "TPM", ["Trusted Platform Module"], S,
      "Trusted Platform Module: un chip de seguridad de la placa madre que guarda claves.",
      "BitLocker le confía la llave del disco: el TPM mide el arranque y solo la entrega si el BIOS, el firmware y el cargador son los mismos. Si algo cambió, Windows pide la clave de recuperación."),
    t("bitlocker", "BitLocker", ["manage-bde"], S,
      "El cifrado de disco de Windows: sin la llave, los datos no se leen aunque se roben el disco.",
      "Llegó con Windows Vista en 2007. Ante un cambio de BIOS, firmware o hardware pide la clave de recuperación de 48 dígitos, que se guarda fuera del equipo: ni el soporte de Microsoft la recupera. Antes de tocar el BIOS se suspende con Suspend-BitLocker -RebootCount 1."),
    t("active-directory", "Active Directory", ["AD", "AD DS", "Active Directory Domain Services"], S,
      "El directorio de Microsoft que centraliza usuarios, equipos y permisos de un dominio Windows.",
      "Llegó con Windows 2000. Además de cuentas, guarda cosas que se consultan en obra: la autorización de un DHCP de Windows, claves de BitLocker y contraseñas de Windows LAPS."),
    t("controlador-dominio", "controlador de dominio", ["controladores de dominio", "domain controller"], S,
      "El servidor que corre Active Directory y valida las credenciales del dominio.",
      "Si no responde, falla el inicio de sesión con cuentas del dominio y NLA rechaza el escritorio remoto: por eso cada equipo tiene un administrador local recuperable. Tiene su propia contraseña de emergencia, la DSRM.", case=False),
    t("ubr", "UBR", ["Update Build Revision"], H,
      "Update Build Revision: el número que sube con cada parche acumulado de Windows.",
      "Se lee en el registro, en HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion, junto con EditionID, DisplayVersion y CurrentBuild. Build y UBR juntos, como 26100 y el UBR, dicen exactamente qué parche tiene el equipo."),
    t("uac", "UAC", ["User Account Control", "Control de cuentas de usuario"], S,
      "User Account Control: el aviso de Windows que pide confirmar antes de que un programa use permisos de administrador.",
      "Llegó con Windows Vista. Aun con una cuenta de administrador, los programas corren con permisos comunes hasta que se aprueba la elevación, como al abrir PowerShell como administrador."),
    t("kerberos", "Kerberos", [], S,
      "Protocolo de autenticación por tickets que usa Active Directory.",
      "Nació en el MIT y es el método por defecto de los dominios Windows desde Windows 2000. Necesita encontrar el controlador de dominio por DNS y relojes con pocos minutos de diferencia, y trabaja con nombres: conectando por IP, Windows suele caer a NTLM."),
    t("ntlm", "NTLM", ["NT LAN Manager"], S,
      "NT LAN Manager: el método de autenticación de Windows anterior a Kerberos, que sigue como respaldo.",
      "Aparece, por ejemplo, cuando se conecta a un equipo por IP en vez de por nombre. En dominios con reglas estrictas puede no alcanzar, y el escritorio remoto con NLA falla."),
    t("firma-smb", "firma SMB", ["SMB signing", "RequireSecuritySignature"], S,
      "Un sello en cada mensaje SMB que prueba quién lo mandó y que nadie lo cambió en el camino.",
      "Desde Windows 11 24H2 y en Windows Server 2025 es obligatoria en todas las conexiones salientes. Un NAS o grabador que no firma deja de abrir, y parece una falla de red. Se ve con Get-SmbClientConfiguration.", case=False),
    t("acceso-invitado", "acceso invitado", ["invitado SMB", "guest access", "EnableInsecureGuestLogons"], S,
      "Entrar a una carpeta compartida sin usuario ni contraseña.",
      "Windows 11 Pro 24H2 ya no lo hace. Como no hay credencial, tampoco se puede firmar la sesión. La carpeta del NAS o grabador se abre con un usuario y una contraseña propios de ese equipo.", case=False),
    t("inicio-rapido", "inicio rápido", ["Fast Startup"], H,
      "Fast Startup: al apagar, Windows guarda el núcleo en disco para arrancar más rápido.",
      "Llegó con Windows 8. En un equipo 24/7 no aporta: puede hacer fallar Wake on LAN y que actualizaciones no terminen de aplicarse. powercfg /hibernate off lo apaga junto con la hibernación.", case=False),
    t("monitor-confiabilidad", "Monitor de confiabilidad", ["perfmon /rel", "Reliability Monitor"], H,
      "Herramienta de Windows que resume la salud del equipo en un índice de 1 a 10 por día.",
      "Se abre con perfmon /rel. Pone en la misma columna las fallas de aplicaciones y de Windows y las instalaciones y actualizaciones de cada día: la caída del índice y el cambio que la causó aparecen juntos. El historial se exporta a XML."),
    t("visor-eventos", "Visor de eventos", ["Event Viewer", "eventvwr"], H,
      "La consola de Windows que muestra los registros de eventos, como System y Application.",
      "Cada evento tiene origen, Id, nivel (1 crítico, 2 error, 3 advertencia, 4 información) y fecha. Desde PowerShell se consulta con Get-WinEvent. Los registros tienen tamaño máximo: cuando se llenan, se pisan los más viejos."),
    t("get-winevent", "Get-WinEvent", ["FilterHashtable"], H,
      "Comando de PowerShell que lee los registros de eventos de Windows.",
      "Con -FilterHashtable (LogName, Id, Level, StartTime) el filtro lo aplica el servicio de registro y es mucho más rápido que Where-Object. El 1074 dice quién pidió un reinicio y el 6008 marca un apagado inesperado. Reemplaza a Get-EventLog, que no existe en PowerShell 7."),
    t("perfil-red", "perfil de red", ["perfiles de red", "perfil del firewall", "NetworkCategory"], S,
      "La categoría de cada placa para el Firewall de Windows: Dominio, Privado o Público.",
      "Una regla de firewall solo actúa en los perfiles que tiene asignados. Se ve con Get-NetConnectionProfile y una red propia se pasa a Privada con Set-NetConnectionProfile. Dominio lo pone Windows cuando la placa llega a un controlador de dominio.", case=False),
    t("horas-activas", "horas activas", ["active hours"], H,
      "El horario en que Windows Update no reinicia el equipo.",
      "De fábrica van de 8 a 17 y el rango máximo es de 18 horas. Fuera de ese horario, si no hay sesiones locales ni de escritorio remoto activas, Windows reinicia solo. En servidores, Microsoft sugiere avisar antes de instalar y de reiniciar.", case=False),
    t("movimiento-lateral", "movimiento lateral", ["lateral movement"], S,
      "Saltar de un equipo a otro de la red con una credencial robada.",
      "Pasa cuando todos los equipos comparten la misma contraseña de administrador local: quien la saca de uno entra a todos. Windows LAPS lo corta con una contraseña distinta por equipo.", case=False),
    t("pathping", "pathping", [], H,
      "Comando de Windows que traza la ruta a un destino y mide pérdida y demora en cada salto.",
      "Combina ping y tracert. Por defecto hace 100 consultas por salto y resuelve nombres; -n, -q 10 y -h 5 lo aceleran. La pérdida que aparece en un salto y sigue hasta el destino marca el tramo con problemas."),
    t("nslookup", "nslookup", [], H,
      "Comando que consulta directamente a un servidor DNS.",
      "No usa el resolvedor de Windows: ignora el archivo hosts y la caché, y a un nombre sin punto final le agrega los sufijos de búsqueda antes de probarlo tal cual. Sirve para comparar con Resolve-DnsName y aislar fallas del resolvedor."),
    t("resolve-dnsname", "Resolve-DnsName", [], H,
      "Comando de PowerShell que resuelve un nombre como lo haría una aplicación de Windows.",
      "Usa el resolvedor del sistema, con archivo hosts, caché y DNS. Con -DnsOnly y -Server consulta un servidor concreto. Llegó con Windows 8 y Server 2012."),
    t("archivo-hosts", "archivo hosts", ["C:\\Windows\\System32\\drivers\\etc\\hosts"], R,
      "Archivo de texto de Windows con pares IP y nombre que le ganan al DNS.",
      "Es heredero de la lista de nombres de ARPANET, anterior al DNS. Resolve-DnsName y las aplicaciones lo leen; nslookup no. Se edita como administrador y conviene anotar en el informe cualquier línea que se deje.", case=False),
    t("wbadmin", "wbadmin", ["Windows Server Backup", "Windows-Server-Backup"], H,
      "El comando de Copias de seguridad de Windows Server.",
      "Reemplazó a NTBackup en Windows Server 2008. wbadmin start backup -backupTarget:E: -allCritical -quiet guarda lo necesario para restaurar el sistema; get versions lista las copias y start recovery restaura. -recreateDisks borra datos."),
    t("powercfg", "powercfg", [], H,
      "Comando de Windows que configura la energía: suspensión, hibernación, disco y monitor.",
      "powercfg /change con un tiempo en 0 quiere decir nunca. /hibernate off apaga la hibernación y el inicio rápido; /requests y /lastwake muestran qué mantiene despierto o despertó al equipo."),
    t("sc-exe", "sc.exe", [], H,
      "Comando de Windows que configura servicios: tipo de inicio y recuperación ante fallas.",
      "sc.exe config nombre start= delayed-auto y sc.exe failure nombre reset= 86400 actions= restart/180000, con el espacio después del igual obligatorio. En PowerShell hay que escribir sc.exe: sc a secas es Set-Content."),
    t("inicio-retrasado", "Automático retrasado", ["delayed-auto", "inicio retrasado"], H,
      "Tipo de inicio de un servicio de Windows que arranca un rato después de los automáticos.",
      "Llegó con Windows Vista y Server 2008. Sirve para servicios que dependen de la red o de una base de datos, como un VMS: se configura con sc.exe config nombre start= delayed-auto.", case=False),
    t("recuperacion-servicio", "recuperación ante fallas", ["recuperación del servicio"], H,
      "Lo que Windows hace solo cuando un servicio termina mal: reiniciarlo, correr un programa o reiniciar el equipo.",
      "Se define por número de falla con una espera en milisegundos y un tiempo de reset del contador en segundos, con sc.exe failure. failureflag 1 hace que también actúe si el servicio se detiene con error.", case=False),
    t("tarea-programada", "tarea programada", ["tareas programadas", "Programador de tareas", "AtStartup"], H,
      "Algo que Windows corre solo según un disparador, como al iniciar el sistema.",
      "Con disparador AtStartup, cuenta SYSTEM y -RunLevel Highest corre al encender sin que nadie inicie sesión. Sin carpeta de inicio, el script deja sus archivos en C:\\Windows\\System32.", case=False),
    t("restore-ac-power-loss", "Restore on AC Power Loss", ["After Power Failure"], SV,
      "Opción del BIOS que decide si el equipo se enciende solo cuando vuelve la energía.",
      "Power On enciende siempre; Last State, solo si estaba prendido; Power Off lo deja apagado. Con una UPS que apaga el equipo en orden, Last State no vuelve: conviene Power On, sabiendo que también enciende lo que se apagó a propósito."),
    t("ley-little", "ley de Little", ["Little's law"], SV,
      "En una fila estable, el largo promedio es el ritmo de llegada por el tiempo que pasa cada uno en el sistema.",
      "John Little la demostró en 1961. Para un disco: cola aproximadamente igual a IOPS por latencia. Por eso latencia y cola suben juntas cuando el disco no da abasto.", year=1961, case=False),
    t("microsoft-defender", "Microsoft Defender", ["Defender", "Add-MpPreference"], S,
      "El antivirus integrado en Windows.",
      "Las exclusiones se ven con Get-MpPreference, se agregan con Add-MpPreference y se quitan con Remove-MpPreference. En un servidor de VMS se excluye solo lo que pide el fabricante, como la base de grabación, nunca un disco entero."),
    t("windows-update", "Windows Update", ["Patch Tuesday"], H,
      "El servicio que descarga e instala las actualizaciones de Windows.",
      "Existe desde 1998, y desde octubre de 2003 los parches salen el segundo martes de cada mes, el Patch Tuesday. Muchas actualizaciones terminan al reiniciar; las horas activas y, en servidores, el aviso antes de instalar y reiniciar controlan ese momento."),
]

T += [
    t("llmnr", "LLMNR", ["Link-Local Multicast Name Resolution"], R,
      "Link-Local Multicast Name Resolution: resolución de nombres por multicast dentro de la red local, sin servidor DNS.",
      "Windows la prueba cuando el DNS no encuentra un nombre. Resolve-DnsName la tiene en cuenta; nslookup no, porque solo pregunta al servidor DNS."),
    t("mdns", "mDNS", ["multicast DNS"], R,
      "Multicast DNS: los equipos de la red local responden por su nombre sin un servidor DNS.",
      "Es el mecanismo de los nombres terminados en .local. En Windows forma parte del resolvedor del sistema junto con el archivo hosts, la caché y LLMNR."),
    t("dora", "DORA", ["Discover, Offer, Request, Ack"], R,
      "Discover, Offer, Request y Ack: los cuatro mensajes con los que un equipo obtiene IP por DHCP.",
      "El Discover va por broadcast porque el equipo todavía no tiene IP. Con una reserva, el servidor ofrece siempre la misma IP a esa MAC. Si hay dos DHCP en la red, los dos contestan y el equipo se queda con la primera oferta."),
    t("winrm", "WinRM", ["Windows Remote Management", "WINRM"], H,
      "Windows Remote Management: el servicio con el que se administra Windows a distancia por PowerShell.",
      "Test-NetConnection lo acepta como nombre en -CommonTCPPort para probar si el puerto responde."),
]

ALIAS = {"test-netconnection": ["TcpTestSucceeded"]}

GLOS = "/home/claude/ies-training/site2/data/glosario.json"
OUT = "/home/claude/ies-training/ilustraciones/windows/glosario-propuesta.json"
COMB = "/tmp/claude-0/glosario-windows.json"

g = json.load(open(GLOS, encoding="utf-8"))
by = {e["id"]: e for e in g["terms"]}
P = {
    "nota": "Propuesta para el curso Windows. terms: entradas nuevas completas. alias_agregar: alias nuevos para entradas existentes. modificar: vacío. Probada sobre una copia combinada con glosario_check.py.",
    "terms": T,
    "alias_agregar": ALIAS,
    "modificar": {},
}
json.dump(P, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
dup = [e["id"] for e in T if e["id"] in by]
if dup:
    sys.exit(f"ids que ya existen en el glosario: {dup}")
n0 = len(g["terms"])
g["terms"] += T
for k, al in ALIAS.items():
    by[k]["aliases"] += [a for a in al if a not in by[k]["aliases"]]
json.dump(g, open(COMB, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = json.dumps(P, ensure_ascii=False)
print("ok", OUT, len(T), "entradas nuevas sobre", n0, "· guiones largos:", "—" in s or "–" in s)
r = subprocess.run([sys.executable, "/home/claude/ies-training/tools/glosario_check.py", "windows", "--glosario", COMB], capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr[-1500:], "exit", r.returncode)
