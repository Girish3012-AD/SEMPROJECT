document.addEventListener('DOMContentLoaded', function () {
    loadStats();
    loadComplaints();
});

async function loadStats() {
    try {
        const response = await fetch('/api/admin/stats');
        if (response.ok) {
            const data = await response.json();
            document.getElementById('totalComplaints').textContent = data.total;
            document.getElementById('pendingComplaints').textContent = data.pending;
            document.getElementById('resolvedComplaints').textContent = data.resolved;

            // Render Chart
            const ctx = document.getElementById('statusChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Pending', 'In Progress', 'Resolved'],
                    datasets: [{
                        data: [data.pending, data.in_progress, data.resolved],
                        backgroundColor: ['#f59e0b', '#0ea5e9', '#22c55e'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadComplaints() {
    try {
        const response = await fetch('/api/admin/complaints');
        if (response.ok) {
            const complaints = await response.json();
            const tbody = document.querySelector('#adminComplaintsTable tbody');
            tbody.innerHTML = '';

            complaints.forEach(complaint => {
                const tr = document.createElement('tr');

                let statusClass = '';
                if (complaint.status === 'Pending') statusClass = 'status-pending';
                else if (complaint.status === 'In Progress') statusClass = 'status-in-progress';
                else if (complaint.status === 'Resolved') statusClass = 'status-resolved';

                tr.innerHTML = `
                    <td>#${complaint.complaint_id}</td>
                    <td>
                        <div>${complaint.name}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">${complaint.email}</div>
                    </td>
                    <td>${complaint.category}</td>
                    <td><span class="status-badge ${statusClass}">${complaint.status}</span></td>
                    <td>${new Date(complaint.submitted_at).toLocaleDateString()}</td>
                    <td>
                        ${complaint.status !== 'Resolved' ?
                        `<button onclick="openStatusModal(${complaint.complaint_id}, '${complaint.status}')" class="btn btn-secondary" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">Update</button>`
                        : '<span style="color: var(--text-muted); font-size: 0.85rem;">Completed</span>'}
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } else if (response.status === 401) {
            window.location.href = '/admin_login.html';
        }
    } catch (error) {
        console.error('Error loading complaints:', error);
    }
}

// Modal Logic
const modal = document.getElementById('statusModal');
const closeBtn = document.querySelector('.close');

closeBtn.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

window.openStatusModal = function (id, currentStatus) {
    document.getElementById('update_complaint_id').value = id;
    document.getElementById('current_status_display').textContent = currentStatus;

    const select = document.getElementById('new_status');
    select.innerHTML = '';

    if (currentStatus === 'Pending') {
        select.innerHTML = `
            <option value="In Progress">In Progress</option>
            <option value="Resolved">Resolved</option>
        `;
    } else if (currentStatus === 'In Progress') {
        select.innerHTML = `
            <option value="Resolved">Resolved</option>
        `;
    }

    modal.style.display = "block";
}

document.getElementById('statusForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const id = document.getElementById('update_complaint_id').value;
    const status = document.getElementById('new_status').value;

    try {
        const response = await fetch('/api/admin/complaints/update_status', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                complaint_id: id,
                status: status
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert('Status updated successfully');
            modal.style.display = "none";
            loadStats();
            loadComplaints();
        } else {
            alert(result.error || 'Update failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred');
    }
});
