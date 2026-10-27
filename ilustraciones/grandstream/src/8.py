import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/grandstream/src")
from _gs import *


def caller(x, y, n, kd="info"):
    bg, fg = KC[kd]
    return (f'<circle cx="{x}" cy="{y}" r="22" fill="{bg}" stroke="{fg if kd != "info" else BLUE}" stroke-width="2"/>'
            + text(x, y + 6, str(n), 17, 700, fg if kd != "info" else BLUE, FM, anchor="middle"))


# ---------------------------------------------------------------- 8.svg: grupo contra cola
c = Canvas(K(), "Grupo si suena en todos; cola si hay que esperar")
c.add(panel(48, 128, 540, 420, "Ring Group 6000", "info", sub="sin espera", title_size=21))
c.add(caller(110, 290, 1))
c.add(arrow((136, 290), (250, 220)))
c.add(arrow((136, 290), (250, 360)))
c.add(Generic(258, 180, "Interna 1001", "suena", icon="phone", w=290))
c.add(Generic(258, 320, "Interna 1002", "suena", icon="phone", w=290))
lst, _ = bullet_list(72, 450, ["Todos a la vez, o en orden con 60 s por miembro.", "Nadie atiende: va al destino del grupo."], 500, size=16, gap=6)
c.add(lst)
c.add(panel(612, 128, 540, 420, "Call Queue 6500", "ok", sub="retiene y reparte", title_size=21))
for i in range(4):
    c.add(caller(660 + i * 52, 290, i + 1))
c.add(text(738, 340, "esperan con música", 15, 500, INK3, FM, anchor="middle"))
c.add(arrow((842, 290), (900, 290), kind="ok"))
for j, a in enumerate(["1001", "1002", "1003"]):
    c.add(Generic(908, 160 + j * 92, "Agente " + a, "", icon="user", w=220))
lst, _ = bullet_list(636, 450, ["Estrategia: Ring All de fábrica, Least Recent, Fewest Calls y otras.", "Largo máximo y destino de desborde."], 500, size=16, gap=6)
c.add(lst)
c.add(text(48, 600, "\"Que suene en todos lados\" es un grupo. Cuando hay más llamadas que personas, es una cola.", 17, 500, INK2, FB))
save(c, "8.svg")

# ---------------------------------------------------------------- 8-paso5: el reparto en la cola
c = Canvas(K(5), "Llamá a la cola con un agente ocupado y mirá el reparto")
c.add(text(48, 150, "EN LA COLA (MAX QUEUE LENGTH 5)", 14, 600, INK3, FM, ls=1.5))
for i in range(5):
    c.add(caller(100 + i * 56, 200, i + 1))
c.add(caller(330, 290, 6, "alert"))
c.add(arrow((330, 314), (330, 418), kind="alert"))
c.add(Generic(180, 424, "Failover Destination", "Ring Group 6000", icon="phone", w=300, hl=ALERT))
c.add(text(366, 286, "la sexta ya no entra:", 15, 600, ALERT, FB))
c.add(text(366, 308, "va al desborde", 15, 600, ALERT, FB))
c.add(arrow((350, 200), (562, 372), kind="ok"))
ag = [("Agente 1001", "en otra llamada", "warn"), ("Agente 1002", "atendió hace 2 min", "info"), ("Agente 1003", "hace más que no atiende", "ok")]
for j, (a, s, kd) in enumerate(ag):
    y = 140 + j * 96
    c.add(Generic(570, y, a, s, icon="user", w=330, hl={"warn": WARN, "info": None, "ok": OK}[kd]))
c.add(Chip(920, 384, "Least Recent: le toca", "ok", mono=False))
c.add(Step(570, 140, 5))
c.add(Table(640, 440, ["Tiempo", "Valor"], [["Agent Ring Time", "30 s sonando"], ["Retry Time", "5 s y pasa al otro"], ["Agent Rest Time", "10 s después de cortar"]], [230, 282], row_h=38))
c.add(Note(48, 530, 560, "Max Queue Length viene en 0, que es sin límite: sin tope, la cola nunca desborda por largo y la espera crece sin fin.", kind="warn", size=16))
save(c, "8-paso5.svg")

# ---------------------------------------------------------------- 8-paso3: PIN del buzón
c = Canvas(K(3), "Desde la 1001 marcá *97 y cambiá el PIN")
c.add(DeskPhone(48, 150, "Interna 1001", "marca *97"))
c.add(arrow((230, 210), (300, 210)))
c.add(Generic(310, 168, "Buzón de la 1001", "pide PIN nuevo", icon="bell", w=300, dark=True))
opts = [("1234", "secuencia: la central lo rechaza", False), ("1111", "repetido: la central lo rechaza", False), ("PIN propio", "4 dígitos o más, sin patrón", True)]
for i, (p, d, ok) in enumerate(opts):
    y = 330 + i * 84
    c.add(Mark(330, y, ok=ok))
    c.add(text(364, y + 7, p, 20, 700, OK if ok else ALERT, FM))
    c.add(text(364, y + 32, d, 16, 500, INK2, FB))
c.add(Step(48, 150, 3))
c.add(Note(700, 150, 452, "Un buzón entra por teléfono. Con un PIN trivial cualquiera escucha los mensajes, y si alguien activa el acceso remoto por DID, también desde afuera.", title="Por qué no 1234", kind="alert", size=16))
c.add(Note(700, 376, 452, "Send Voicemail to Email necesita el SMTP de la central configurado (paso 4). Keep Voicemail after Emailing viene activo: el mensaje queda también en la central.", title="Buzón a correo", kind="info", size=16))
save(c, "8-paso3.svg")
