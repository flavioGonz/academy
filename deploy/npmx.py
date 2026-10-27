#!/usr/bin/env python3
"""npmx.py - cliente minimo de la API del Nginx Proxy Manager de IES (stdlib).
  python npmx.py GET /nginx/proxy-hosts
  python npmx.py POST /nginx/proxy-hosts body.json
Credenciales: env IES_NPM_* o los defaults documentados en la skill ies-nginx-proxy.
"""
import json, os, sys, urllib.request

URL = os.environ.get("IES_NPM_URL", "http://172.26.20.17:81").rstrip("/")
ID = os.environ.get("IES_NPM_IDENTITY", "")
SEC = os.environ.get("IES_NPM_SECRET") or sys.exit("Definí IES_NPM_SECRET")


def req(method, path, body=None, token=None):
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json"}
    if token: h["Authorization"] = "Bearer " + token
    r = urllib.request.Request(URL + "/api" + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            t = resp.read().decode(); return resp.status, (json.loads(t) if t else None)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


if __name__ == "__main__":
    st, tok = req("POST", "/tokens", {"identity": ID, "secret": SEC})
    token = tok["token"]
    m, path = sys.argv[1], sys.argv[2]
    body = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else None
    st, out = req(m, path, body, token)
    if m == "GET" and path == "/nginx/proxy-hosts" and isinstance(out, list):
        for h in out:
            print(h["id"], ",".join(h["domain_names"]), "->", f'{h["forward_scheme"]}://{h["forward_host"]}:{h["forward_port"]}', "cert", h.get("certificate_id"), "ssl_forced", h.get("ssl_forced"), "enabled", h.get("enabled"))
    else:
        print(st); print(json.dumps(out, indent=1, ensure_ascii=False) if not isinstance(out, str) else out)
