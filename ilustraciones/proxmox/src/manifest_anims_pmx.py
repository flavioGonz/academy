#!/usr/bin/env python3
"""Arma ilustraciones/proxmox/manifest-anims-proxmox.json: animaciones "Cómo se ve en la red" (anims) y de
Laboratorio (steps) del curso Proxmox VE. El alt sale del <desc> de cada SVG (lo escribe cada script anim_*_r_*.py /
anim_*_l*_*.py); los after son fragmentos únicos de la línea del paso en lab.md del curso vigente."""
import html
import json
import re
from pathlib import Path

SITE = Path("/home/claude/ies-training/site2/ilustraciones/proxmox")
OUT = Path("/home/claude/ies-training/ilustraciones/proxmox/manifest-anims-proxmox.json")
CURSO = "/mnt/user-data/uploads/ies-training/sync/proxmox-srv1029.json"


def alt(f):
    s = (SITE / f).read_text(encoding="utf-8")
    return html.unescape(re.search(r'<desc id="d">(.*?)</desc>', s, re.S).group(1)).strip()


R = {  # id: caption del Resumen
    "1": "Cada línea de apt update es un servidor que contesta: Debian firma, enterprise sin clave da 401, no-subscription responde.",
    "2": "Dos VLAN por un solo cable: el switch pone el tag, el trunk lo lleva y vmbr0 lo saca al entregar a cada VM.",
    "3": "ZFS compara cada bloque con su checksum y, con dos discos a la vista, corrige solo; detrás de una RAID no puede.",
    "4": "Ping, IPs, apagado y freeze: todo pasa por el canal del agente entre el host y la VM.",
    "5": "Clon, CD de cloud-init y primer arranque: usuario, clave e IP sin pasar por un instalador.",
    "6": "pct start: namespaces y cgroup en el kernel del host, un par veth en vmbr0 y una IP por DHCP.",
    "7": "El snapshot vivía en el mismo pool y se pierde con el disco; el archivo de vzdump en el NFS rearma la VM.",
    "8": "El token del host sube backups pero no los puede borrar; la copia de afuera y los backups viejos quedan intactos.",
    "9": "El token de corosync necesita su propia red; con un segundo enlace de menor prioridad, el clúster aguanta un corte.",
    "10": "Fuente quemada en pve1: fence, recovery y started en pve2, sin que nadie entre a hacerlo a mano.",
    "11": "Clave más código TOTP para entrar, y PVEAuditor para mirar sin poder apagar ni borrar.",
    "12": "Quórum, logs, locks: en ese orden aparece el lock que quedó de un backup cortado.",
}

S = {  # id: [(paso, archivo, after, caption)]
    "1": [(4, "1-l1.svg", "migralos y actualizá",
           "Lo que pasa en el archivo: la línea vieja se reparte en los campos del bloque deb822, y Enabled: no apaga sin borrar.")],
    "2": [(1, "2-l1.svg", "tildá **VLAN aware**",
           "Lo que pasa en el host: el cambio espera en interfaces.new y Apply lo aplica sin reiniciar ni cortar tu sesión."),
          (5, "2-l2.svg", "En el switch, el puerto del host va en trunk",
           "Lo que pasa en el cable: con el puerto en access la trama con tag 10 se descarta; en trunk llega al gateway y vuelve.")],
    "3": [(2, "3-l1.svg", "Si es LVM-thin, mirá el pool",
           "Lo que muestra lvs: LSize es lo asignado, Data% lo escrito; sobreasignar anda hasta que el pool se llena."),
          (3, "3-l2.svg", "Si es ZFS, mirá la salud del pool",
           "Lo que pasa en la RAM: el ARC guarda lo leído y crece hasta zfs_arc_max, que se lee y se fija en bytes.")],
    "4": [(3, "4-l1.svg", "Apagá y prendé la VM desde Proxmox",
           "Lo que pasa por dentro: un reboot del invitado no arma el canal del agente; Stop y Start crean un proceso QEMU nuevo.")],
    "5": [(2, "5-l1.svg", "Creá la VM base, importá el disco",
           "Lo que pasa en el almacenamiento: la imagen se importa como disco, se suma la unidad cloud-init y qm template deja el disco base de solo lectura.")],
    "6": [(3, "6-l1.svg", "Creá un contenedor no privilegiado",
           "Lo que pasa en el disco: pct create desempaqueta la plantilla corriendo cada dueño 100000.")],
    "7": [(3, "7-l1.svg", "Antes de arrancar, desconectá la placa",
           "Lo que pasa en la red: la 900 es una copia exacta de la 100; con link_down=1 arranca aislada y no le corta el servicio.")],
    "8": [(2, "8-l1.svg", "Garbage collection semanal y verify diario",
           "Lo que hace verify: relee cada trozo, compara su SHA-256 y marca fallido el backup con un trozo dañado."),
          (4, "8-l2.svg", "En Proxmox VE: **Datacenter",
           "Lo que pasa en la conexión: TLS al 8007, PVE compara la huella, entra con el token y PBS revisa DatastoreBackup.")],
    "9": [(4, "9-l1.svg", "Probá crear una VM: no te deja",
           "Lo que cambia en pvecm status: Total votes 1 con Quorum 2, Quorate: No, y qm create falla."),
          (5, "9-l2.svg", "En una tercera máquina Debian",
           "Lo que pasa en la red: cada nodo habla con el qnetd por TCP 5403 y el clúster espera 3 votos; sin pve2 quedan 2 de 3.")],
    "10": [(3, "10-l1.svg", "Desarmá la HA como harías antes de tocar corosync",
            "Lo que pasa con los watchdogs: disarm-ha freeze los libera, un corte de corosync no reinicia nodos y arm-ha los vuelve a abrir.")],
    "11": [(1, "11-l1.svg", "Usuario de solo lectura",
            "Lo que pasa en el árbol de permisos: PVEAuditor asignado en / se hereda a nodos, VMs y almacenamiento.")],
    "12": [(5, "12-l1.svg", "Si el host viene de la 8, buscá ajustes",
            "Lo que pasa al arrancar en la 9: systemd-sysctl ya no lee sysctl.conf y el ajuste vuelve desde /etc/sysctl.d/.")],
}


def main():
    curso = {str(l["id"]): l for l in json.load(open(CURSO, encoding="utf-8"))["lessons"]}
    man = {}
    for lid in [str(i) for i in range(1, 13)]:
        e = {"anims": [{"file": f"{lid}-r1.svg", "alt": alt(f"{lid}-r1.svg"), "caption": R[lid]}]}
        lab = curso[lid]["lab"]["md"].split("\n")
        steps = []
        for paso, f, after, cap in S.get(lid, []):
            fence, hits = False, []
            for ln in lab:
                if ln.strip().startswith("```"):
                    fence = not fence
                    continue
                if not fence and after in ln:
                    hits.append(ln)
            assert len(hits) == 1 and re.match(rf"\s*{paso}\. ", hits[0]), (lid, after, hits)
            steps.append({"step": paso, "file": f, "after": after, "alt": alt(f), "caption": cap})
        if steps:
            e["steps"] = steps
        for x in e["anims"] + e.get("steps", []):
            assert (SITE / x["file"]).exists() and len(x["alt"]) <= 1000, x["file"]
        man[lid] = e
    OUT.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", OUT, sum(len(v["anims"]) for v in man.values()), "anims,", sum(len(v.get("steps", [])) for v in man.values()), "steps")


if __name__ == "__main__":
    main()
