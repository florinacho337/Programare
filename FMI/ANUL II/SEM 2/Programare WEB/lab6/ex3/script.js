window.onload = function() {
    const key_list = document.getElementById("keyList");
    const form = document.getElementById("dataForm");
    const saveButton = document.getElementById("saveButton");
    let currentKey = null;
    let isFormChanged = false;
    fetch("get_keys.php")
        .then(response => response.json())
        .then(data => {
            data.forEach(key => {
                const option = document.createElement("option");
                option.text = key;
                key_list.add(option);
            });
        })
        .catch(error => console.error(error));
    key_list.addEventListener("change", function() {
        if (isFormChanged) {
            if (confirm("You have unsaved changes. Do you want to save them before switching?")) {
                saveFormData(currentKey);
            }
        }
        loadFormData(this.value);
    });

    form.addEventListener("input", function() {
        isFormChanged = true;
        saveButton.disabled = false;
    });

    saveButton.addEventListener("click", function() {
        saveFormData(currentKey);
    });

    function loadFormData(key) {
        currentKey = key;
        fetch(`get_data.php?key=${key}`)
            .then(response => response.json())
            .then(data => {
                form.elements["nume"].value = data.nume;
                form.elements["prenume"].value = data.prenume;
                form.elements["telefon"].value = data.telefon;
                form.elements["email"].value = data.email;
                isFormChanged = false;
                saveButton.disabled = true;
            })
            .catch(error => console.error(error));
    }

    function saveFormData(key) {
        const data = {
            nume: form.elements["nume"].value,
            prenume: form.elements["prenume"].value,
            telefon: form.elements["telefon"].value,
            email: form.elements["email"].value,
            key: key
        };

        fetch("save_data.php", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(response => response.text())
            .then(result => {
                alert(result);
                isFormChanged = false;
                saveButton.disabled = true;
            })
            .catch(error => console.error(error));
    }
}

