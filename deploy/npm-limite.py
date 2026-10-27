import npmx
# Proxy host 11 (entrenamientos.ies.com.uy): permitir cuerpos de hasta 70 MB para subir videos y GIF.
st, t = npmx.req("POST", "/tokens", {"identity": npmx.ID, "secret": npmx.SEC}); tok = t["token"]
st, h = npmx.req("GET", "/nginx/proxy-hosts/11", None, tok)
adv = h.get("advanced_config", "") or ""
if "client_max_body_size" in adv:
    import re; adv = re.sub(r"client_max_body_size\s+\S+;", "client_max_body_size 70m;", adv)
else:
    adv = (adv + "\n" if adv.strip() else "") + "client_max_body_size 70m;"
st, h = npmx.req("PUT", "/nginx/proxy-hosts/11", {"advanced_config": adv}, tok)
print("host", st, h if isinstance(h, str) else {"id": h.get("id"), "advanced_config": h.get("advanced_config"), "enabled": h.get("enabled")})
