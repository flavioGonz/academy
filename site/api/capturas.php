<?php
/*
 * IES Training · medios por lección: capturas, GIF animados, videos y videos de YouTube/Vimeo.
 *
 * GET  capturas.php?curso=mikrotik&leccion=5            → lista pública (sin los medios insertados en el texto)
 * POST multipart: curso, leccion, imagen (archivo), texto, inline=1?   → sube un archivo
 * POST JSON {accion:"borrar"|"texto"|"mover"|"embed", curso, leccion, id, texto, url, dir}
 * GET  capturas.php?verificar=1                         → 200 si la clave de editor o la sesión sirven
 *
 * Permiso: clave de editor (X-Editor-Key) o sesión de administrador/editor con X-IES: 1.
 * Los archivos quedan en ../capturas/<curso>/<leccion>/ con un index.json al lado.
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

const IMG_MAX = 12 * 1024 * 1024;
const GIF_MAX = 30 * 1024 * 1024;
const VID_MAX = 60 * 1024 * 1024;
const IMG_TIPOS = [IMAGETYPE_PNG => 'png', IMAGETYPE_JPEG => 'jpg', IMAGETYPE_WEBP => 'webp', IMAGETYPE_GIF => 'gif'];
require __DIR__ . '/lib.php';
$BASE = dirname(__DIR__) . '/capturas';
$CFG = cfg();

function fin(int $code, array $data): void { http_response_code($code); echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); exit; }
function clave_ok(array $cfg): bool {
    $k = $_SERVER['HTTP_X_EDITOR_KEY'] ?? '';
    if ($k !== '') return !empty($cfg['editor_hash']) && password_verify($k, $cfg['editor_hash']);
    $u = current_user();
    return $u && in_array($u['role'], ['admin', 'editor'], true) && ($_SERVER['HTTP_X_IES'] ?? '') === '1';
}
function destino(string $base, $curso, $leccion): array {
    $curso = (string)$curso; $leccion = (string)$leccion;
    if (!preg_match('/^[a-z0-9-]{1,40}$/', $curso) || !preg_match('/^[A-Za-z0-9_-]{1,24}$/', $leccion)) fin(400, ['error' => 'Curso o lección inválidos.']);
    $sub = ctype_digit($leccion) ? sprintf('%02d', (int)$leccion) : $leccion;
    return ["$base/$curso/$sub", "capturas/$curso/$sub"];
}
function leer(string $dir): array { $f = "$dir/index.json"; return is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : []; }
function guardar(string $dir, array $items): void {
    $tmp = "$dir/index.json." . bin2hex(random_bytes(4));
    file_put_contents($tmp, json_encode(array_values($items), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
    rename($tmp, "$dir/index.json");
}
function con_lock(string $dir, callable $fn) {
    if (!is_dir($dir) && !mkdir($dir, 0755, true)) fin(500, ['error' => 'No se pudo crear la carpeta de medios.']);
    $h = fopen("$dir/.lock", 'c'); flock($h, LOCK_EX);
    try { return $fn(); } finally { flock($h, LOCK_UN); fclose($h); }
}
/* YouTube / Vimeo → id del video. Solo se guardan esos dos proveedores. */
function embed_de(string $url): ?array {
    if (preg_match('#(?:youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/)|youtu\.be/)([A-Za-z0-9_-]{11})#', $url, $m)) return ['proveedor' => 'youtube', 'video' => $m[1]];
    if (preg_match('#vimeo\.com/(?:video/)?(\d{5,12})#', $url, $m)) return ['proveedor' => 'vimeo', 'video' => $m[1]];
    return null;
}
function tipo_video(string $file): ?string {
    $h = (string)file_get_contents($file, false, null, 0, 16);
    if (substr($h, 4, 4) === 'ftyp') return 'mp4';
    if (substr($h, 0, 4) === "\x1A\x45\xDF\xA3") return 'webm';
    return null;
}
function publico(array $x, string $url): array { return $x + (isset($x['archivo']) ? ['url' => "$url/{$x['archivo']}"] : []); }

$m = $_SERVER['REQUEST_METHOD'];
if ($m === 'GET' && isset($_GET['verificar'])) clave_ok($CFG) ? fin(200, ['ok' => true]) : fin(403, ['error' => 'Clave de editor incorrecta.']);
if ($m === 'GET') {
    if (!current_user() && !clave_ok($CFG)) fin(401, ['error' => 'Iniciá sesión para ver los medios de la lección.']);
    [$dir, $url] = destino($BASE, $_GET['curso'] ?? '', $_GET['leccion'] ?? 0);
    $items = array_values(array_filter(leer($dir), fn($x) => empty($x['inline'])));
    fin(200, ['capturas' => array_map(fn($x) => publico($x, $url), $items)]);
}
if ($m !== 'POST') fin(405, ['error' => 'Método no permitido.']);
if (!clave_ok($CFG)) fin(403, ['error' => 'No tenés permiso para cargar medios. Entrá con una cuenta de editor o administrador.']);

$ct = $_SERVER['CONTENT_TYPE'] ?? '';
if (str_starts_with($ct, 'application/json')) {
    $in = json_decode((string)file_get_contents('php://input'), true) ?: [];
    [$dir, $url] = destino($BASE, $in['curso'] ?? '', $in['leccion'] ?? 0);
    $accion = $in['accion'] ?? '';
    if ($accion === 'embed') {
        $e = embed_de((string)($in['url'] ?? ''));
        if (!$e) fin(400, ['error' => 'Pegá un enlace de YouTube o de Vimeo.']);
        $id = date('Ymd-His') . '-' . bin2hex(random_bytes(3));
        $x = ['id' => $id, 'tipo' => 'embed'] + $e + ['texto' => mb_substr(trim((string)($in['texto'] ?? '')), 0, 300), 'fecha' => date('c')];
        con_lock($dir, function () use ($dir, $x) { $items = leer($dir); $items[] = $x; guardar($dir, $items); });
        fin(201, ['captura' => $x]);
    }
    $id = (string)($in['id'] ?? '');
    $res = con_lock($dir, function () use ($dir, $id, $accion, $in) {
        $items = array_values(leer($dir)); $hit = false;
        foreach ($items as $i => $x) {
            if ($x['id'] !== $id) continue;
            $hit = true;
            if ($accion === 'borrar') {
                // No se borra el archivo: se aparta a _borradas/ por si hay que recuperarlo.
                if (isset($x['archivo'])) { @mkdir("$dir/_borradas", 0755); @rename("$dir/{$x['archivo']}", "$dir/_borradas/{$x['archivo']}"); }
                unset($items[$i]);
            } elseif ($accion === 'texto') {
                $items[$i]['texto'] = mb_substr(trim((string)($in['texto'] ?? '')), 0, 300);
            } elseif ($accion === 'mover') {
                // mueve entre los visibles de la galería
                $vis = array_keys(array_filter($items, fn($y) => empty($y['inline'])));
                $p = array_search($i, $vis, true); $q = $p + ((int)($in['dir'] ?? 0) < 0 ? -1 : 1);
                if ($p !== false && isset($vis[$q])) { $j = $vis[$q]; [$items[$i], $items[$j]] = [$items[$j], $items[$i]]; }
            }
            break;
        }
        if (!$hit) return false;
        guardar($dir, $items); return true;
    });
    $res ? fin(200, ['ok' => true]) : fin(404, ['error' => 'No se encontró el medio.']);
}

// Subida de archivo
[$dir, $url] = destino($BASE, $_POST['curso'] ?? '', $_POST['leccion'] ?? 0);
$f = $_FILES['imagen'] ?? null;
if (!$f || ($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
    $c = $f['error'] ?? 0;
    fin(400, ['error' => in_array($c, [UPLOAD_ERR_INI_SIZE, UPLOAD_ERR_FORM_SIZE], true) ? 'El archivo es demasiado grande.' : 'No llegó el archivo (código ' . ($c ?: 'sin archivo') . ').']);
}
$info = @getimagesize($f['tmp_name']);
if ($info && isset(IMG_TIPOS[$info[2]])) {
    $ext = IMG_TIPOS[$info[2]];
    $tipo = $ext === 'gif' ? 'gif' : 'imagen';
    if ($f['size'] > ($tipo === 'gif' ? GIF_MAX : IMG_MAX)) fin(413, ['error' => $tipo === 'gif' ? 'El GIF pesa más de 30 MB.' : 'La imagen pesa más de 12 MB.']);
    $dim = ['ancho' => $info[0], 'alto' => $info[1]];
} elseif ($v = tipo_video($f['tmp_name'])) {
    if ($f['size'] > VID_MAX) fin(413, ['error' => 'El video pesa más de 60 MB. Recortalo o bajale la resolución.']);
    $ext = $v; $tipo = 'video'; $dim = [];
} else {
    fin(415, ['error' => 'Formato no admitido. Imágenes PNG, JPG, WebP o GIF, y videos MP4 o WebM.']);
}
$id = date('Ymd-His') . '-' . bin2hex(random_bytes(3));
$archivo = "$id.$ext";
$item = con_lock($dir, function () use ($dir, $f, $archivo, $id, $tipo, $dim) {
    if (!move_uploaded_file($f['tmp_name'], "$dir/$archivo")) fin(500, ['error' => 'No se pudo guardar el archivo.']);
    @chmod("$dir/$archivo", 0644);
    $items = leer($dir);
    $x = ['id' => $id, 'tipo' => $tipo, 'archivo' => $archivo] + $dim + ['bytes' => (int)$f['size'],
          'texto' => mb_substr(trim((string)($_POST['texto'] ?? '')), 0, 300), 'fecha' => date('c')];
    if (!empty($_POST['inline'])) $x['inline'] = true;
    $items[] = $x; guardar($dir, $items); return $x;
});
fin(201, ['captura' => publico($item, $url)]);
