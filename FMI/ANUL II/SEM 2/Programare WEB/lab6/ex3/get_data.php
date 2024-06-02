<?php
    header('Content-Type: application/json');

    $conn = new mysqli("localhost", "root", "password", "users");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $key = $_GET['key'];

    $sql = "SELECT nume, prenume, telefon, email FROM users WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $key);
    $stmt->execute();
    $stmt->bind_result($nume, $prenume, $telefon, $email);
    $stmt->fetch();
    $stmt->close();

    $data = array(
        'nume' => $nume,
        'prenume' => $prenume,
        'telefon' => $telefon,
        'email' => $email
    );
    echo json_encode($data);
    $conn->close();
    exit;
?>