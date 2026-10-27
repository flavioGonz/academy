<?php
/* IES Training · administración: usuarios registrados y edición de cursos. Solo rol admin
   (los editores pueden editar cursos, no usuarios). */
declare(strict_types=1);
require __DIR__ . '/lib.php';

$a = $_GET['a'] ?? '';
$me = require_role('admin', 'editor');
$isAdmin = $me['role'] === 'admin';
$DATA = web_root() . '/data';
$HIST = data_dir() . '/historial';

function catalog(): array {
    global $DATA;
    return json_decode((string)@file_get_contents("$DATA/catalog.json"), true) ?: ['courses' => [], 'order' => []];
}
function course_file(string $slug): string { global $DATA; return "$DATA/$slug.json"; }
function read_course(string $slug): array {
    if (!valid_slug($slug) || !is_file(course_file($slug))) out(404, ['error' => 'No existe ese curso.']);
    return json_decode((string)file_get_contents(course_file($slug)), true) ?: [];
}
function lid(array $l): string { return (string)($l['id'] ?? $l['n']); }
function catalog_entry(array $c): array {
    $lab = 0; foreach ($c['lessons'] as $l) $lab += (int)($l['lab']['minutes'] ?? 0);
    return ['slug' => $c['slug'], 'title' => $c['title'], 'vendor' => $c['vendor'] ?? '', 'tagline' => $c['tagline'] ?? '',
            'level' => $c['level'] ?? '', 'draft' => !empty($c['draft']), 'logo' => $c['logo'] ?? null,
            'lessons' => array_map(fn($l) => ['n' => $l['n'], 'id' => lid($l), 'handle' => $l['handle']], $c['lessons']),
            'lab_minutes' => $lab, 'sources_count' => $c['sources_count'] ?? null];
}
function save_catalog(array $cat): void { global $DATA; atomic_write("$DATA/catalog.json", json_encode($cat, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)); }
function history_snapshot(string $slug, string $who): void {
    global $HIST;
    if (!is_file(course_file($slug))) return;
    $d = "$HIST/$slug"; if (!is_dir($d)) mkdir($d, 0750, true);
    copy(course_file($slug), "$d/" . date('Ymd-His') . '-' . preg_replace('/[^a-z0-9]/i', '', $who) . '.json');
    $all = glob("$d/*.json"); sort($all);
    foreach (array_slice($all, 0, max(0, count($all) - 60)) as $old) @unlink($old); // se guardan las últimas 60 versiones
}
function clean_html($h): string {
    $h = preg_replace(['#<script\b[^>]*>.*?</script>#is', '#<(object|embed|form)\b[^>]*>.*?</\1>#is', '#\son\w+\s*=\s*("[^"]*"|\'[^\']*\')#i', '#javascript:#i'], ['', '', '', ''], (string)$h);
    // iframes: solo reproductores de YouTube (sin cookies) y Vimeo
    return preg_replace_callback('#<iframe\b[^>]*>(?:.*?</iframe>)?#is', fn($m) => preg_match('#\ssrc="https://(www\.youtube-nocookie\.com/embed/[A-Za-z0-9_-]{11}|player\.vimeo\.com/video/\d{5,12})[^"]*"#i', $m[0]) ? $m[0] : '', $h);
}
function pics_ok($arr): array {
    $out = [];
    foreach (array_slice((array)$arr, 0, 6) as $p) {
        $src = (string)($p['src'] ?? '');
        if (!preg_match('#^(ilustraciones|capturas)/[A-Za-z0-9_/-]+\.(webp|png|jpg|jpeg|gif)$#', $src) || str_contains($src, '..')) continue;
        $out[] = ['src' => $src, 'caption' => mb_substr(trim((string)($p['caption'] ?? '')), 0, 300)];
    }
    return $out;
}
function s($v, int $max = 2000): string { return mb_substr(trim((string)$v), 0, $max); }

function normalize_course(array $c, string $slug): array {
    if (s($c['title'] ?? '') === '') out(400, ['error' => 'El curso necesita un título.']);
    $lessons = []; $n = 0; $ids = [];
    foreach ((array)($c['lessons'] ?? []) as $l) {
        if (!is_array($l)) continue;
        $n++;
        $id = preg_match('/^[A-Za-z0-9_-]{1,24}$/', (string)($l['id'] ?? '')) ? (string)$l['id'] : (string)$n;
        if (isset($ids[$id])) $id = substr(bin2hex(random_bytes(4)), 0, 8);
        $ids[$id] = true;
        if (s($l['handle'] ?? '') === '') out(400, ['error' => "La lección $n necesita un nombre."]);
        $quiz = [];
        foreach ((array)($l['quiz'] ?? []) as $q) {
            $opts = array_values(array_filter(array_map(fn($o) => s($o, 400), (array)($q['options'] ?? [])), 'strlen'));
            if (s($q['q'] ?? '') === '' || count($opts) < 2) continue;
            $quiz[] = ['q' => s($q['q'], 600), 'options' => $opts, 'answer' => max(0, min(count($opts) - 1, (int)($q['answer'] ?? 0))), 'why' => s($q['why'] ?? '', 1200)];
        }
        $sources = [];
        foreach ((array)($l['sources'] ?? []) as $x) {
            $url = s($x['url'] ?? '', 600);
            if (!preg_match('#^https?://#i', $url)) continue;
            $sources[] = ['label' => s($x['label'] ?? '', 200) ?: $url, 'url' => $url];
        }
        $script = [];
        foreach ((array)($l['script'] ?? []) as $x) {
            if (s($x['t'] ?? '') === '') continue;
            $script[] = ['s' => ($x['s'] ?? 'A') === 'B' ? 'B' : 'A', 't' => s($x['t'], 1200)];
        }
        $lessons[] = [
            'n' => $n, 'id' => $id, 'handle' => s($l['handle'], 80), 'summary' => s($l['summary'] ?? '', 300),
            'idea' => array_map('clean_html', array_slice((array)($l['idea'] ?? []), 0, 6)),
            'idea_md' => array_map(fn($x) => s($x, 600), array_slice((array)($l['idea_md'] ?? []), 0, 6)),
            'impact' => clean_html($l['impact'] ?? ''), 'impact_md' => s($l['impact_md'] ?? '', 800),
            'who' => clean_html($l['who'] ?? ''), 'who_md' => s($l['who_md'] ?? '', 800),
            'lab' => ['energy' => s($l['lab']['energy'] ?? '', 30), 'minutes' => ($l['lab']['minutes'] ?? '') === '' ? null : max(0, min(240, (int)$l['lab']['minutes'])),
                      'md' => s($l['lab']['md'] ?? '', 40000), 'html' => clean_html($l['lab']['html'] ?? '')],
            'rule' => s($l['rule'] ?? '', 400), 'sources' => $sources, 'script' => $script, 'quiz' => $quiz,
        ];
        // ilustración principal y conceptos ("para qué se creó, cómo se usa, ejemplo")
        $fig = (array)($l['fig'] ?? []);
        if (preg_match('#^(ilustraciones|capturas)/[A-Za-z0-9_/-]+\.(webp|png|jpg|jpeg|gif|svg)$#', (string)($fig['src'] ?? '')) && !str_contains((string)$fig['src'], '..'))
            $lessons[count($lessons) - 1]['fig'] = ['src' => $fig['src'], 'alt' => s($fig['alt'] ?? '', 400), 'caption' => s($fig['caption'] ?? '', 300)];
        $concepts = [];
        foreach (array_slice((array)($l['concepts'] ?? []), 0, 8) as $k) {
            if (!is_array($k) || s($k['name'] ?? '') === '') continue;
            $kk = ['name' => s($k['name'], 80), 'para_que' => s($k['para_que'] ?? '', 1200), 'como' => s($k['como'] ?? '', 1500), 'ejemplo' => s($k['ejemplo'] ?? '', 1500)];
            if ($ps = pics_ok($k['pics'] ?? [])) $kk['pics'] = $ps;
            $concepts[] = $kk;
        }
        $L = &$lessons[count($lessons) - 1];
        if ($concepts) $L['concepts'] = $concepts;
        // fotos de cada idea (alineadas con idea_md) y teoría
        $ip = array_map('pics_ok', array_slice((array)($l['idea_pics'] ?? []), 0, 6));
        if (array_filter($ip)) $L['idea_pics'] = $ip;
        $obj = array_values(array_filter(array_map(fn($x) => s($x, 300), array_slice((array)($l['objetivos'] ?? []), 0, 5)), 'strlen'));
        if ($obj) $L['objetivos'] = $obj;
        foreach (['conecta', 'sigue'] as $f) if (s($l[$f] ?? '', 800) !== '') $L[$f] = s($l[$f], 800);
        $req = array_values(array_filter(array_map('strval', (array)($l['requisitos'] ?? [])), fn($x) => preg_match('/^[A-Za-z0-9_-]{1,24}$/', $x)));
        if ($req) $L['requisitos'] = $req;
        $au = (array)($l['auto'] ?? []);
        if (s($au['codigo'] ?? '', 16000) !== '') {
            $vars = [];
            foreach (array_slice((array)($au['variables'] ?? []), 0, 20) as $v) if (preg_match('/^[A-Z0-9_]{1,30}$/', (string)($v['nombre'] ?? ''))) $vars[] = ['nombre' => $v['nombre'], 'valor' => s($v['valor'] ?? '', 200), 'detalle' => s($v['detalle'] ?? '', 200)];
            $L['auto'] = ['titulo' => s($au['titulo'] ?? '', 160), 'descripcion' => s($au['descripcion'] ?? '', 600), 'variables' => $vars, 'codigo' => s($au['codigo'], 16000),
                          'notas' => array_values(array_filter(array_map(fn($x) => s($x, 300), array_slice((array)($au['notas'] ?? []), 0, 8)), 'strlen'))];
        }
        if (s($l['theory_md'] ?? '', 12000) !== '') { $L['theory_md'] = s($l['theory_md'], 12000); $L['theory'] = clean_html($l['theory'] ?? ''); }
        unset($L);
    }
    $arcs = [];
    foreach ((array)($c['arcs'] ?? []) as $ar) {
        $ls = array_values(array_filter(array_map('strval', (array)($ar['lessons'] ?? [])), fn($x) => isset($ids[$x])));
        if (s($ar['title'] ?? '') === '') continue;
        $ao = array_values(array_filter(array_map(fn($x) => s($x, 300), array_slice((array)($ar['objetivos'] ?? []), 0, 6)), 'strlen'));
        $arcs[] = ['title' => s($ar['title'], 120), 'why' => s($ar['why'] ?? '', 600), 'lessons' => $ls] + ($ao ? ['objetivos' => $ao] : []);
    }
    $listS = fn($k) => array_values(array_filter(array_map(fn($x) => s($x, 400), (array)($c[$k] ?? [])), 'strlen'));
    $splits = [];
    foreach ((array)($c['splits'] ?? []) as $sp) if (s($sp['topic'] ?? '') !== '') $splits[] = ['topic' => clean_html(s($sp['topic'], 300)), 'sides' => clean_html(s($sp['sides'] ?? '', 1200)), 'decide' => clean_html(s($sp['decide'] ?? '', 800))];
    return [
        'slug' => $slug, 'title' => s($c['title'], 140), 'vendor' => s($c['vendor'] ?? '', 60), 'tagline' => s($c['tagline'] ?? '', 240),
        'description' => s($c['description'] ?? '', 1500), 'level' => s($c['level'] ?? 'Inicial a intermedio', 60), 'audience' => s($c['audience'] ?? '', 400),
        'prerequisites' => $listS('prerequisites'), 'outcomes' => $listS('outcomes'), 'version_note' => s($c['version_note'] ?? '', 800),
        'arcs' => $arcs, 'splits' => $splits, 'sources_count' => isset($c['sources_count']) ? (int)$c['sources_count'] : null,
        'draft' => !empty($c['draft']), 'updated' => date('c'), 'lessons' => $lessons,
        'objetivo' => s($c['objetivo'] ?? '', 400), 'recorrido' => s($c['recorrido'] ?? '', 1200), 'secuencial' => !isset($c['secuencial']) || !empty($c['secuencial']),
        'logo' => preg_match('#^logos/[a-z0-9-]+\.(png|jpg|webp)$#', (string)($c['logo'] ?? '')) ? $c['logo'] : null,
    ];
}

function user_summary(array $u, array $courses): array {
    $st = db()->prepare('SELECT data, updated FROM progress WHERE user_id=?'); $st->execute([$u['id']]);
    $row = $st->fetch(); $p = json_decode((string)($row['data'] ?? '{}'), true)['l'] ?? [];
    $per = []; $done = 0; $labs = 0; $quiz = 0;
    foreach ($courses as $c) {
        $d = 0;
        foreach ($c['lessons'] as $l) {
            $x = $p[$c['slug'] . '/' . ($l['id'] ?? $l['n'])] ?? [];
            if (!empty($x['done'])) $d++;
            if (!empty($x['lab'])) $labs++;
            if (!empty($x['quiz']['done'])) $quiz++;
        }
        if ($d) $per[$c['slug']] = ['done' => $d, 'total' => count($c['lessons'])];
        $done += $d;
    }
    return public_user($u) + ['created' => $u['created'], 'last_seen' => $u['last_seen'], 'progress_updated' => $row['updated'] ?? null,
        'done' => $done, 'labs' => $labs, 'quizzes' => $quiz, 'courses' => $per,
        'completed' => count(array_filter($per, fn($x) => $x['done'] >= $x['total']))];
}
function temp_password(): string { return 'ies-' . substr(strtr(base64_encode(random_bytes(9)), '+/', 'xy'), 0, 10); }

function media_count(string $slug): array {
    $n = ['total' => 0, 'video' => 0, 'gif' => 0, 'por_leccion' => []];
    foreach (glob(web_root() . "/capturas/$slug/*/index.json") ?: [] as $f) {
        $items = json_decode((string)file_get_contents($f), true) ?: [];
        $k = basename(dirname($f)); $k = ctype_digit($k) ? (string)(int)$k : $k;
        $n['por_leccion'][$k] = count($items); $n['total'] += count($items);
        foreach ($items as $x) { $t = $x['tipo'] ?? 'imagen'; if ($t === 'video' || $t === 'embed') $n['video']++; elseif ($t === 'gif') $n['gif']++; }
    }
    return $n;
}
/* Salud del contenido: lo que le falta a cada lección para estar completa. */
function course_health(array $c): array {
    $issues = [];
    foreach ($c['lessons'] as $l) {
        $miss = [];
        if (trim((string)($l['lab']['md'] ?? '')) === '') $miss[] = 'laboratorio';
        if (count($l['quiz'] ?? []) < 3) $miss[] = 'quiz';
        if (!count($l['sources'] ?? [])) $miss[] = 'fuentes';
        if (count(array_filter((array)($l['idea_md'] ?? $l['idea'] ?? []), fn($x) => trim(strip_tags((string)$x)) !== '')) < 3) $miss[] = 'idea';
        if ($miss) $issues[] = ['id' => lid($l), 'n' => $l['n'], 'handle' => $l['handle'], 'falta' => $miss];
    }
    return $issues;
}
function progress_rows(): array {
    return db()->query('SELECT p.user_id, p.data, u.name, u.company, u.role, u.active FROM progress p JOIN users u ON u.id=p.user_id')->fetchAll();
}

/* ---------- lecturas ---------- */
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if ($a === 'users' || $a === 'stats') {
        if (!$isAdmin) out(403, ['error' => 'Solo administradores.']);
        $courses = catalog()['courses'];
        $users = array_map(fn($u) => user_summary($u, $courses), db()->query('SELECT * FROM users ORDER BY created DESC')->fetchAll());
        if ($a === 'users') out(200, ['users' => $users]);
        $week = date('c', time() - 7 * 86400);
        $byCourse = [];
        foreach ($courses as $c) {
            $started = 0; $finished = 0;
            foreach ($users as $u) { if (isset($u['courses'][$c['slug']])) { $started++; if ($u['courses'][$c['slug']]['done'] >= count($c['lessons'])) $finished++; } }
            $byCourse[] = ['slug' => $c['slug'], 'title' => $c['title'], 'lessons' => count($c['lessons']), 'started' => $started, 'finished' => $finished];
        }
        out(200, ['users' => count($users), 'active7' => count(array_filter($users, fn($u) => ($u['last_seen'] ?? '') > $week)),
                  'lessons_done' => array_sum(array_column($users, 'done')), 'certificates' => array_sum(array_column($users, 'completed')), 'courses' => $byCourse]);
    }
    if ($a === 'dashboard') {
        if (!$isAdmin) out(403, ['error' => 'Solo administradores.']);
        $cat = catalog(); $courses = $cat['courses'];
        $users = db()->query('SELECT * FROM users ORDER BY created DESC')->fetchAll();
        $sum = array_map(fn($u) => user_summary($u, $courses), $users);
        $now = time(); $day = fn($ts) => date('Y-m-d', $ts);
        $days = []; for ($i = 29; $i >= 0; $i--) $days[$day($now - $i * 86400)] = ['lecciones' => 0, 'laboratorios' => 0, 'registros' => 0, 'activos' => []];
        foreach ($users as $u) { $d = substr((string)$u['created'], 0, 10); if (isset($days[$d])) $days[$d]['registros']++; }
        // activos por día: ingresos registrados en la auditoría + lecciones completadas
        $logins = db()->prepare("SELECT at, user_id FROM audit WHERE user_id IS NOT NULL AND at >= ?");
        $logins->execute([date('c', $now - 30 * 86400)]);
        foreach ($logins as $r) { $d = substr($r['at'], 0, 10); if (isset($days[$d])) $days[$d]['activos'][$r['user_id']] = 1; }
        // datos finos de las lecciones y de los quizzes
        $full = []; foreach ($courses as $c) { $f = course_file($c['slug']); if (is_file($f)) $full[$c['slug']] = json_decode((string)file_get_contents($f), true); }
        $qstat = []; $courseQ = []; $done7 = 0; $done30 = 0;
        foreach (progress_rows() as $r) {
            $p = json_decode((string)$r['data'], true)['l'] ?? [];
            foreach ($p as $k => $x) {
                [$slug, $id] = explode('/', $k, 2) + [1 => ''];
                if (!empty($x['t'])) { $d = $day((int)$x['t']); if (isset($days[$d])) { $days[$d]['lecciones']++; $days[$d]['activos'][$r['user_id']] = 1; $done30++; } if ($x['t'] >= $now - 7 * 86400) $done7++; }
                if (!empty($x['tl'])) { $d = $day((int)$x['tl']); if (isset($days[$d])) $days[$d]['laboratorios']++; }
                $ans = $x['quiz']['a'] ?? []; if (!$ans || !isset($full[$slug])) continue;
                $les = null; foreach ($full[$slug]['lessons'] as $l) if (lid($l) === $id) { $les = $l; break; }
                if (!$les) continue;
                foreach ($ans as $qi => $pick) {
                    if ($pick === null || !isset($les['quiz'][$qi])) continue;
                    $ok = (int)$pick === (int)$les['quiz'][$qi]['answer'];
                    $key = "$slug/$id/$qi";
                    $qstat[$key] ??= ['slug' => $slug, 'id' => $id, 'n' => $les['n'], 'handle' => $les['handle'], 'q' => $les['quiz'][$qi]['q'], 'intentos' => 0, 'errores' => 0];
                    $qstat[$key]['intentos']++; if (!$ok) $qstat[$key]['errores']++;
                    $courseQ[$slug] ??= [0, 0]; $courseQ[$slug][0]++; if ($ok) $courseQ[$slug][1]++;
                }
            }
        }
        $hard = array_values(array_filter($qstat, fn($q) => $q['intentos'] >= 3 && $q['errores'] > 0));
        usort($hard, fn($a, $b) => $b['errores'] / $b['intentos'] <=> $a['errores'] / $a['intentos'] ?: $b['intentos'] <=> $a['intentos']);
        $byCourse = [];
        foreach ($cat['order'] as $slug) {
            $c = null; foreach ($courses as $x) if ($x['slug'] === $slug) $c = $x; if (!$c) continue;
            $t = count($c['lessons']); $started = 0; $finished = 0; $sumPct = 0;
            foreach ($sum as $u) if (isset($u['courses'][$slug])) { $started++; $sumPct += $u['courses'][$slug]['done'] / max(1, $t); if ($u['courses'][$slug]['done'] >= $t) $finished++; }
            $m = media_count($slug);
            $byCourse[] = ['slug' => $slug, 'title' => $c['title'], 'vendor' => $c['vendor'] ?? '', 'logo' => $c['logo'] ?? null, 'draft' => !empty($c['draft']),
                'lessons' => $t, 'started' => $started, 'finished' => $finished, 'avg' => $started ? (int)round($sumPct / $started * 100) : 0,
                'quiz_ok' => isset($courseQ[$slug]) ? (int)round($courseQ[$slug][1] / $courseQ[$slug][0] * 100) : null,
                'media' => $m['total'], 'pendientes' => isset($full[$slug]) ? count(course_health($full[$slug])) : 0];
        }
        $companies = [];
        foreach ($users as $u) { $k = trim((string)$u['company']) ?: 'Sin empresa'; $companies[$k] = ($companies[$k] ?? 0) + 1; }
        arsort($companies);
        $top = $sum; usort($top, fn($a, $b) => $b['done'] <=> $a['done'] ?: strcmp((string)$b['last_seen'], (string)$a['last_seen']));
        $top = array_map(fn($u) => array_intersect_key($u, array_flip(['id', 'name', 'company', 'role', 'done', 'completed', 'last_seen'])), array_slice(array_filter($top, fn($u) => $u['done'] > 0), 0, 8));
        $since = fn($n) => date('c', $now - $n * 86400);
        out(200, [
            'kpi' => ['users' => count($users), 'new7' => count(array_filter($users, fn($u) => $u['created'] >= $since(7))), 'new30' => count(array_filter($users, fn($u) => $u['created'] >= $since(30))),
                      'active7' => count(array_filter($users, fn($u) => ($u['last_seen'] ?? '') >= $since(7))), 'active30' => count(array_filter($users, fn($u) => ($u['last_seen'] ?? '') >= $since(30))),
                      'lessons_done' => array_sum(array_column($sum, 'done')), 'done7' => $done7, 'done30' => $done30,
                      'labs' => array_sum(array_column($sum, 'labs')), 'certificates' => array_sum(array_column($sum, 'completed')),
                      'staff' => count(array_filter($users, fn($u) => $u['role'] !== 'tecnico')), 'inactive' => count(array_filter($users, fn($u) => !$u['active']))],
            'days' => array_map(fn($d, $v) => ['d' => $d, 'lecciones' => $v['lecciones'], 'laboratorios' => $v['laboratorios'], 'registros' => $v['registros'], 'activos' => count($v['activos'])], array_keys($days), $days),
            'courses' => $byCourse, 'top' => $top, 'hard' => array_slice($hard, 0, 6),
            'companies' => array_slice(array_map(fn($k, $v) => ['name' => $k, 'n' => $v], array_keys($companies), $companies), 0, 6),
            'recent' => db()->query('SELECT a.at, a.action, a.detail, a.user_id, u.name FROM audit a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.id DESC LIMIT 10')->fetchAll(),
        ]);
    }
    if ($a === 'courses') {
        $cat = catalog(); $out = [];
        $prog = progress_rows();
        foreach ($cat['order'] as $slug) {
            $f = course_file($slug); if (!is_file($f)) continue;
            $c = json_decode((string)file_get_contents($f), true) ?: [];
            $learners = 0; foreach ($prog as $r) { $p = json_decode((string)$r['data'], true)['l'] ?? []; foreach ($p as $k => $x) if (str_starts_with($k, "$slug/") && (!empty($x['seen']) || !empty($x['done']) || !empty($x['lab']))) { $learners++; break; } }
            $m = media_count($slug); $h = course_health($c);
            $hist = glob("$HIST/$slug/*.json") ?: []; sort($hist);
            $out[] = ['slug' => $slug, 'title' => $c['title'] ?? $slug, 'vendor' => $c['vendor'] ?? '', 'tagline' => $c['tagline'] ?? '', 'logo' => $c['logo'] ?? null, 'draft' => !empty($c['draft']),
                'lessons' => count($c['lessons'] ?? []), 'arcs' => count($c['arcs'] ?? []), 'quiz' => array_sum(array_map(fn($l) => count($l['quiz'] ?? []), $c['lessons'] ?? [])),
                'lab_minutes' => array_sum(array_map(fn($l) => (int)($l['lab']['minutes'] ?? 0), $c['lessons'] ?? [])),
                'media' => $m, 'learners' => $learners, 'health' => $h, 'updated' => $c['updated'] ?? null, 'versions' => count($hist)];
        }
        out(200, ['courses' => $out]);
    }
    if ($a === 'user') {
        if (!$isAdmin) out(403, ['error' => 'Solo administradores.']);
        $st = db()->prepare('SELECT * FROM users WHERE id=?'); $st->execute([(int)($_GET['id'] ?? 0)]);
        $u = $st->fetch() ?: out(404, ['error' => 'No existe ese usuario.']);
        $log = db()->prepare('SELECT at, action, detail FROM audit WHERE user_id=? ORDER BY id DESC LIMIT 30'); $log->execute([$u['id']]);
        $p = db()->prepare('SELECT data FROM progress WHERE user_id=?'); $p->execute([$u['id']]);
        $pl = json_decode((string)($p->fetchColumn() ?: '{}'), true)['l'] ?? [];
        $names = []; foreach (catalog()['courses'] as $c) foreach ($c['lessons'] as $l) $names[$c['slug'] . '/' . lid($l)] = [$c['title'], $l['handle'], $l['n']];
        $hechos = [];
        foreach ($pl as $k => $x) if (!empty($x['t']) && isset($names[$k])) $hechos[] = ['t' => (int)$x['t'], 'curso' => $names[$k][0], 'slug' => explode('/', $k)[0], 'n' => $names[$k][2], 'handle' => $names[$k][1]];
        usort($hechos, fn($a, $b) => $b['t'] <=> $a['t']);
        out(200, ['user' => user_summary($u, catalog()['courses']), 'log' => $log->fetchAll(), 'hechos' => array_slice($hechos, 0, 20)]);
    }
    if ($a === 'course') out(200, ['course' => read_course((string)($_GET['slug'] ?? ''))]);
    if ($a === 'history') {
        $slug = (string)($_GET['slug'] ?? ''); if (!valid_slug($slug)) out(400, ['error' => 'Curso inválido.']);
        $files = array_reverse(glob("$HIST/$slug/*.json") ?: []);
        out(200, ['versions' => array_map(fn($f) => ['file' => basename($f), 'size' => filesize($f)], array_slice($files, 0, 60))]);
    }
    if ($a === 'audit') {
        if (!$isAdmin) out(403, ['error' => 'Solo administradores.']);
        out(200, ['log' => db()->query('SELECT a.at, a.action, a.detail, u.name FROM audit a LEFT JOIN users u ON u.id=a.user_id ORDER BY a.id DESC LIMIT 200')->fetchAll()]);
    }
    out(404, ['error' => 'Acción desconocida.']);
}

/* ---------- escrituras ---------- */
require_write();

/* Logo del curso (multipart: slug, logo). PNG, JPG o WebP; vacío = quitar. */
if ($a === 'logo') {
    $slug = (string)($_POST['slug'] ?? '');
    $c = read_course($slug);
    $f = $_FILES['logo'] ?? null;
    $logo = null;
    if ($f && ($f['error'] ?? 4) === UPLOAD_ERR_OK) {
        if ($f['size'] > 3 * 1024 * 1024) out(413, ['error' => 'El logo pesa más de 3 MB.']);
        $info = @getimagesize($f['tmp_name']);
        $ext = [IMAGETYPE_PNG => 'png', IMAGETYPE_JPEG => 'jpg', IMAGETYPE_WEBP => 'webp'][$info[2] ?? 0] ?? null;
        if (!$ext) out(415, ['error' => 'El logo tiene que ser PNG, JPG o WebP (mejor PNG con fondo transparente).']);
        $dir = web_root() . '/logos'; if (!is_dir($dir)) mkdir($dir, 0755, true);
        $name = $slug . '-' . substr(bin2hex(random_bytes(4)), 0, 6) . ".$ext";
        if (!move_uploaded_file($f['tmp_name'], "$dir/$name")) out(500, ['error' => 'No se pudo guardar el logo.']);
        @chmod("$dir/$name", 0644);
        $logo = "logos/$name";
    } elseif (empty($_POST['quitar'])) out(400, ['error' => 'No llegó el archivo del logo.']);
    history_snapshot($slug, $me['name']);
    if ($logo) $c['logo'] = $logo; else unset($c['logo']);
    $c['updated'] = date('c');
    atomic_write(course_file($slug), json_encode($c, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    $cat = catalog(); foreach ($cat['courses'] as $i => $e) if ($e['slug'] === $slug) $cat['courses'][$i] = catalog_entry($c); save_catalog($cat);
    audit((int)$me['id'], $logo ? 'logo cargado' : 'logo quitado', $slug);
    out(200, ['logo' => $logo, 'updated' => $c['updated']]);
}

$in = body();

if ($a === 'course_save') {
    $slug = (string)($in['course']['slug'] ?? '');
    if (!valid_slug($slug)) out(400, ['error' => 'Curso inválido.']);
    $exists = is_file(course_file($slug));
    if ($exists && ($in['base'] ?? '') !== '' && (read_course($slug)['updated'] ?? '') !== $in['base'])
        out(409, ['error' => 'Otra persona guardó este curso mientras lo editabas. Recargá para ver su versión.']);
    $c = normalize_course((array)$in['course'], $slug);
    history_snapshot($slug, $me['name']);
    atomic_write(course_file($slug), json_encode($c, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    $cat = catalog(); $found = false;
    foreach ($cat['courses'] as $i => $e) if ($e['slug'] === $slug) { $cat['courses'][$i] = catalog_entry($c); $found = true; }
    if (!$found) $cat['courses'][] = catalog_entry($c);
    if (!in_array($slug, $cat['order'], true)) $cat['order'][] = $slug;
    save_catalog($cat);
    audit((int)$me['id'], 'curso guardado', "$slug (" . count($c['lessons']) . ' lecciones)');
    out(200, ['course' => $c]);
}
if ($a === 'course_new') {
    $slug = strtolower(trim((string)($in['slug'] ?? '')));
    if (!valid_slug($slug)) out(400, ['error' => 'El identificador va en minúsculas, con letras, números y guiones (ej. bosch-incendio).']);
    if (is_file(course_file($slug))) out(409, ['error' => 'Ya existe un curso con ese identificador.']);
    $c = normalize_course(['title' => $in['title'] ?? 'Curso nuevo', 'vendor' => $in['vendor'] ?? '', 'draft' => true, 'arcs' => [['title' => 'Parte 1', 'lessons' => ['1']]],
        'lessons' => [['id' => '1', 'handle' => 'Primera lección', 'idea' => ['', '', ''], 'idea_md' => ['', '', ''], 'lab' => ['energy' => 'Rápido', 'minutes' => 10, 'md' => '', 'html' => ''], 'rule' => '']]], $slug);
    atomic_write(course_file($slug), json_encode($c, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    $cat = catalog(); $cat['courses'][] = catalog_entry($c); $cat['order'][] = $slug; save_catalog($cat);
    audit((int)$me['id'], 'curso creado', $slug);
    out(201, ['course' => $c]);
}
if ($a === 'catalog_order') {
    $cat = catalog(); $known = array_column($cat['courses'], 'slug');
    $order = array_values(array_filter((array)($in['order'] ?? []), fn($s) => in_array($s, $known, true)));
    foreach ($known as $k) if (!in_array($k, $order, true)) $order[] = $k;
    $cat['order'] = $order; save_catalog($cat);
    audit((int)$me['id'], 'orden del catálogo'); out(200, ['order' => $order]);
}
if ($a === 'restore') {
    $slug = (string)($in['slug'] ?? ''); $file = basename((string)($in['file'] ?? ''));
    if (!valid_slug($slug) || !is_file("$HIST/$slug/$file")) out(404, ['error' => 'No existe esa versión.']);
    $c = normalize_course(json_decode((string)file_get_contents("$HIST/$slug/$file"), true) ?: [], $slug);
    history_snapshot($slug, $me['name']);
    atomic_write(course_file($slug), json_encode($c, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    $cat = catalog(); foreach ($cat['courses'] as $i => $e) if ($e['slug'] === $slug) $cat['courses'][$i] = catalog_entry($c); save_catalog($cat);
    audit((int)$me['id'], 'versión restaurada', "$slug $file"); out(200, ['course' => $c]);
}

/* usuarios: solo admin */
if (!$isAdmin) out(403, ['error' => 'Solo administradores.']);
if ($a === 'user_update') {
    $id = (int)($in['id'] ?? 0);
    if ($id === (int)$me['id'] && (isset($in['role']) && $in['role'] !== 'admin' || isset($in['active']) && !$in['active'])) out(400, ['error' => 'No podés quitarte el rol de administrador ni desactivar tu propia cuenta.']);
    if (isset($in['role'])) { if (!in_array($in['role'], ROLES, true)) out(400, ['error' => 'Rol inválido.']); db()->prepare('UPDATE users SET role=? WHERE id=?')->execute([$in['role'], $id]); }
    if (isset($in['active'])) db()->prepare('UPDATE users SET active=? WHERE id=?')->execute([$in['active'] ? 1 : 0, $id]);
    audit((int)$me['id'], 'usuario modificado', "id $id " . json_encode(array_intersect_key($in, ['role' => 1, 'active' => 1])));
    $st = db()->prepare('SELECT * FROM users WHERE id=?'); $st->execute([$id]);
    out(200, ['user' => user_summary($st->fetch() ?: out(404, ['error' => 'No existe ese usuario.']), catalog()['courses'])]);
}
if ($a === 'user_reset') {
    $id = (int)($in['id'] ?? 0); $tmp = temp_password();
    $st = db()->prepare('UPDATE users SET pass=?, must_change=1 WHERE id=?'); $st->execute([password_hash($tmp, PASSWORD_DEFAULT), $id]);
    if (!$st->rowCount()) out(404, ['error' => 'No existe ese usuario.']);
    audit((int)$me['id'], 'contraseña reiniciada', "id $id");
    out(200, ['password' => $tmp]);
}
if ($a === 'user_create') {
    $email = strtolower(trim((string)($in['email'] ?? ''))); $name = trim((string)($in['name'] ?? ''));
    if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($name) < 3) out(400, ['error' => 'Completá nombre y un correo válido.']);
    $role = in_array($in['role'] ?? '', ROLES, true) ? $in['role'] : 'tecnico';
    $tmp = temp_password();
    try {
        db()->prepare('INSERT INTO users(name,email,company,pass,role,must_change,created) VALUES(?,?,?,?,?,1,?)')
            ->execute([mb_substr($name, 0, 80), $email, mb_substr(trim((string)($in['company'] ?? '')), 0, 80), password_hash($tmp, PASSWORD_DEFAULT), $role, date('c')]);
    } catch (PDOException $e) { out(409, ['error' => 'Ya hay una cuenta con ese correo.']); }
    audit((int)$me['id'], 'usuario creado', $email);
    out(201, ['password' => $tmp, 'id' => (int)db()->lastInsertId()]);
}
out(404, ['error' => 'Acción desconocida.']);
