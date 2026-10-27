set -e
# Muestra qu?? cambi?? en __SLUG__ desde el panel (versi??n vigente contra la anterior del historial).
pct exec 115 -- php -r '
$h = glob("/var/www/entrenamientos-data/historial/__SLUG__/*.json"); sort($h);
$a = json_decode(file_get_contents($h[0]), true); $b = json_decode(file_get_contents("/var/www/entrenamientos/data/__SLUG__.json"), true);
echo "antes: ", basename($h[0]), " | vigente updated: ", $b["updated"] ?? "", PHP_EOL;
foreach ($b as $k => $v) if ($k !== "lessons" && $k !== "updated" && json_encode($a[$k] ?? null) !== json_encode($v)) echo "campo del curso: $k", PHP_EOL;
foreach ($a as $k => $v) if (!array_key_exists($k, $b)) echo "campo quitado: $k", PHP_EOL;
$ia = []; foreach ($a["lessons"] as $l) $ia[(string)($l["id"] ?? $l["n"])] = $l;
foreach ($b["lessons"] as $l) { $id = (string)($l["id"] ?? $l["n"]); if (!isset($ia[$id])) { echo "leccion nueva id $id: {$l["handle"]}", PHP_EOL; continue; }
  foreach ($l as $k => $v) if (json_encode($ia[$id][$k] ?? null) !== json_encode($v)) echo "leccion $id ({$l["handle"]}): $k", PHP_EOL; unset($ia[$id]); }
foreach ($ia as $id => $l) echo "leccion quitada id $id: {$l["handle"]}", PHP_EOL;
echo "arcos: ", json_encode(array_map(fn($x) => [$x["title"], $x["lessons"]], $b["arcs"]), JSON_UNESCAPED_UNICODE), PHP_EOL;
echo "logo: ", $b["logo"] ?? "-", PHP_EOL;
'
