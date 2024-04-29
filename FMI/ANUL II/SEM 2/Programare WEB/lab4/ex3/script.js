const size = 4; // Change this to increase/decrease grid size
let firstCard;
let secondCard;
let flippedCards;

const gameTable = document.getElementById('gameTable');

function initializeGame() {
    flippedCards = 0;
    firstCard = null;
    secondCard = null;
    gameTable.innerHTML = '';

    // const numbers = Array.from({length: (size * size) / 2}, (_, i) => i + 1);
    // const cardValues = [...numbers, ...numbers].sort(() => Math.random() - 0.5);

    const availableImages = [
        'image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png',
        'image6.png', 'image7.png', 'image8.png', 'image9.png', 'image10.png',
        'image11.png', 'image12.png', 'image13.png', 'image14.png', 'image15.png',
        'image16.png', 'image17.png', 'image18.png', 'image19.png', 'image20.png',
        'image21.png', 'image22.png', 'image23.png', 'image24.png', 'image25.png'
    ];


    const images = [];
    while (images.length < size*size / 2) {
        const randomIndex = Math.floor(Math.random() * availableImages.length);
        const randomImage = availableImages[randomIndex];
        if (!images.includes(randomImage)) {
            images.push(randomImage);
        }
    }
    
    const shuffledImages = images.concat(images).sort(() => Math.random() - 0.5);

    for (let i = 0; i < size; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < size; j++) {
            const cell = document.createElement('td');
            const image = document.createElement('img');
            // cell.dataset.value = cardValues[i * size + j];
            image.src = shuffledImages[i * size + j];
            image.alt = 'Card';
            cell.appendChild(image);
            cell.addEventListener('click', () => revealCard(cell));
            row.appendChild(cell);
        }
        gameTable.appendChild(row);
    }
}

initializeGame();

function revealCard(card) {
    // if (card.innerHTML) return;
    if (card.querySelector('img').style.display === 'block') return;
    // card.innerHTML = card.dataset.value;
    card.querySelector('img').style.display = 'block';
    if (!firstCard) {
        firstCard = card;
    } else {
        secondCard = card;
        // if (firstCard.dataset.value === secondCard.dataset.value) {
        if (firstCard.querySelector('img').src === secondCard.querySelector('img').src) {
            flippedCards += 2;
            firstCard = null;
            secondCard = null;
            if (flippedCards === size * size) {
                setTimeout(() => {
                    alert('Congratulations! You won!');
                    initializeGame();
                }, 500);
            }
        } else {
            setTimeout(() => {
                // firstCard.innerHTML = '';
                // secondCard.innerHTML = '';
                firstCard.querySelector('img').style.display = 'none';
                secondCard.querySelector('img').style.display = 'none';
                firstCard = null;
                secondCard = null;
            }, 1000);
        }
    }
}