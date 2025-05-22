document.addEventListener('DOMContentLoaded', () => {
    // Управление вкладками
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = btn.getAttribute('data-tab');
            // Снять активность со всех кнопок и вкладок
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            // Активировать выбранные
            btn.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Управление модальным окном
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modal-message');
    const modalContent = document.querySelector('.modal-content');
    const closeModal = document.querySelector('.modal-close');

    window.showModal = function(type, text) {
        modalMessage.textContent = text;
        modalContent.className = 'modal-content ' + type;
        modal.style.display = 'block';
    };

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Закрытие модального окна при клике вне его
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Клиентская валидация форм
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', (e) => {
            const inputs = form.querySelectorAll('input[required], select[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value) {
                    valid = false;
                    input.classList.add('invalid');
                } else {
                    input.classList.remove('invalid');
                }
            });
            if (!valid) {
                e.preventDefault();
                showModal('error', 'Пожалуйста, заполните все обязательные поля.');
            } else if (!confirm('Подтвердить действие?')) {
                e.preventDefault();
            }
        });
    });
});