document.getElementById('submitForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    try {
        const response = await fetch('/api/submit_complaint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert('Complaint submitted successfully! ID: ' + result.complaint_id);
            window.location.href = '/track.html?id=' + result.complaint_id;
        } else {
            if (response.status === 401) {
                alert('Please login to submit a complaint');
                window.location.href = '/login.html';
            } else {
                alert(result.error || 'Submission failed');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});
