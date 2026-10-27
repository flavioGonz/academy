echo "== nodos"; pvesh get /cluster/resources --type node --output-format json | python3 -c "import json,sys;[print(n['node'],n.get('status'),'cpu%.0f%%'%(100*n.get('cpu',0)),'mem %.1f/%.1fG'%(n.get('mem',0)/2**30,n.get('maxmem',0)/2**30)) for n in json.load(sys.stdin)]"
echo "== guests"; pvesh get /cluster/resources --type vm --output-format json | python3 -c "import json,sys;[print(v['vmid'],v['type'],v['node'],v.get('name'),v.get('status')) for v in sorted(json.load(sys.stdin),key=lambda x:x['vmid'])]"
echo "== nextid"; pvesh get /cluster/nextid
echo "== storage pve01"; pvesm status 2>/dev/null
echo "== plantillas pve01"; pveam list local 2>/dev/null
