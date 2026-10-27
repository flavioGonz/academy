import json, npmx
st, t = npmx.req("POST", "/tokens", {"identity": npmx.ID, "secret": npmx.SEC}); tok = t["token"]
st, cert = npmx.req("POST", "/nginx/certificates", {"provider": "letsencrypt", "nice_name": "entrenamientos.ies.com.uy",
    "domain_names": ["entrenamientos.ies.com.uy"], "meta": {"letsencrypt_agree": True, "dns_challenge": False}}, tok)
print("cert", st, cert if isinstance(cert, str) else {k: cert.get(k) for k in ("id", "domain_names", "expires_on")})
if st in (200, 201):
    st, h = npmx.req("PUT", "/nginx/proxy-hosts/11", {"certificate_id": cert["id"], "ssl_forced": True, "http2_support": True,
        "hsts_enabled": False, "block_exploits": True}, tok)
    print("host", st, h if isinstance(h, str) else {k: h.get(k) for k in ("id", "domain_names", "certificate_id", "ssl_forced", "http2_support", "enabled")})
