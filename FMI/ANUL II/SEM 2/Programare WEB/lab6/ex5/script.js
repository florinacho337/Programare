function loadDirectoryContent(path, element) {
    fetch('server.php?path=' + encodeURIComponent(path))
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            let list = element.querySelector('ul');
            if (list) {
                element.removeChild(list);
            } else {
                list = document.createElement('ul');
                data.directories.forEach(directory => {
                    const newPath = path === '.' ? directory : path + '/' + directory;
                    const li = document.createElement('li');
                    li.textContent = directory;
                    li.style.cursor = 'pointer';
                    li.addEventListener('click', function (event) {
                        event.stopPropagation();
                        loadDirectoryContent(newPath, li);
                    });
                    list.appendChild(li);
                });

                data.files.forEach(file => {
                    const li = document.createElement('li');
                    li.textContent = file;
                    li.style.cursor = 'pointer';
                    li.addEventListener('click', function (event) {
                        event.stopPropagation();
                        // Clear any previous file content
                        const existingContent = element.querySelector('.file-content');
                        if (existingContent) {
                            existingContent.remove();
                        }
                        loadFileContent(path + '/' + file, element);
                    });
                    list.appendChild(li);
                });

                element.appendChild(list);
            }
        })
        .catch(error => console.error(error));
}

function loadFileContent(filePath, element) {
    fetch('server.php?file=' + encodeURIComponent(filePath))
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }

            const contentDiv = document.createElement('div');
            contentDiv.classList.add('file-content');
            contentDiv.textContent = data.content;
            element.appendChild(contentDiv);
        })
        .catch(error => console.error(error));
}

loadDirectoryContent('.', document.body);