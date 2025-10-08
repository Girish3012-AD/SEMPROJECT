document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('complaintForm');
    const modal = document.getElementById('successModal');
    const closeBtn = document.querySelector('.close');
    const complaintIdSpan = document.getElementById('complaintId');

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Validation
        const category = document.getElementById('category').value;
        const complaintText = document.getElementById('complaintText').value.trim();

        if (!category || !complaintText) {
            alert('Please fill in all required fields.');
            return;
        }

        // Get form data
        const formData = {
            complaint_text: complaintText,
            category: category
        };

        try {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';

            const response = await fetch('/api/submit_complaint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.status === 401) {
                alert('Please login to submit a complaint.');
                window.location.href = 'login.html';
                return;
            }

            let result;
            try {
                result = await response.json();
            } catch (e) {
                throw new Error('Invalid response from server');
            }

            if (response.ok && result.success) {
                complaintIdSpan.textContent = result.complaint_id;
                modal.style.display = 'block';
                form.reset();
            } else {
                alert(result.error || 'Failed to submit complaint. Please try again.');
            }
        } catch (error) {
            alert('Error submitting complaint: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Complaint';
        }
    });

    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});