let sortTables = document.querySelectorAll('.sortableTable');
sortTables.forEach(table => {
    const th = table.querySelectorAll('th');
    th.forEach((header, index) => {
        header.addEventListener('click', () => sortTable(header, index));
    });
});

function sortTable(header, columnIndex) {
    const table = header.closest('table');
    const rows = Array.from(table.querySelectorAll('tr'));
    const headerRow = rows.shift();

    rows.sort((a, b) => {
        const aValue = getValue(a.cells[columnIndex].textContent);
        const bValue = getValue(b.cells[columnIndex].textContent);

        if (typeof aValue === 'number' && typeof bValue === 'number') {
            return aValue - bValue;
        } else {
            return aValue.localeCompare(bValue);
        }
    });

    if (header.classList.contains('sorted-desc')) {
        rows.reverse();
        header.classList.remove('sorted-desc');
    } else {
        header.classList.add('sorted-desc');
    }

    table.appendChild(headerRow);
    rows.forEach(row => table.appendChild(row));
}

function getValue(cellValue) {
    const numberValue = parseFloat(cellValue);
    return isNaN(numberValue) ? cellValue : numberValue;
}