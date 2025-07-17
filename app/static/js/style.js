 const dropArea = document.getElementById('drop-area');
        const fileInput = document.getElementById('file-upload');
        const uploadIcon = document.getElementById('upload-icon');
        const uploadInstructions = document.getElementById('upload-instructions');
        const fileSizeInfo = document.getElementById('file-size-info');
        const fileDisplayArea = document.getElementById('file-display-area');
        const selectedFileNameSpan = document.getElementById('selected-file-name');
        const clearFileButton = document.getElementById('clear-file-button');

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropArea.classList.add('drag-over');
        }

        function unhighlight(e) {
            dropArea.classList.remove('drag-over');
        }

        dropArea.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                fileInput.files = files;
                updateFileDisplay(files[0]);
            }
        }

        fileInput.addEventListener('change', function(event) {
            updateFileDisplay(event.target.files[0]);
        });

        function updateFileDisplay(file) {
            if (file) {
                selectedFileNameSpan.textContent = file.name;
                fileDisplayArea.classList.remove('hidden');
                uploadIcon.classList.add('hidden');
                uploadInstructions.classList.add('hidden');
                fileSizeInfo.classList.add('hidden');
            } else {
                selectedFileNameSpan.textContent = '';
                fileDisplayArea.classList.add('hidden');
                uploadIcon.classList.remove('hidden');
                uploadInstructions.classList.remove('hidden');
                fileSizeInfo.classList.remove('hidden');
            }
        }

        clearFileButton.addEventListener('click', function() {
            fileInput.value = '';
            updateFileDisplay(null);
        });

        updateFileDisplay(fileInput.files[0]);