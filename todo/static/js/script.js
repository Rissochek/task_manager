// Найти все заголовки задач и добавить обработчик клика
var taskHeaders = document.querySelectorAll('.open-modal');
taskHeaders.forEach(function (header) {
    header.addEventListener('click', function () {
        // Найти id задачи из data-атрибута
        var taskId = header.getAttribute('data-task-id');
        // Показать модальное окно для этой задачи
        var modal = document.getElementById('description-' + taskId);
        modal.style.display = "block";
    });
});

// Закрыть модальное окно при клике вне его области
window.addEventListener('click', function (event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function (modal) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});

$(document).ready(function(){
    $('[id^="example-"]').each(function() {
        var taskId = $(this).data('task-id');
        $(this).calendar({
            onChange: function(date, text, mode) {
               $.ajax({
                    type: "POST",
                    url: "/add_calendar",
                    contentType: "application/json",
                    data: JSON.stringify({ taskId: taskId, date: text }),
                });
            }
        });
    });
});
$('.ui.dropdown').dropdown();

    document.getElementById('editIcon').addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение ссылки

        // Отображаем форму для ввода
        document.getElementById('editForm').style.display = 'block';

        // Если нужно, можно добавить дополнительный код для загрузки данных или другой логики
    });
