window.onload = function() {
    const plecare = document.getElementById("plecare");
    const sosire = document.getElementById("sosire");

    ajaxRequest('GET', 'server.php', function(response) {
        const values = JSON.parse(response);
        populateSelect(plecare, values);
    });

    plecare.onchange = function() {
        ajaxRequest('GET', 'server.php?plecare=' + plecare.value, function(response) {
            const values = JSON.parse(response);
            populateSelect(sosire, values);
        });
    }
}

function ajaxRequest(method, url, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(xhr.responseText);
        }
    };
    xhr.send();

}

function populateSelect(select, values) {
    while (select.firstChild) {
        select.removeChild(select.firstChild);
    }

    values.forEach(value => {
        const option = document.createElement("option");
        option.value = value;
        option.text = value;
        select.appendChild(option);
    });
}