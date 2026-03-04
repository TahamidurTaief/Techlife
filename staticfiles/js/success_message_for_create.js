document.body.addEventListener('htmx:afterOnLoad', function(evt) {
    const toasts = document.querySelectorAll('.toast-message');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 500);
        }, 3000); // 3 seconds
    });
});