document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const queryForm = document.getElementById('query-form');
    const uploadResponse = document.getElementById('upload-response');
    const queryResponse = document.getElementById('query-response');

    // Handle upload form submission
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            uploadResponse.innerText = JSON.stringify(result, null, 2);
        } catch (error) {
            console.error('Error:', error);
            uploadResponse.innerText = 'Error uploading document.';
        }
    });

    // Handle query form submission
    queryForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(queryForm);

        try {
            const response = await fetch('/query', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            queryResponse.innerText = JSON.stringify(result, null, 2);
        } catch (error) {
            console.error('Error:', error);
            queryResponse.innerText = 'Error querying document.';
        }
    });
});
