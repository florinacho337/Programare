let currentPage = 1;

window.onload = function() {
    const previousButton = document.getElementById('previous');
    const nextButton = document.getElementById('next');

    fetchRecords();

    previousButton.onclick = function() {
        currentPage--;
        fetchRecords();
    };

    nextButton.onclick = function() {
        currentPage++;
        fetchRecords();
    };
};

function fetchRecords() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'server.php?page=' + currentPage, true);
    xhr.onload = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const data = JSON.parse(xhr.responseText);
            populateTable(data.users);
            updateButtons(data.users.length, data.hasNextPage);
        }
    };
    xhr.send();
}

function populateTable(records) {
    const table = document.getElementById('tabel');

    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    records.forEach(function(record) {
        const row = table.insertRow();
        row.insertCell().textContent = record.nume;
        row.insertCell().textContent = record.prenume;
        row.insertCell().textContent = record.telefon;
        row.insertCell().textContent = record.email;
    });
}

function updateButtons(recordCount, hasNextPage) {
    const previousButton = document.getElementById('previous');
    const nextButton = document.getElementById('next');

    previousButton.disabled = (currentPage === 1);
    nextButton.disabled = !hasNextPage;
}