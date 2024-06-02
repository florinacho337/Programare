<?php
$servername = "localhost";
$username = "root";
$password = "password";
$dbname = "produse";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Conexiunea a esuat: " . $conn->connect_error);
}

if (isset($_GET['noProducts'])) {
    $number = intval($_GET['noProducts']);
} else {
    $number = 10;
}

if (isset($_GET['page'])) {
    $page = intval($_GET['page']);
} else {
    $page = 1;
}

$offset = ($page - 1) * $number;

// Interogare pentru numărul total de produse
$totalResult = $conn->query("SELECT COUNT(*) AS total FROM produse");
$totalRow = $totalResult->fetch_assoc();
$total = $totalRow['total'];

$sql = "SELECT * FROM produse LIMIT $number OFFSET $offset";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo "<table>";
    echo "<tr><th>Nume</th><th>Descriere</th><th>Pret</th><";

    while ($row = $result->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . $row['nume'] . "</td>";
        echo "<td>" . $row['descriere'] . "</td>";
        echo "<td>" . $row['pret'] . "</td>";
        echo "</tr>";
    }

    echo "</table>";

    echo "<div>";

    if ($page > 1) {
        $previousPage = $page - 1;
        echo "<button><a href='fetch_products.php?noProducts=$number&page=$previousPage'>Previous page</a></button>";
    }

    // Verificare pentru paginile următoare
    if (($page * $number) < $total) {
        $nextPage = $page + 1;
        echo "<button><a href='fetch_products.php?noProducts=$number&page=$nextPage'>Next page</a></button>";
    }

    echo "</div>";
} else {
    echo "There is no data to fetch";
}

$conn->close();
?>
