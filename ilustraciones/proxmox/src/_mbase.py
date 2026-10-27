"""Base del manifest Proxmox: L (lección), C (concepto), S (script de shell del host)."""
M = {}


def L(lid, fig, steps, concepts, teoria, tfig, script=None):
    M[lid] = {"fig": fig, "steps": steps, "concepts": concepts, "teoria_md": teoria.strip(), "teoria_figs": tfig}
    if script:
        M[lid]["script_rsc"] = script


def C(name, para_que, como, ejemplo):
    return {"name": name, "para_que": para_que, "como": como, "ejemplo": ejemplo}


def S(titulo, descripcion, variables, codigo, notas):
    return {"titulo": titulo, "descripcion": descripcion, "lenguaje": "bash",
            "variables": [{"nombre": n, "valor": v, "detalle": d} for n, v, d in variables],
            "codigo": codigo.strip(), "notas": notas}
