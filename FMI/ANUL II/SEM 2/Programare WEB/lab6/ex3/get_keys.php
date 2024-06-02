<?php
    header('Content-Type: application/json');

    $conn = new mysqli("localhost", "root", "password", "users");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT id FROM users";
    $result = $conn->query($sql);

    $users = array();

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            array_push($users, $row["id"]);
        }
    }

    echo json_encode($users);
    $conn->close();
    exit;
?>