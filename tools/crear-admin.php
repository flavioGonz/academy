<?php
/* Uso (en el CT): php /root/crear-admin.php "Nombre" correo@dominio  -> crea o promueve a admin y muestra una contraseña temporal. */
if (PHP_SAPI !== 'cli') exit(1);
require '/var/www/entrenamientos/api/lib.php';
[$_, $name, $email] = $argv + [null, null, null];
if (!$name || !filter_var($email, FILTER_VALIDATE_EMAIL)) { fwrite(STDERR, "uso: php crear-admin.php \"Nombre\" correo\n"); exit(2); }
$tmp = 'ies-' . substr(strtr(base64_encode(random_bytes(9)), '+/', 'xy'), 0, 10);
$st = db()->prepare('SELECT id FROM users WHERE email=?'); $st->execute([strtolower($email)]);
if ($id = $st->fetchColumn()) {
    db()->prepare("UPDATE users SET role='admin', active=1, pass=?, must_change=1 WHERE id=?")->execute([password_hash($tmp, PASSWORD_DEFAULT), $id]);
} else {
    db()->prepare("INSERT INTO users(name,email,pass,role,must_change,created) VALUES(?,?,?,'admin',1,?)")->execute([$name, strtolower($email), password_hash($tmp, PASSWORD_DEFAULT), date('c')]);
}
audit(null, 'admin creado por consola', $email);
echo "$email\n$tmp\n";
