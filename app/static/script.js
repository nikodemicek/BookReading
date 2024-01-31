function submitFiles() {
    let fileInput = document.getElementById('fileElem');
    let formData = new FormData();

    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append('file' + i, fileInput.files[i]);
    }

    // Example AJAX request (You need to replace 'your-server-endpoint' with your actual server URL)
    fetch('your-server-endpoint', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data
        console.log(data);
        // Update the table-container with results
        // For example:
        // document.getElementById('table-container').innerHTML = '<table>...</table>';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
