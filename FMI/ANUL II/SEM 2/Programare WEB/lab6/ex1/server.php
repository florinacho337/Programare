<?php
    header('Content-Type: application/json');

    $conn = new mysqli("localhost", "root", "password", "trenuri");

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    if ($_SERVER['REQUEST_METHOD'] === 'GET'){
        if (isset($_GET['plecare'])) {
            $plecare = $_GET['plecare'];
            $sql = "SELECT sosire FROM trenuri WHERE plecare = '$plecare'";
            $result = $conn->query($sql);
            $destinatii = array();
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    array_push($destinatii, $row['sosire']);
                }
            }
            echo json_encode($destinatii);
            $conn->close();
            exit;
        } else {
            $sql = "SELECT DISTINCT plecare FROM trenuri";
            $result = $conn->query($sql);

            $plecari = array();
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    array_push($plecari, $row['plecare']);
                }
            }
            echo json_encode($plecari);
            $conn->close();
            exit;
        }
    }
?>