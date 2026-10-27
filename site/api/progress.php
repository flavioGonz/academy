<?php
/* IES Training · progreso del usuario. GET devuelve lo guardado; POST lo combina con lo que manda el navegador. */
declare(strict_types=1);
require __DIR__ . '/lib.php';

$u = require_role();
$st = db()->prepare('SELECT data FROM progress WHERE user_id=?'); $st->execute([$u['id']]);
$saved = json_decode((string)($st->fetchColumn() ?: '{}'), true) ?: [];
$saved += ['l' => []];

if ($_SERVER['REQUEST_METHOD'] === 'GET') out(200, ['progress' => $saved]);

require_write();
$in = body();
$inc = is_array($in['l'] ?? null) ? $in['l'] : [];
if (count($inc) > 5000) out(413, ['error' => 'Demasiados datos.']);

/* Combinación: lo hecho no se deshace por sincronizar, salvo que el navegador lo desmarque explícitamente (replace=true). */
$replace = !empty($in['replace']);
if (!empty($in['clear'])) $saved['l'] = [];
foreach ($inc as $k => $v) {
    if (!is_string($k) || !preg_match('#^[a-z0-9-]{2,40}/[A-Za-z0-9_-]{1,24}$#', $k) || !is_array($v)) continue;
    $cur = $saved['l'][$k] ?? [];
    $m = [];
    foreach (['seen', 'lab', 'done', 'rule'] as $f) $m[$f] = $replace ? !empty($v[$f]) : (!empty($v[$f]) || !empty($cur[$f]));
    $qa = is_array($v['quiz'] ?? null) ? $v['quiz'] : [];
    $qb = is_array($cur['quiz'] ?? null) ? $cur['quiz'] : [];
    $pick = $replace ? $qa : ((!empty($qa['done']) || count($qa['a'] ?? []) >= count($qb['a'] ?? [])) ? $qa : $qb);
    if ($pick) $m['quiz'] = ['done' => !empty($pick['done']) || (!$replace && !empty($qb['done'])), 'a' => array_slice(array_map(fn($x) => $x === null ? null : (int)$x, (array)($pick['a'] ?? [])), 0, 10)];
    // fecha (servidor) en que se completó la lección y en que se hizo el laboratorio, para las estadísticas
    if (!empty($m['done'])) $m['t'] = (int)($cur['t'] ?? 0) ?: time();
    if (!empty($m['lab'])) $m['tl'] = (int)($cur['tl'] ?? 0) ?: time();
    $saved['l'][$k] = array_filter($m, fn($x) => $x !== false && $x !== null);
}
if (isset($in['name']) && is_string($in['name'])) $saved['name'] = mb_substr($in['name'], 0, 80);
$json = json_encode($saved, JSON_UNESCAPED_UNICODE);
db()->prepare('INSERT INTO progress(user_id,data,updated) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET data=excluded.data, updated=excluded.updated')
    ->execute([$u['id'], $json, date('c')]);
out(200, ['progress' => $saved]);
