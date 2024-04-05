// Найти все заголовки задач и добавить обработчик клика
var taskHeaders = document.querySelectorAll('.open-modal');
taskHeaders.forEach(function(header) {
    header.addEventListener('click', function() {
        // Найти id задачи из data-атрибута
        var taskId = header.getAttribute('data-task-id');
        // Показать модальное окно для этой задачи
        var modal = document.getElementById('description-' + taskId);
        modal.style.display = "block";
    });
});

// Закрыть модальное окно при клике вне его области
window.addEventListener('click', function(event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});


