#!/usr/bin/env python3
"""pvex.py - helper de IES Training para operar el cluster Proxmox desde esta PC.

  python pvex.py run  pve01 script.sh        ejecuta el script bash en el nodo (bash -s)
  python pvex.py cmd  pve01 "pct list"       un comando suelto
  python pvex.py put  pve01 local remoto     sube un archivo por SFTP al nodo

Credencial root: env IES_PVE_PASSWORD o el default documentado en la skill ies-proxmox.
"""
import os, sys, paramiko

NODES = {"pve01": "172.26.20.91", "pve02": "172.26.20.92", "pve03": "172.26.20.93"}
PW = os.environ.get("IES_PVE_PASSWORD") or sys.exit("Definí IES_PVE_PASSWORD (clave root de los nodos Proxmox)")


def client(node):
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(NODES.get(node, node), username="root", password=PW, timeout=15, look_for_keys=False, allow_agent=False)
    return c


def run(node, script):
    c = client(node)
    try:
        stdin, stdout, stderr = c.exec_command("bash -s", timeout=900)
        stdin.write(script.replace("\r\n", "\n")); stdin.channel.shutdown_write()
        out = stdout.read().decode(errors="replace"); err = stderr.read().decode(errors="replace")
        code = stdout.channel.recv_exit_status()
        sys.stdout.write(out)
        if err: sys.stdout.write("\n[stderr]\n" + err)
        sys.stdout.write(f"\n[exit {code}]\n")
        return code
    finally:
        c.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "run":
        sys.exit(run(a[1], open(a[2], encoding="utf-8").read()))
    if a[0] == "cmd":
        sys.exit(run(a[1], a[2]))
    if a[0] == "put":
        c = client(a[1]); s = c.open_sftp(); s.put(a[2], a[3]); s.close(); c.close(); print("ok", a[3])
    if a[0] == "get":
        # python pvex.py get pve01 /ruta/remota archivo_local
        c = client(a[1]); s = c.open_sftp(); s.get(a[2], a[3]); s.close(); c.close(); print("ok", a[3])
