let playerSymbol = 'X';
let computerSymbol = '0';

window.onload = function() {
    resetGame();
    const table = document.getElementById('tabel');
    table.onclick = event => {
        if (event.target.tagName === 'TD' && event.target.textContent === '') {
            event.target.textContent = playerSymbol;
            checkGameStatus();
        }
    };
};

function resetGame() {
    const table = document.getElementById('tabel');
    for (let i = 0; i < table.rows.length; i++) {
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            table.rows[i].cells[j].textContent = '';
        }
    }
    if (Math.random() < 0.5) {
        computerSymbol = 'X';
        playerSymbol = '0';
        checkGameStatus();
    } else {
        computerSymbol = '0';
        playerSymbol = 'X';
    }
}

function checkGameStatus() {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'server.php', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updateBoardState(response);
        }
    };
    xhr.send('board=' + encodeURIComponent(getBoardState()) + '&computerSymbol=' + encodeURIComponent(computerSymbol));
}

function updateBoardState(response) {
    const table = document.getElementById('tabel');
    const newBoardState = response.board;
    let index = 0;
    for (let i = 0; i < table.rows.length; i++) {
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            table.rows[i].cells[j].textContent = newBoardState[index] !== ' ' ? newBoardState[index] : '';
            index++;
        }
    }
    if (response.gameOver) {
        setTimeout(() => {
            if (response.winner === null)
                alert("Egalitate!")
            else
                alert(response.winner === playerSymbol ? playerSymbol + ' a castigat!' : computerSymbol + ' a castigat!');
            resetGame();
        }, 100);
    }
}

function getBoardState() {
    const table = document.getElementById('tabel');
    let board = '';
    for (let i = 0; i < table.rows.length; i++) {
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            board += table.rows[i].cells[j].textContent || ' ';
        }
    }
    return board;
}