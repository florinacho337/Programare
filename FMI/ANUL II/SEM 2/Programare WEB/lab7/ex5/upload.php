<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();

$target_dir = $_SERVER['DOCUMENT_ROOT'] . "/ex5/photos/" . $_SESSION['id'] . "/";

if (!is_dir($target_dir) || !is_writable($target_dir)) {
    $_SESSION['message'] = 'The directory is not valid';
    header("Location: userView.php");
    exit;
}

$target_file = $target_dir . basename($_FILES['image']['name']);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

if (isset($_POST['submit'])) {
    $check = getimagesize($_FILES['image']['tmp_name']);
    if ($check !== false) {
        $uploadOk = 1;
    } else {
        $_SESSION['message'] = 'Incorrect type';
        header("Location: userView.php");
        exit;
    }
}

if (file_exists($target_file)) {
    $_SESSION['message'] = 'Image already exists';
    header("Location: userView.php");
    exit;
}

if ($_FILES['image']['size'] > 300000) {
    $_SESSION['message'] = 'Image size too big';
    header("Location: userView.php");
    exit;
}

if ($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg") {
    $_SESSION['message'] = "Error! Image must be in one of these formats: JPG, JPEG, PNG.";
    header("Location: userView.php");
    exit;
}

if (move_uploaded_file($_FILES['image']['tmp_name'], $target_file)) {
    $_SESSION['message'] = "Image was successfully uploaded";
} else {
    $_SESSION['message'] = "Image cannot be saved in " . $target_file;
}

header("Location: userView.php");
exit;
?>
