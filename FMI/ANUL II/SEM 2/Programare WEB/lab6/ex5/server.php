<?php

    header('Content-Type: application/json');

    $path = $_GET['path'] ?? '.';
    $file = $_GET['file'] ?? '';

    $root = realpath('.');

    function getDirectoryTree($dir) {
        $result = ['directories' => [], 'files' => []];
        $items = array_diff(scandir($dir), ['.', '..']);

        foreach ($items as $item) {
            $path = $dir . DIRECTORY_SEPARATOR . $item;
            if (is_dir($path)) {
                $result['directories'][] = $item;
            } else {
                $result['files'][] = $item;
            }
        }

        return $result;
    }

    $realPath = realpath($root . DIRECTORY_SEPARATOR . $path);
    if (!$realPath || strpos($realPath, $root) !== 0) {
        echo json_encode(['error' => 'Invalid path']);
        exit;
    }

    if ($file) {
        $realFilePath = realpath($realPath . DIRECTORY_SEPARATOR . $file);
        if ($realFilePath && strpos($realFilePath, $root) === 0 && is_file($realFilePath)) {
            echo json_encode(['content' => file_get_contents($realFilePath)]);
        } else {
            echo json_encode(['error' => 'Invalid file']);
        }
    } else {
        $directoryTree = getDirectoryTree($realPath);
        echo json_encode($directoryTree);
    }
?>
