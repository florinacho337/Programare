$(document).ready(function () {
    const size = 4, gameTable = $('#gameTable');
    let firstCard, secondCard, flippedCards;

    function initializeGame() {
        flippedCards = 0; firstCard = null; secondCard = null; gameTable.html('');
        const images = [], availableImages = Array.from({length: 25}, (_, i) => `image${i + 1}.png`);
        while (images.length < size * size / 2) images.push(availableImages.splice(Math.floor(Math.random() * availableImages.length), 1)[0]);
        const shuffledImages = images.concat(images).sort(() => Math.random() - 0.5);
        for (let i = 0; i < size; i++) {
            const row = $('<tr></tr>').appendTo(gameTable);
            for (let j = 0; j < size; j++)
                $('<td></td>').append($('<img alt="" src="">', {alt: 'Card', src: shuffledImages[i * size + j]})).on('click', () => revealCard($(this))).appendTo(row);
        }
    }

    function revealCard(card) {
        if (card.find('img').css('display') === 'block') return;
        card.find('img').css('display', 'block');
        if (!firstCard) firstCard = card;
        else if (firstCard !== card) {
            secondCard = card;
            setTimeout(function () {
                if (firstCard.find('img').attr('src') === secondCard.find('img').attr('src')) {
                    flippedCards += 2; firstCard.off('click'); secondCard.off('click'); firstCard = null; secondCard = null;
                    if (flippedCards === size * size) {alert('Congratulations! You won!'); initializeGame();}
                } else {firstCard.find('img').css('display', 'none'); secondCard.find('img').css('display', 'none'); firstCard = null; secondCard = null;}
            }, 100);
        }
    }

    initializeGame();
});