   document.addEventListener('DOMContentLoaded', function() {
        const loginForm = document.getElementById('login-form');

        // Xử lý sự kiện đăng nhập
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            window.location.href = 'index.html';
            alert('Đăng nhập thành công! Sẽ chuyển hướng đến trang triển khai.');
        });
    });