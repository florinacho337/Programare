<?php
    header('Content-Type: application/json');

    $board = str_split($_POST['board']);

    $gameOver = checkGameOver($board);
    $winner = null;
    if ($gameOver) {
        $winner = checkWinner($board);
    } else {
        for ($i = 0; $i < count($board); $i++) {
            if ($board[$i] === ' ') {
                $board[$i] = $_POST['computerSymbol'];
                break;
            }
        }
        $gameOver = checkGameOver($board);
        if ($gameOver) {
            $winner = checkWinner($board);
        }
    }

    echo json_encode(array(
        'board' => implode('', $board),
        'gameOver' => $gameOver,
        'winner' => $winner
    ));

    function checkGameOver($board) {
        return !in_array(' ', $board) || checkWinner($board) !== null;
    }

    function checkWinner($board) {
        $wins = array(
            array(0, 1, 2),
            array(3, 4, 5),
            array(6, 7, 8),
            array(0, 3, 6),
            array(1, 4, 7),
            array(2, 5, 8),
            array(0, 4, 8),
            array(2, 4, 6)
        );

        foreach ($wins as $win) {
            if ($board[$win[0]] !== ' ' && $board[$win[0]] === $board[$win[1]] && $board[$win[0]] === $board[$win[2]]) {
                return $board[$win[0]];
            }
        }

        return null;
    }
?>