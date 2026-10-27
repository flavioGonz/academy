<?php
/* IES Training · control de acceso para nginx (auth_request) a /capturas/ y /ilustraciones/:
   204 si hay una sesión de una cuenta activa, 401 si no. No crea sesiones para visitantes. */
declare(strict_types=1);
require __DIR__ . '/lib.php';
header('Cache-Control: no-store');
if (empty($_COOKIE['ies_training'])) { http_response_code(401); exit; }
session_name('ies_training');
session_save_path(data_dir() . '/sesiones');
@session_start(['read_and_close' => true]);
$id = $_SESSION['uid'] ?? null;
if (!$id) { http_response_code(401); exit; }
$st = db()->prepare('SELECT active FROM users WHERE id=?'); $st->execute([$id]);
http_response_code($st->fetchColumn() ? 204 : 401);
