<?php
	header('Content-Type: application/json');

    $conn = new mysqli("localhost", "root", "password", "users");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

	$page = $_GET['page'];
	$offset = ($page - 1) * 3;
	$sql = "SELECT * FROM users LIMIT 3 OFFSET $offset";
	$result = $conn->query($sql);

    $users = array();
    while($row = $result->fetch_assoc()) {
        array_push($users, $row);
    }

    $sql1 = "SELECT COUNT(*) as count FROM users";
    $result1 = $conn->query($sql1);
    $count = $result1->fetch_assoc()['count'];

    $hasNextPage = $count > $page * 3;

    echo json_encode(array(
        'users' => $users,
        'hasNextPage' => $hasNextPage
    ));

    $conn->close();
    exit;
?>