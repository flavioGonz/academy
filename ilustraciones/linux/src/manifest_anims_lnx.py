"""Genera ilustraciones/linux/manifest-anims-linux.json: animaciones del Resumen (anims), del Laboratorio (steps)
y la figura extra de teoría de la lección 6 (teoria_figs). El alt sale del <desc> de cada SVG."""
import html
import json
import re
from pathlib import Path

SITE = Path("/home/claude/ies-training/site2/ilustraciones/linux")
OUT = Path("/home/claude/ies-training/ilustraciones/linux/manifest-anims-linux.json")


def alt(f):
    s = (SITE / f).read_text(encoding="utf-8")
    return html.unescape(re.search(r'<desc id="d">(.*?)</desc>', s, re.S).group(1)).strip()


def R(f, cap):
    return {"file": f, "alt": alt(f), "caption": cap}


def P(step, f, after, cap):
    return {"step": step, "file": f, "after": after, "alt": alt(f), "caption": cap}


M = {
    "1": {"anims": [R("1-r1.svg", "Un solo árbol desde /: el segundo disco es una carpeta más, y findmnt dice cuál es.")],
          "steps": [P(2, "1-l1.svg", "Encontrá los archivos de configuración del servidor SSH:",
                      "Lo que pasa en este paso: los resultados salen por el canal 1 y los Permission denied por el canal 2, que 2>/dev/null descarta.")]},
    "2": {"anims": [R("2-r1.svg", "Con 777 el resto también borra; con un grupo y 2770, solo entran los técnicos.")],
          "steps": [P(1, "2-l1.svg", "Creá el grupo y dos usuarios de prueba:",
                      "Lo que pasa en este paso: -aG suma el grupo; sin la a, la lista se reemplaza. Y vale desde la próxima sesión.")]},
    "4": {"anims": [R("4-r1.svg", "Copia, snippet, sshd -t, reload y prueba desde una sesión nueva, sin cerrar la que funciona.")],
          "steps": [P(3, "4-l1.svg", "Tu cambio en un archivo propio y validación:",
                      "Lo que pasa en este paso: con &&, lo de la derecha corre solo si sshd -t terminó con código 0.")]},
    "5": {"anims": [R("5-r1.svg", "start levanta ahora; enable deja el enlace para que arranque solo después de un corte.")],
          "steps": [P(2, "5-l1.svg", "Rompé la configuración a propósito y mirá el error",
                      "Lo que pasa en este paso: systemd corre sshd -t antes de arrancar, falla con 255 y la unidad queda en failed."),
                    P(4, "5-l2.svg", "Filtros de journalctl para obra:",
                      "Lo que pasa en este paso: -b -1 elige el arranque anterior y -p err deja las prioridades 0 a 3.")]},
    "10": {"anims": [R("10-r1.svg", "La caché de disco se suelta cuando un programa pide: por eso available es la cifra que importa.")],
           "steps": [P(1, "10-l1.svg", "Memoria y carga:",
                       "Lo que pasa en este paso: la carga se compara con nproc; lo que pasa de ahí es la fila de espera."),
                     P(4, "10-l2.svg", "Si el que consume es un servicio:",
                       "Lo que pasa en este paso: systemd manda SIGTERM, espera, recién al vencer el plazo manda SIGKILL, y lo vuelve a arrancar.")]},
    "3": {"anims": [R("3-r1.svg", "Firma de InRelease, suma de Packages y suma del .deb: cada eslabón confirma el siguiente.")],
          "steps": [P(2, "3-l1.svg", "Instalá (si falta) y activá las actualizaciones automáticas",
                      "Lo que pasa en este paso: unattended-upgrades aplica solo lo que viene de un origen permitido, como -security.")]},
    "6": {"anims": [R("6-r1.svg", "ARP, ping, DNS por UDP 53 y saludo TCP: lo que prueba cada escalón en el cable.")],
          "steps": [P(1, "6-l1.svg", "Subí la escalera y anotá el resultado de cada escalón:",
                      "Lo que pasa en este paso: antes del primer ping, ARP busca la MAC del gateway, y esa MAC sirve también para 1.1.1.1.")],
          "teoria_figs": [{"file": "6-t3.svg", "after": "La resolución de nombres sigue el orden de /etc/nsswitch.conf", "alt": alt("6-t3.svg"),
                           "caption": "ping sigue nsswitch y una línea vieja de /etc/hosts le gana al DNS; dig va directo al DNS."}]},
    "7": {"anims": [R("7-r1.svg", "La llave de host del servidor va a known_hosts; la tuya, a authorized_keys.")],
          "steps": [P(2, "7-l1.svg", "Copiala y entrá con ella:",
                      "Lo que pasa en este paso: la contraseña viaja una última vez y la pública queda al final de authorized_keys."),
                    P(4, "7-l2.svg", "Desde OTRA terminal, probá que la contraseña ya no entra:",
                      "Lo que pasa en este paso: el servidor ofrece solo publickey; sin llave, Permission denied (publickey).")]},
    "8": {"anims": [R("8-r1.svg", "SSH desde gestión entra, la PC de la LAN no recibe nada, la respuesta de apt vuelve y postgres no se ve.")],
          "steps": [P(3, "8-l2.svg", "Opción Debian 13 con nftables (equivalente mínimo):",
                      "Lo que pasa en este paso: nft -c valida, enable deja el servicio para el arranque y lo hecho en vivo se pierde al reiniciar."),
                    P(4, "8-l1.svg", "Verificá desde OTRA máquina, no desde el servidor:",
                      "Lo que pasa en este paso: SYN-ACK es open, RST es closed y sin respuesta es filtered.")]},
    "9": {"anims": [R("9-r1.svg", "rm borra el nombre, pero un archivo abierto sigue ocupando el disco hasta que el proceso lo cierra.")],
          "steps": [P(1, "9-l1.svg", "¿Dónde está lleno?",
                      "Lo que pasa en este paso: df -h cuenta espacio y df -i cuenta archivos; los inodos se pueden acabar antes.")]},
    "11": {"anims": [R("11-r1.svg", "La copia en otro equipo, probada restaurando, es la que queda cuando se rompe el disco.")],
           "steps": [P(4, "11-l1.svg", "Para datos, rsync a otro equipo",
                       "Lo que pasa en este paso: rsync compara tamaño y fecha, y con -n solo lista lo que copiaría.")]},
    "12": {"anims": [R("12-r1.svg", "En una red de Docker los contenedores se hablan por nombre; solo el proxy publica el 443.")],
           "steps": [P(5, "12-l1.svg", "Volumen para datos que sobreviven al contenedor:",
                       "Lo que pasa en este paso: docker rm -f borra el contenedor y su capa; el volumen y sus datos quedan.")]},
}

for k, v in M.items():
    for x in v.get("anims", []) + v.get("steps", []) + v.get("teoria_figs", []):
        assert len(x["alt"]) <= 1000, x["file"]
        assert "—" not in x["alt"] + x["caption"] and "–" not in x["alt"] + x["caption"], x["file"]
OUT.write_text(json.dumps(M, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok", OUT, sum(len(v.get("anims", [])) for v in M.values()), "anims,", sum(len(v.get("steps", [])) for v in M.values()), "steps,",
      sum(len(v.get("teoria_figs", [])) for v in M.values()), "teoria_figs")
