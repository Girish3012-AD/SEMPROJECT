document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    if (id) {
        document.getElementById('complaint_id').value = id;
        trackComplaint(id);
    }
});

document.getElementById('trackForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const id = document.getElementById('complaint_id').value;
    trackComplaint(id);
});

async function trackComplaint(id) {
    const resultDiv = document.getElementById('result');
    const btn = document.querySelector('button[type="submit"]');

    btn.disabled = true;
    btn.textContent = 'Tracking...';

    try {
        const response = await fetch(`/api/track_complaint?id=${id}`);
        const data = await response.json();

        if (response.ok) {
            let statusClass = '';
            if (data.status === 'Pending') statusClass = 'status-pending';
            else if (data.status === 'In Progress') statusClass = 'status-in-progress';
            else if (data.status === 'Resolved') statusClass = 'status-resolved';

            resultDiv.innerHTML = `
                <div style="text-align: left;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="margin: 0;">Complaint #${data.complaint_id}</h3>
                        <span class="status-badge ${statusClass}">${data.status}</span>
                    </div>
                    <p><strong>Category:</strong> ${data.category}</p>
                    <p><strong>Date:</strong> ${new Date(data.submitted_at).toLocaleDateString()}</p>
                    <p><strong>Description:</strong></p>
                    <p style="background: var(--background); padding: 1rem; border-radius: 0.5rem; margin-top: 0.5rem;">${data.complaint_text}</p>
                </div>
            `;
            resultDiv.style.display = 'block';
        } else {
            if (response.status === 401) {
                alert('Please login to track complaints');
                window.location.href = '/login.html';
            } else {
                resultDiv.innerHTML = `<p style="color: var(--danger); text-align: center;">${data.error || 'Complaint not found'}</p>`;
                resultDiv.style.display = 'block';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `<p style="color: var(--danger); text-align: center;">An error occurred</p>`;
        resultDiv.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Track Status';
    }
}
