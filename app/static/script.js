// This function will be called when dragging over the drop area
function fileDragHover(e) {
    e.preventDefault();
    e.stopPropagation();
    var fileDrag = document.getElementById('file-drag');
    fileDrag.className = (e.type === 'dragover' ? 'hover' : 'file-drag');
}

// This function will be called when a file is dropped into the drop area
function fileSelectHandler(e) {
    fileDragHover(e); // Call the fileDragHover function
    
    // Get the files that were dropped
    var files = e.target.files || e.dataTransfer.files;

    // We need to send dropped files to Server
    uploadFiles(files);
}

// Function to upload files to the server
function uploadFiles(files) {
    var formData = new FormData();

    // Loop through each of the selected files.
    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        // Check the file type.
        if (!file.type.match('image.*')) {
            continue;
        }

        // Add the file to the request.
        formData.append('files[]', file, file.name);
    }

    // Set up the request.
    var xhr = new XMLHttpRequest();

    // Open the connection.
    xhr.open('POST', '/', true);

    // Set up a handler for when the task for the request is complete.
    xhr.onload = function () {
        if (xhr.status == 200) {
            alert('Upload complete!');
            // Refresh the page or display a success message
        } else {
            alert('An error occurred while uploading the file. Please try again.');
            // Display an error message
        }
    };

    // Send the data.
    xhr.send(formData);
}

// Initialize the drag and drop events
function Init() {
    var fileDrag = document.getElementById('file-drag');

    // file select
    fileDrag.addEventListener('dragover', fileDragHover, false);
    fileDrag.addEventListener('dragleave', fileDragHover, false);
    fileDrag.addEventListener('drop', fileSelectHandler, false);
}

// Call the initialization function when the window is fully loaded
window.addEventListener('load', Init, false);
