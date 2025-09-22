document.addEventListener('DOMContentLoaded', function() {
    const trackBtn = document.getElementById('trackBtn');
    const editBtn = document.getElementById('editBtn');
    const complaintIdInput = document.getElementById('complaintIdInput');
    const resultDiv = document.getElementById('result');
    const resultSpans = {
        id: document.getElementById('resultId'),
        name: document.getElementById('resultName'),
        email: document.getElementById('resultEmail'),
        category: document.getElementById('resultCategory'),
        status: document.getElementById('resultStatus'),
        date: document.getElementById('resultDate'),
        text: document.getElementById('resultText')
    };
    const editCategory = document.getElementById('editCategory');
    const editText = document.getElementById('editText');

    let currentComplaint = null;

    trackBtn.addEventListener('click', async function() {
        const complaintId = complaintIdInput.value.trim();

        if (!complaintId) {
            alert('Please enter a Complaint ID.');
            return;
        }

        try {
            trackBtn.disabled = true;
            trackBtn.textContent = 'Tracking...';

            const response = await fetch(`/api/track_complaint?id=${complaintId}`);
            const result = await response.json();

            if (response.ok && result.complaint_id) {
                currentComplaint = result;
                // Populate results
                resultSpans.id.textContent = result.complaint_id;
                resultSpans.name.textContent = result.name;
                resultSpans.email.textContent = result.email;
                resultSpans.category.textContent = result.category;
                resultSpans.status.textContent = result.status;
                resultSpans.date.textContent = new Date(result.submitted_at).toLocaleString();
                resultSpans.text.textContent = result.complaint_text;

                // Set status class
                resultSpans.status.className = `status-${result.status.toLowerCase().replace(' ', '-')}`;

                // Show edit button if status is Pending
                if (result.status === 'Pending') {
                    editBtn.style.display = 'inline-block';
                } else {
                    editBtn.style.display = 'none';
                }

                // Hide edit fields
                resultSpans.category.style.display = 'inline';
                resultSpans.text.style.display = 'inline';
                editCategory.style.display = 'none';
                editText.style.display = 'none';
                editBtn.textContent = 'Edit Complaint';

                resultDiv.style.display = 'block';
                resultDiv.scrollIntoView({ behavior: 'smooth' });
            } else {
                alert(result.error || 'Complaint not found. Please check the ID and try again.');
            }
        } catch (error) {
            alert('Error tracking complaint: ' + error.message);
        } finally {
            trackBtn.disabled = false;
            trackBtn.textContent = 'Track Complaint';
        }
    });

    editBtn.addEventListener('click', async function() {
        if (editBtn.textContent === 'Edit Complaint') {
            // Enter edit mode
            resultSpans.category.style.display = 'none';
            resultSpans.text.style.display = 'none';
            editCategory.style.display = 'inline';
            editText.style.display = 'block';

            editCategory.value = currentComplaint.category;
            editText.value = currentComplaint.complaint_text;

            editBtn.textContent = 'Save Changes';
        } else {
            // Save changes
            const newCategory = editCategory.value;
            const newText = editText.value.trim();

            if (!newText) {
                alert('Please enter complaint text.');
                return;
            }

            try {
                editBtn.disabled = true;
                editBtn.textContent = 'Saving...';

                const response = await fetch('/api/edit_complaint', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        complaint_id: currentComplaint.complaint_id,
                        complaint_text: newText,
                        category: newCategory
                    })
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    alert('Complaint updated successfully!');
                    // Update display
                    currentComplaint.category = newCategory;
                    currentComplaint.complaint_text = newText;
                    resultSpans.category.textContent = newCategory;
                    resultSpans.text.textContent = newText;

                    // Exit edit mode
                    resultSpans.category.style.display = 'inline';
                    resultSpans.text.style.display = 'inline';
                    editCategory.style.display = 'none';
                    editText.style.display = 'none';
                    editBtn.textContent = 'Edit Complaint';
                } else {
                    alert(result.error || 'Failed to update complaint.');
                }
            } catch (error) {
                alert('Error updating complaint: ' + error.message);
            } finally {
                editBtn.disabled = false;
                editBtn.textContent = 'Save Changes';
            }
        }
    });
});