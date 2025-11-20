document.addEventListener('DOMContentLoaded', async function () {
    const navLinks = document.getElementById('navLinks');

    if (!navLinks) return;

    try {
        const response = await fetch('/api/user_complaints');

        if (response.ok) {
            // Logged in
            navLinks.innerHTML = `
                <a href="/" class="nav-link">Home</a>
                <a href="/submit.html" class="nav-link">Submit</a>
                <a href="/track.html" class="nav-link">Track</a>
                <a href="/my_complaints.html" class="nav-link">My Complaints</a>
                <a href="#" id="logoutBtn" class="nav-link btn-primary">Logout</a>
            `;

            document.getElementById('logoutBtn').addEventListener('click', async function (e) {
                e.preventDefault();
                await fetch('/api/logout', { method: 'POST' });
                window.location.href = '/';
            });
        } else {
            // Not logged in
            navLinks.innerHTML = `
                <a href="/" class="nav-link">Home</a>
                <a href="/login.html" class="nav-link">Login</a>
                <a href="/signup.html" class="nav-link btn-primary">Sign Up</a>
                <a href="/admin_login.html" class="nav-link admin-link">Admin</a>
            `;
        }
    } catch (error) {
        console.error('Auth check failed', error);
        // Default to not logged in
        navLinks.innerHTML = `
            <a href="/" class="nav-link">Home</a>
            <a href="/login.html" class="nav-link">Login</a>
            <a href="/signup.html" class="nav-link btn-primary">Sign Up</a>
            <a href="/admin_login.html" class="nav-link admin-link">Admin</a>
        `;
    }
});
