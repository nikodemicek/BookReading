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

$(document).ready(function() {
    $('#upload-form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            type: 'POST',
            url: '/',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Start polling for status
                checkJobStatus(response.job_id);
            },
            error: function() {
                $('#results').html('Error submitting file.');
            }
        });
    });
});

function checkJobStatus(jobId) {
    $.ajax({
        type: 'GET',
        url: '/results/' + jobId,
        success: function(response) {
            if (response.status === 'Processing') {
                // Poll every 2 seconds
                setTimeout(function() { checkJobStatus(jobId); }, 2000);
            } else {
                // Show table container and populate data
                $('#table_container').show();
                populateTable(response);
            }
        },
        error: function() {
            $('#results').html('Error checking job status.');
        }
    });
}

function populateTable(data) {
    var table = $('#table_container table');
    table.html(''); // Clear existing table data

    // Add table headers
    var headers = '<tr><th>Thumbnail</th><th>Title</th><th>Author</th><th>Description</th><th>Avg Rating</th><th>Ratings count</th></tr>';
    table.append(headers);

    // Add rows
    data.forEach(function(item) {
        var row = '<tr>' +
            '<td><img src="' + item.thumbnail + '" alt="Book Cover"></td>' +
            '<td><b>' + item.title + '</b></td>' +
            '<td>' + item.author + '</td>' +
            '<td>' + item.description + '</td>' +
            '<td>' + item.rating + '</td>' +
            '<td>' + item.rating_count + '</td>' +
            '</tr>';
        table.append(row);
    });
}
