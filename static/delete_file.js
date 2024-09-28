// delete_file.js
console.log("This is a test: Script is loading");

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed");

    // Use event delegation to capture click events from delete buttons
    document.getElementById('file-list').addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains('delete-file-btn')) {
            const deleteUrl = event.target.getAttribute('data-delete-url');
            console.log("Delete button clicked for file with URL:", deleteUrl);

            deleteFile(deleteUrl, event.target);
        }
    });

    function getCSRFToken() {
        return document.getElementById('csrf_token').value;
    }

    function deleteFile(deleteUrl, button) {
        console.log("deleteFile function called for URL:", deleteUrl);

        if (confirm('Are you sure you want to delete this file?')) {
            fetch(deleteUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken()  // Include CSRF token in the headers
                }
            })
            .then(response => {
                if (response.ok) {
                    console.log('File deleted successfully');
                    const messageDiv = document.getElementById('message');
                    messageDiv.style.display = 'block'; 
                    messageDiv.textContent = 'File deleted successfully!';
                    const fileItem = button.closest('li');
                    fileItem.remove();
                } else {
                    alert('Failed to delete file.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the file.');
            });
        }
    }
});
