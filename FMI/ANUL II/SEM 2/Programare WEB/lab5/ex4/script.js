$(document).ready(function() {
    $('.sortableTable th').on('click', function() {
        const rows = $(this).closest('table').find('tr:gt(0)').toArray().sort((a, b) => $.isNumeric($(a).children().eq($(this).index()).text()) ? $(a).children().eq($(this).index()).text() - $(b).children().eq($(this).index()).text() : $(a).children().eq($(this).index()).text().localeCompare($(b).children().eq($(this).index()).text()))
        if ($(this).toggleClass('sorted-desc').hasClass('sorted-desc')) rows.reverse();
        $(this).closest('table').append(rows);
    });
});