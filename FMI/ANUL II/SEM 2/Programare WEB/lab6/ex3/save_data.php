<?php
header('Content-Type: application/json');

$data = json_decode(file_get_contents('php://input'), true);

$mysqli = new mysqli('localhost', 'root', 'password', 'users');

if ($mysqli->connect_error) {
    die("Connection failed: " . $mysqli->connect_error);
}

$key = $data['key'];
$nume = $data['nume'];
$prenume = $data['prenume'];
$telefon = $data['telefon'];
$email = $data['email'];

$query = $mysqli->prepare("UPDATE users SET nume = ?, prenume = ?, telefon = ?, email = ? WHERE id = ?");
$query->bind_param("ssssi", $nume, $prenume, $telefon, $email, $key);

if ($query->execute()) {
    echo "Data saved successfully!";
} else {
    echo "Error: " . $query->error;
}

$query->close();
exit;
?>