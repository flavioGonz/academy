#!/usr/bin/env python3
"""Publish /home/claude/ies-training/site to training.ies.com.uy via cPanel UAPI (port 443).

Steps (each idempotent):
  check     whoami, list domains, resource usage
  subdomain create training.ies.com.uy with docroot public_html/training (if missing)
  upload    create folders (API2 Fileman::mkdir) and upload every file, folder by folder
  ssl       start an AutoSSL pass

Never deletes anything. Token from IES_CPANEL_TOKEN (never a file).
Usage: python3 deploy_training.py check|subdomain|upload|ssl|all [--only data,assets]
"""
import json, os, sys, urllib.parse
sys.path.insert(0, "/root/.claude/skills/synced/a9ecc74d-07d4-4270-8b1b-f043434ee60a_7b1c6357-22aa-431a-9cbd-76b0523a77d6/ies-cpanel/scripts")
from cpanel_api import CpanelError, _base, _request, call, upload  # noqa: E402

SITE = "/home/claude/ies-training/site"
SUB, ROOT = "training", "ies.com.uy"
DOCROOT = "public_html/training"
LOTE = 6 * 1024 * 1024


def api2(module, func, **params):
    q = {"cpanel_jsonapi_user": os.environ.get("IES_CPANEL_USER", "ies"), "cpanel_jsonapi_apiversion": "2",
         "cpanel_jsonapi_module": module, "cpanel_jsonapi_func": func, **params}
    res = _request("%s/json-api/cpanel?%s" % (_base(), urllib.parse.urlencode(q)))
    return res.get("cpanelresult", res)


def check():
    d = call("DomainInfo", "list_domains")
    print("main:", d.get("main_domain"), "| sub:", ", ".join(d.get("sub_domains", [])[:60]))
    try:
        for u in call("ResourceUsage", "get_usages"):
            if u.get("id") in ("disk_usage", "filesusage", "bandwidth"):
                print(f"  {u.get('description')}: {u.get('usage')} / {u.get('maximum')}")
    except CpanelError as e:
        print("  usage n/a:", e)
    return d


def subdomain():
    d = call("DomainInfo", "list_domains")
    if f"{SUB}.{ROOT}" in d.get("sub_domains", []):
        print(f"{SUB}.{ROOT} ya existe")
        return
    print(call("SubDomain", "addsubdomain", domain=SUB, rootdomain=ROOT, dir=DOCROOT))
    print(f"creado {SUB}.{ROOT} -> {DOCROOT}")


def existing(path):
    try:
        return {x.get("file") for x in (call("Fileman", "list_files", dir=path, types="dir|file") or [])}
    except CpanelError:
        return None


def mkdir(parent, name):
    r = api2("Fileman", "mkdir", path=parent, name=name)
    return r


def upload_all(only=None):
    dirs = {}
    for root, ds, fs in os.walk(SITE):
        ds[:] = sorted(d for d in ds if not d.startswith("."))
        rel = os.path.relpath(root, SITE)
        rel = "" if rel == "." else rel
        if only and rel and rel.split("/")[0] not in only:
            continue
        if only and not rel and "root" not in only:
            fs = []
        dirs[rel] = [os.path.join(root, f) for f in sorted(fs) if not f.startswith(".")]
    for rel, files in dirs.items():
        remote = DOCROOT + ("/" + rel if rel else "")
        parts = rel.split("/") if rel else []
        for i in range(len(parts)):
            parent = "/".join([DOCROOT] + parts[:i])
            have = existing(parent) or set()
            if parts[i] not in have:
                mkdir(parent, parts[i])
        if not files:
            continue
        lote, peso, n = [], 0, 0
        for f in files:
            t = os.path.getsize(f)
            if lote and peso + t > LOTE:
                upload(remote, lote); n += len(lote); lote, peso = [], 0
            lote.append(f); peso += t
        if lote:
            upload(remote, lote); n += len(lote)
        print(f"  {remote or '/'}: {n} archivos", flush=True)


def ssl():
    try:
        print(call("SSL", "start_autossl_check"))
    except CpanelError as e:
        print("autossl:", e)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    try:
        if cmd in ("check", "all"): check()
        if cmd in ("subdomain", "all"): subdomain()
        if cmd in ("upload", "all"): upload_all(only)
        if cmd in ("ssl", "all"): ssl()
    except CpanelError as e:
        sys.exit(f"ERROR: {e}")
