document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('category_select');
    const label = select.nextElementSibling; // Get the label element

    // 1. Initial check on load for select field
    if (select.value) {
        // Apply floating effect immediately if a default value exists
        label.style.transform = 'translateY(-36px) translateX(4px) scale(0.85)';
        label.style.color = '#60a5fa'; // Blue-400
        label.style.background = '#ffffff';
        label.style.padding = '0 8px';
    }

    // 2. Add event listener for user interaction (for select field)
    select.addEventListener('change', function() {
        // This is primarily handled by CSS selectors.
    });

    document.querySelectorAll('.input-wrapper input:not([type="file"]):not([placeholder]), .input-wrapper textarea').forEach((input) => {
        // For required fields without placeholders (Title/Description)
        if (input.value) {
            input.classList.add('valid');
        }
        input.addEventListener('blur', () => {
            if (input.value) {
                input.classList.add('valid');
            } else {
                input.classList.remove('valid');
            }
        });
    });

    // Simple form submission handler
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Form Submitted!');
        // You would typically send the data to a server here using fetch.
    });
});