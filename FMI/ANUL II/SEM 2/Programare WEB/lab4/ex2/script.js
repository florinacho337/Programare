const form = document.querySelector('form');
const inputs = form.querySelectorAll('input');
const errors = [];

form.addEventListener('submit', (e) => {
    e.preventDefault();
    inputs.forEach(input => {
        if (input.type === 'text' && input.value === '') {
            errors.push('Name');
        }
        if (input.type === 'date' && input.value === '') {
            errors.push('Birthdate');
        }
        if (input.type === 'number' && input.value === '' || input.value < 0 || input.value > 100) {
            errors.push('Age');
        }
        if (input.type === 'email' && input.value === '') {
            errors.push('Email');
        }
    });

    if (errors.length > 0) {
        if (errors.length === 1) {
            alert("Campul " + errors[0] + " nu este completat corect!");
        } else {
            alert("Campurile " + errors.join(', ') + " nu sunt completate corect!");
        }
        errors.length = 0;

        inputs.forEach(input => {
            if (input.type === 'submit') {
                return;
            }
            input.style.border = '1px solid red';
        });
    } else {
        alert('Datele sunt completate corect');
    }
});