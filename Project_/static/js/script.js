// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        // Запобігаємо відправці форми, якщо вона не валідна
        if (!form.checkValidity()) {
            event.preventDefault();  // Не відправляємо форму

            // Додаємо клас для валідації після спроби відправки
            form.classList.add('was-validated');
        }
    });
});
