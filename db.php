<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Basic Authentication
if (!isset($_SERVER['PHP_AUTH_USER']) || $_SERVER['PHP_AUTH_USER'] !== 'user' || $_SERVER['PHP_AUTH_PW'] !== 'pass') {
    header('WWW-Authenticate: Basic realm="Family Calendar"');
    http_response_code(401);
    exit('Unauthorized');
}

$databasePath = './family_calendar.db';

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (file_exists($databasePath)) {
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="family_calendar.db"');
        readfile($databasePath);
    } else {
        http_response_code(404);
        echo 'Database not found';
    }
} elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        if (move_uploaded_file($_FILES['file']['tmp_name'], $databasePath)) {
            chmod($databasePath, 0664);
            echo 'Database saved successfully';
        } else {
            http_response_code(500);
            echo 'Error saving database';
        }
    } else {
        http_response_code(400);
        echo 'Error uploading database';
    }
}
?>