$(document).ready(function() {
    $('#upload-form').submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        console.log("upload-form submitted!");
        $.ajax({
            type: 'POST',
            url: '/',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // Start polling for status
                console.log("job status checked!");
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
            console.log("job status: ", response.status);
            if (response.status === 'Processing') {
                document.getElementById('spinner').style.display = 'block';
                // Poll every 2 seconds
                setTimeout(function() { checkJobStatus(jobId); }, 2000);
            } else {
                // Show table container and populate data
                $('#table-container').show();
                // Hide spinner
                document.getElementById('spinner').style.display = 'none';
                populateTable(response);
            }
        },
        error: function() {
            $('#results').html('Error checking job status.');
        }
    });
}

function populateTable(data) {
    var table = $('#table-container table');
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