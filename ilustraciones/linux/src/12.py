import sys; sys.path.insert(0, "/home/claude/ies-training/ilustraciones/linux/src")
from _lnx import *

# ---------------------------------------------------------------- 12.svg: panorama
c = new(None, "Docker en cuatro piezas, y dónde publicar el puerto")
pieces = [("Imagen", "el software empaquetado", "nginx"), ("Contenedor", "la imagen corriendo", "docker run -d"),
          ("Volumen", "datos que sobreviven", "/var/lib/docker/volumes"), ("Red de Docker", "cómo se hablan entre ellos", "sin publicar nada")]
for i, (t, d, ex) in enumerate(pieces):
    x = 48 + i * 282
    c.add(panel(x, 124, 264, 150, t, "info"))
    c.add(text(x + 20, 190, d, 16, 500, INK2, FB))
    c.add(text(x + 20, 236, ex, 15, 600, BLUE, FM))
c.add(text(48, 318, "Publicar un puerto en el host", 19, 600, INK, FD))
c.add(panel(48, 336, 540, 230, None, "alert"))
c.add(code(68, 356, 500, "docker run -d -p 8080:80 nginx", 16, h=42))
c.add(text(68, 434, "0.0.0.0:8080", 22, 700, ALERT, FM))
c.add(lines(68, 470, ["Todas las interfaces. Docker lo abre antes", "de que lleguen las reglas de ufw: responde", "a la red aunque ufw diga deny."], 16, 26))
c.add(panel(612, 336, 540, 230, None, "ok"))
c.add(code(632, 356, 500, "docker run -d -p 127.0.0.1:8081:80 nginx", 16, h=42))
c.add(text(632, 434, "127.0.0.1:8081", 22, 700, OK, FM))
c.add(lines(632, 470, ["Solo el propio host. Lo público va detrás", "de un proxy inverso en 80 y 443, o se filtra", "en la cadena DOCKER-USER."], 16, 26))
c.add(Note(48, 588, 1104, "La prueba se hace desde otra máquina: nmap -Pn -p 8080,8081 contra la IP del servidor.", kind="info"))
save(c, "12.svg")

# ---------------------------------------------------------------- 12-paso3: abierto pese a ufw
c = new(3, "ufw dice deny, pero el 8080 responde desde la otra VM")
svg, h = term(48, 124, 540, ["$ sudo docker run -d -p 8080:80 nginx", "$ sudo ss -tlnp | grep 8080", ("LISTEN 0.0.0.0:8080  docker-proxy", T_ERR),
                             "$ sudo ufw status", ("Status: active", T_OUT), ("22/tcp  ALLOW  10.10.10.0/24", T_OUT), ("(nada del 8080)", T_COM)],
            "SERVIDOR 192.168.88.50 · EJEMPLO", size=15, lh=28)
c.add(svg)
svg2, h2 = term(612, 124, 540, ["$ nmap -Pn -p 8080,8081 192.168.88.50", ("8080/tcp  open", T_ERR), ("8081/tcp  filtered", T_OUT)],
                "OTRA VM DE LA MISMA RED · EJEMPLO", size=15, lh=28)
c.add(svg2)
c.add(Note(612, 124 + h2 + 24, 540, "El 8081 todavía no existe: más adelante, publicado en 127.0.0.1, tampoco va a aparecer abierto.", kind="info"))
c.add(box(48, 124 + h + 30, 1104, 150, "Por qué pasa", ["Docker redirige el puerto publicado en la tabla nat, antes de que el paquete llegue a la cadena input,",
                                                    "donde ufw tiene sus reglas. Para el kernel ya no es tráfico para el host: va por forward hacia el contenedor.",
                                                    "Por eso ufw status no lo menciona, y por eso se verifica desde otra máquina."], kind="alert"))
save(c, "12-paso3.svg")

# ---------------------------------------------------------------- 12-paso4: solo para el host
c = new(4, "Publicado en 127.0.0.1: responde en el servidor, no en la red")
svg, h = term(48, 124, 640, ["$ sudo docker run -d -p 127.0.0.1:8081:80 nginx", "$ sudo ss -tlnp | grep 8081", ("LISTEN 127.0.0.1:8081  docker-proxy", T_OK),
                             "$ curl -sI 127.0.0.1:8081 | head -1", ("HTTP/1.1 200 OK", T_OK)], "SERVIDOR · EJEMPLO", size=15, lh=28)
c.add(svg)
c.add(panel(760, 124, 392, 190, "Servidor", "info", sub="192.168.88.50"))
c.add(rect(780, 220, 352, 64, OK_BG, OK, rx=10))
c.add(text(800, 258, "nginx en 127.0.0.1:8081", 16, 700, OK, FM))
c.add(Laptop(760, 440, "Otra VM", "nmap -Pn -p 8081", w=392))
c.add(Cable((956, 440), (956, 322), "alert", label="8081 no aparece abierto", arrow=True, bend="straight"))
c.add(Note(48, 124 + h + 28, 640, "Para los datos, un volumen: docker volume create datos-prueba y docker volume inspect muestra su Mountpoint.", kind="info"))
c.add(Note(48, 124 + h + 132, 640, "No pongas \"iptables\": false en Docker: rompe la red de los contenedores y deja sus puertos accesibles desde la red local.", kind="warn"))
save(c, "12-paso4.svg")
