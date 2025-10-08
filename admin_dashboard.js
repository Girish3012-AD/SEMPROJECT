document.addEventListener('DOMContentLoaded', async function() {
    const logoutBtn = document.getElementById('logoutBtn');
    
    // Logout functionality
    logoutBtn.addEventListener('click', async function() {
        try {
            await fetch('/api/logout', {
                method: 'POST'
            });
        } catch (error) {
            console.log('Logout error:', error);
        }
        window.location.href = 'admin_login.html';
    });

    // Charts
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');
    let categoryChart, monthlyChart;

    // Fetch stats and complaints
    async function loadData() {
        try {
            // Check admin session
            const sessionCheck = await fetch('/api/admin/stats');
            if (sessionCheck.status === 401) {
                alert('Admin session expired. Please login again.');
                window.location.href = 'admin_login.html';
                return;
            }

            // Fetch stats
            const statsResponse = await fetch('/api/admin/stats');
            let stats;
            try {
                stats = await statsResponse.json();
            } catch (e) {
                throw new Error('Invalid response from server');
            }

            if (!statsResponse.ok) {
                alert(stats.error || 'Failed to load stats');
                return;
            }

            // Update stats cards
            document.getElementById('totalComplaints').textContent = stats.total;
            document.getElementById('pendingCount').textContent = stats.pending;
            document.getElementById('inProgressCount').textContent = stats.in_progress;
            document.getElementById('resolvedCount').textContent = stats.resolved;

            // Category chart (bar)
            const categories = Object.keys(stats.by_category);
            const categoryCounts = Object.values(stats.by_category);
            if (categoryChart) categoryChart.destroy();
            categoryChart = new Chart(categoryCtx, {
                type: 'bar',
                data: {
                    labels: categories,
                    datasets: [{
                        label: 'Complaints',
                        data: categoryCounts,
                        backgroundColor: ['#ffd700', '#00bfff', '#00ff88', '#ff6b6b'], // Colors for categories
                        borderColor: '#00ff88',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });

            // Monthly chart (line)
            const months = stats.monthly.map(item => item.month);
            const monthlyCounts = stats.monthly.map(item => item.count);
            if (monthlyChart) monthlyChart.destroy();
            monthlyChart = new Chart(monthlyCtx, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Complaints',
                        data: monthlyCounts,
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0, 255, 136, 0.2)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    }
                }
            });

            // Fetch complaints
            const complaintsResponse = await fetch('/api/admin/complaints');
            let complaints;
            try {
                complaints = await complaintsResponse.json();
            } catch (e) {
                throw new Error('Invalid response from server');
            }

            if (!complaintsResponse.ok) {
                alert(complaints.error || 'Failed to load complaints');
                return;
            }

            // Populate table
            const tbody = document.getElementById('complaintsTable');
            tbody.innerHTML = '';

            complaints.forEach(complaint => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${complaint.complaint_id}</td>
                    <td>${complaint.name}</td>
                    <td>${complaint.email}</td>
                    <td>${complaint.category}</td>
                    <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${complaint.complaint_text}</td>
                    <td>${new Date(complaint.submitted_at).toLocaleString()}</td>
                    <td>
                        <select class="status-select" data-id="${complaint.complaint_id}">
                            <option value="Pending" ${complaint.status === 'Pending' ? 'selected' : ''}>Pending</option>
                            <option value="In Progress" ${complaint.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                            <option value="Resolved" ${complaint.status === 'Resolved' ? 'selected' : ''}>Resolved</option>
                        </select>
                    </td>
                `;
                tbody.appendChild(row);
            });

            // Add event listeners to status selects
            document.querySelectorAll('.status-select').forEach(select => {
                select.addEventListener('change', async function() {
                    const complaintId = this.dataset.id;
                    const newStatus = this.value;

                    try {
                        const response = await fetch('/api/admin/complaints/update_status', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ complaint_id: complaintId, status: newStatus })
                        });

                        let result;
                        try {
                            result = await response.json();
                        } catch (e) {
                            throw new Error('Invalid response from server');
                        }

                        if (!response.ok) {
                            alert(result.error || 'Failed to update status');
                            // Revert select
                            this.value = complaint.status; // Assuming original status stored, but for simplicity, reload
                        } else {
                            alert('Status updated successfully!');
                            // Refresh data
                            loadData();
                        }
                    } catch (error) {
                        alert('Error updating status: ' + error.message);
                        this.value = complaint.status; // Revert
                    }
                });
            });

        } catch (error) {
            alert('Error loading dashboard data: ' + error.message);
        }
    }

    // Initial load
    loadData();
});