document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            alert('Please enter username and password.');
            return;
        }

        try {
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;

            // Show spinner
            submitBtn.innerHTML = '<div class="spinner" style="display: inline-block; width: 16px; height: 16px; border: 2px solid #f3f3f3; border-top: 2px solid #00ff88; border-radius: 50%; animation: spin 1s linear infinite; margin-right: 8px;"></div>Authenticating...';

            const response = await fetch('/api/admin/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Show success checkmark
                submitBtn.innerHTML = '<svg class="checkmark" style="display: inline-block; width: 16px; height: 16px; margin-right: 8px; animation: bounce 0.6s;" viewBox="0 0 24 24"><path fill="#00ff88" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>Success!';
                submitBtn.style.background = '#00ff88';
                submitBtn.style.color = '#000';

                setTimeout(() => {
                    window.location.href = 'admin_dashboard.html';
                }, 1000);
            } else {
                submitBtn.innerHTML = 'Login Failed';
                submitBtn.style.background = '#ff6b6b';
                setTimeout(() => {
                    submitBtn.innerHTML = 'Login';
                    submitBtn.style.background = '';
                }, 2000);
            }
        } catch (error) {
            submitBtn.innerHTML = 'Error';
            submitBtn.style.background = '#ff6b6b';
            setTimeout(() => {
                submitBtn.innerHTML = 'Error';
                submitBtn.style.background = '';
            }, 2000);
        } finally {
            submitBtn.disabled = false;
        }
    });
});