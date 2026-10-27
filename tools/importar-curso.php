<?php
/* Uso (en el CT, como www-data): php importar-curso.php <slug> <archivo.json> [--forzar]
   Reemplaza un curso por una versión nueva generada fuera del panel. Guarda la actual en el historial
   y se niega si el curso ya fue editado desde el panel (salvo --forzar). */
if (PHP_SAPI !== 'cli') exit(1);
require '/var/www/entrenamientos/api/lib.php';
[$_, $slug, $file] = $argv + [null, null, null];
$force = in_array('--forzar', $argv, true);
if (!valid_slug($slug) || !is_file($file)) { fwrite(STDERR, "uso: php importar-curso.php slug archivo.json [--forzar]\n"); exit(2); }
$W = '/var/www/entrenamientos/data'; $H = data_dir() . "/historial/$slug";
$edited = is_dir($H) && count(glob("$H/*.json")) > 0;
if ($edited && !$force) { fwrite(STDERR, "El curso $slug ya tiene ediciones desde el panel. Revisá antes o usá --forzar.\n"); exit(3); }
$c = json_decode(file_get_contents($file), true);
if (!$c || ($c['slug'] ?? '') !== $slug || empty($c['lessons'])) { fwrite(STDERR, "Archivo inválido.\n"); exit(4); }
if (!is_dir($H)) mkdir($H, 0750, true);
// el logo se sube desde el panel: se conserva si el archivo importado no trae uno
$prev = is_file("$W/$slug.json") ? (json_decode(file_get_contents("$W/$slug.json"), true) ?: []) : [];
if (empty($c['logo']) && !empty($prev['logo'])) $c['logo'] = $prev['logo'];
if (is_file("$W/$slug.json")) copy("$W/$slug.json", "$H/" . date('Ymd-His') . "-importacion.json");
$c['updated'] = date('c');
atomic_write("$W/$slug.json", json_encode($c, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
$cat = json_decode(file_get_contents("$W/catalog.json"), true);
$lab = 0; foreach ($c['lessons'] as $l) $lab += (int)($l['lab']['minutes'] ?? 0);
$entry = ['slug' => $slug, 'title' => $c['title'], 'vendor' => $c['vendor'] ?? '', 'tagline' => $c['tagline'] ?? '', 'level' => $c['level'] ?? '',
  'draft' => !empty($c['draft']), 'logo' => $c['logo'] ?? null, 'lessons' => array_map(fn($l) => ['n' => $l['n'], 'id' => (string)($l['id'] ?? $l['n']), 'handle' => $l['handle']], $c['lessons']),
  'lab_minutes' => $lab, 'sources_count' => $c['sources_count'] ?? null];
$found = false; foreach ($cat['courses'] as $i => $e) if ($e['slug'] === $slug) { $cat['courses'][$i] = $entry; $found = true; }
if (!$found) { $cat['courses'][] = $entry; $cat['order'][] = $slug; }
atomic_write("$W/catalog.json", json_encode($cat, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
audit(null, 'curso importado', "$slug (" . count($c['lessons']) . " lecciones)");
echo "ok $slug: " . count($c['lessons']) . " lecciones\n";
