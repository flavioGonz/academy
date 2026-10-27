<?php
/* IES Training · funciones comunes de la API (sesiones, base de datos, permisos). */
declare(strict_types=1);

const ROLES = ['tecnico', 'editor', 'admin'];

function cfg(): array {
    static $c = null;
    if ($c === null) $c = is_file(__DIR__ . '/config.php') ? (require __DIR__ . '/config.php') : [];
    return $c;
}
function data_dir(): string {
    $d = cfg()['data_dir'] ?? dirname(__DIR__, 2) . '/entrenamientos-data';
    if (!is_dir($d)) mkdir($d, 0750, true);
    return $d;
}
function web_root(): string { return dirname(__DIR__); }

function out(int $code, $data): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function body(): array {
    $raw = (string)file_get_contents('php://input');
    $j = json_decode($raw, true);
    return is_array($j) ? $j : [];
}
/* Las escrituras exigen un encabezado propio: un sitio ajeno no puede mandarlo sin CORS. */
function require_write(): void {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, ['error' => 'Método no permitido.']);
    if (($_SERVER['HTTP_X_IES'] ?? '') !== '1') out(400, ['error' => 'Solicitud no válida.']);
}

function db(): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $pdo = new PDO('sqlite:' . data_dir() . '/ies-training.sqlite');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $pdo->exec('PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=4000;');
    $pdo->exec("CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE COLLATE NOCASE, company TEXT DEFAULT '',
        pass TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'tecnico', active INTEGER NOT NULL DEFAULT 1,
        must_change INTEGER NOT NULL DEFAULT 0, created TEXT NOT NULL, last_seen TEXT)");
    $pdo->exec("CREATE TABLE IF NOT EXISTS progress(user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE, data TEXT NOT NULL, updated TEXT NOT NULL)");
    $pdo->exec("CREATE TABLE IF NOT EXISTS attempts(ip TEXT NOT NULL, at INTEGER NOT NULL)");
    $pdo->exec("CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, at TEXT NOT NULL, user_id INTEGER, action TEXT NOT NULL, detail TEXT)");
    return $pdo;
}
function audit(?int $uid, string $action, string $detail = ''): void {
    db()->prepare('INSERT INTO audit(at,user_id,action,detail) VALUES(?,?,?,?)')->execute([date('c'), $uid, $action, mb_substr($detail, 0, 500)]);
}

function start_session(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $secure = (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https') || (($_SERVER['HTTPS'] ?? '') === 'on');
    session_name('ies_training');
    session_set_cookie_params(['lifetime' => 60 * 60 * 24 * 30, 'path' => '/', 'secure' => $secure, 'httponly' => true, 'samesite' => 'Lax']);
    ini_set('session.gc_maxlifetime', (string)(60 * 60 * 24 * 30));
    $sd = data_dir() . '/sesiones';
    if (!is_dir($sd)) mkdir($sd, 0700, true);
    session_save_path($sd);
    session_start();
}
function public_user(array $u): array {
    return ['id' => (int)$u['id'], 'name' => $u['name'], 'email' => $u['email'], 'company' => $u['company'] ?? '',
            'role' => $u['role'], 'active' => (bool)$u['active'], 'must_change' => (bool)$u['must_change']];
}
function current_user(): ?array {
    if (session_status() !== PHP_SESSION_ACTIVE && empty($_COOKIE['ies_training'])) return null; // sin cookie no hay sesión: no se crea una para visitantes
    start_session();
    $id = $_SESSION['uid'] ?? null;
    if (!$id) return null;
    $st = db()->prepare('SELECT * FROM users WHERE id=?'); $st->execute([$id]);
    $u = $st->fetch();
    if (!$u || !$u['active']) { $_SESSION = []; return null; }
    if (!isset($_SESSION['seen']) || time() - $_SESSION['seen'] > 300) {
        db()->prepare('UPDATE users SET last_seen=? WHERE id=?')->execute([date('c'), $id]);
        $_SESSION['seen'] = time();
    }
    return $u;
}
function require_role(string ...$roles): array {
    $u = current_user();
    if (!$u) out(401, ['error' => 'Iniciá sesión para continuar.']);
    if ($roles && !in_array($u['role'], $roles, true)) out(403, ['error' => 'Tu cuenta no tiene permiso para esto.']);
    return $u;
}
function client_ip(): string {
    $f = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? '';
    return trim(explode(',', $f)[0]) ?: ($_SERVER['REMOTE_ADDR'] ?? '?');
}
function too_many_attempts(): bool {
    $st = db()->prepare('SELECT COUNT(*) FROM attempts WHERE ip=? AND at>?');
    $st->execute([client_ip(), time() - 900]);
    return (int)$st->fetchColumn() >= 10;
}
function note_attempt(): void {
    db()->prepare('INSERT INTO attempts(ip,at) VALUES(?,?)')->execute([client_ip(), time()]);
    db()->prepare('DELETE FROM attempts WHERE at<?')->execute([time() - 86400]);
}
function valid_slug($s): bool { return is_string($s) && (bool)preg_match('/^[a-z0-9-]{2,40}$/', $s); }
function atomic_write(string $file, string $content): void {
    $tmp = $file . '.tmp' . bin2hex(random_bytes(3));
    if (file_put_contents($tmp, $content) === false) out(500, ['error' => 'No se pudo escribir ' . basename($file) . '.']);
    @chmod($tmp, 0644);
    rename($tmp, $file);
}
