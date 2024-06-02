$(document).ready(function () {
    const errorMessages = {
        'text': 'Name',
        'date': 'Birthdate',
        'number': 'Age',
        'email': 'Email'
    };

    $('form').on('submit', function (e) {
        e.preventDefault();
        const errors = [];

        $(this).find('input').each(() => $(this).val() === '' || ($(this).attr('type') === 'number' && ($(this).val() < 0 || $(this).val() > 100))) ? errors.push(errorMessages[$(this).attr('type').css('border', '1px solid red')]): $(this).css('border', '1px solid black');
        errors.length > 0 ? alert("Campurile " + errors.join(', ') + " nu sunt completate corect!"): alert('Datele sunt completate corect');

    });
});