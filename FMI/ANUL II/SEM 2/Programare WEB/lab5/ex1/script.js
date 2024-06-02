$(document).ready(function () {
    const selects = $('select');
    selects.each((i, select) => $(select).on('dblclick', () => {
            selects.eq((i + 1) % selects.length).append($(select).find(':selected'));
        }));
});