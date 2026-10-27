<?php
/* IES Training · contenido de un curso.
   GET course.php?slug=mikrotik
   - Con sesión (cualquier cuenta activa): el curso completo.
   - Sin sesión: solo el temario (títulos de partes y lecciones, minutos de laboratorio, cantidad de preguntas)
     y "locked": true. Los borradores solo los ve el equipo (editor o admin). */
declare(strict_types=1);
require __DIR__ . '/lib.php';

$slug = (string)($_GET['slug'] ?? '');
if (!valid_slug($slug)) out(400, ['error' => 'Curso inválido.']);
$f = web_root() . "/data/$slug.json";
if (!is_file($f)) out(404, ['error' => 'No existe ese curso.']);
$c = json_decode((string)file_get_contents($f), true) ?: [];
$u = current_user();
$staff = $u && in_array($u['role'], ['admin', 'editor'], true);
if (!empty($c['draft']) && !$staff) out(404, ['error' => 'No existe ese curso.']);
if ($u) { header('Vary: Cookie'); out(200, ['course' => $c + ['locked' => false]]); }

$keep = ['slug', 'title', 'vendor', 'tagline', 'description', 'level', 'audience', 'prerequisites', 'outcomes', 'version_note', 'arcs', 'sources_count', 'updated', 'logo', 'draft', 'objetivo', 'recorrido', 'secuencial'];
$o = array_intersect_key($c, array_flip($keep));
$o['splits_count'] = count($c['splits'] ?? []);
$o['lessons'] = array_map(fn($l) => [
    'n' => $l['n'], 'id' => (string)($l['id'] ?? $l['n']), 'handle' => $l['handle'],
    'lab' => ['minutes' => $l['lab']['minutes'] ?? null, 'energy' => $l['lab']['energy'] ?? ''],
    'quiz_n' => count($l['quiz'] ?? []), 'objetivos' => $l['objetivos'] ?? [],
], $c['lessons'] ?? []);
$o['locked'] = true;
out(200, ['course' => $o]);
