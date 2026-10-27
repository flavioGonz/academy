<?php
/* IES Training · cuentas: registro, ingreso, salida, cambio de contraseña. */
declare(strict_types=1);
require __DIR__ . '/lib.php';

$a = $_GET['a'] ?? 'me';

if ($a === 'me') {
    $u = current_user();
    out(200, ['user' => $u ? public_user($u) : null]);
}

require_write();
$in = body();

if ($a === 'register') {
    if (too_many_attempts()) out(429, ['error' => 'Demasiados intentos. Probá de nuevo en 15 minutos.']);
    note_attempt();
    $name = trim((string)($in['name'] ?? ''));
    $email = strtolower(trim((string)($in['email'] ?? '')));
    $company = trim((string)($in['company'] ?? ''));
    $pass = (string)($in['password'] ?? '');
    if (mb_strlen($name) < 3 || mb_strlen($name) > 80) out(400, ['error' => 'Escribí tu nombre y apellido.']);
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(400, ['error' => 'El correo no parece válido.']);
    if (strlen($pass) < 8) out(400, ['error' => 'La contraseña necesita al menos 8 caracteres.']);
    $st = db()->prepare('SELECT 1 FROM users WHERE email=?'); $st->execute([$email]);
    if ($st->fetchColumn()) out(409, ['error' => 'Ya hay una cuenta con ese correo. Ingresá con tu contraseña.']);
    db()->prepare('INSERT INTO users(name,email,company,pass,role,created,last_seen) VALUES(?,?,?,?,?,?,?)')
        ->execute([$name, $email, mb_substr($company, 0, 80), password_hash($pass, PASSWORD_DEFAULT), 'tecnico', date('c'), date('c')]);
    $id = (int)db()->lastInsertId();
    start_session(); session_regenerate_id(true); $_SESSION['uid'] = $id;
    audit($id, 'registro', $email);
    $st = db()->prepare('SELECT * FROM users WHERE id=?'); $st->execute([$id]);
    out(201, ['user' => public_user($st->fetch())]);
}

if ($a === 'login') {
    if (too_many_attempts()) out(429, ['error' => 'Demasiados intentos. Probá de nuevo en 15 minutos.']);
    $email = strtolower(trim((string)($in['email'] ?? '')));
    $st = db()->prepare('SELECT * FROM users WHERE email=?'); $st->execute([$email]);
    $u = $st->fetch();
    if (!$u || !password_verify((string)($in['password'] ?? ''), $u['pass'])) {
        note_attempt();
        out(401, ['error' => 'El correo o la contraseña no coinciden.']);
    }
    if (!$u['active']) out(403, ['error' => 'Tu cuenta está desactivada. Pedile a IES que la reactive.']);
    if (password_needs_rehash($u['pass'], PASSWORD_DEFAULT)) db()->prepare('UPDATE users SET pass=? WHERE id=?')->execute([password_hash((string)$in['password'], PASSWORD_DEFAULT), $u['id']]);
    start_session(); session_regenerate_id(true); $_SESSION['uid'] = (int)$u['id'];
    db()->prepare('UPDATE users SET last_seen=? WHERE id=?')->execute([date('c'), $u['id']]);
    audit((int)$u['id'], 'ingreso');
    out(200, ['user' => public_user($u)]);
}

if ($a === 'logout') {
    start_session(); $_SESSION = []; session_destroy();
    out(200, ['ok' => true]);
}

if ($a === 'password') {
    $u = require_role();
    $new = (string)($in['new'] ?? '');
    if (!$u['must_change'] && !password_verify((string)($in['current'] ?? ''), $u['pass'])) out(401, ['error' => 'La contraseña actual no es correcta.']);
    if (strlen($new) < 8) out(400, ['error' => 'La contraseña nueva necesita al menos 8 caracteres.']);
    db()->prepare('UPDATE users SET pass=?, must_change=0 WHERE id=?')->execute([password_hash($new, PASSWORD_DEFAULT), $u['id']]);
    audit((int)$u['id'], 'cambio de contraseña');
    out(200, ['ok' => true]);
}

if ($a === 'profile') {
    $u = require_role();
    $name = trim((string)($in['name'] ?? $u['name']));
    if (mb_strlen($name) < 3) out(400, ['error' => 'Escribí tu nombre y apellido.']);
    db()->prepare('UPDATE users SET name=?, company=? WHERE id=?')->execute([mb_substr($name, 0, 80), mb_substr(trim((string)($in['company'] ?? $u['company'])), 0, 80), $u['id']]);
    $st = db()->prepare('SELECT * FROM users WHERE id=?'); $st->execute([$u['id']]);
    out(200, ['user' => public_user($st->fetch())]);
}

out(404, ['error' => 'Acción desconocida.']);
