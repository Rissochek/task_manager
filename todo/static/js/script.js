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

// Получаем все элементы с классом 'editIcon'
var editIcons = document.querySelectorAll('.editIcon');

// Проходимся по каждому элементу и навешиваем обработчик события
editIcons.forEach(function(icon) {
    icon.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение ссылки

        // Получаем форму, связанную с иконкой
        var editForm = icon.nextElementSibling;

        // Отображаем или скрываем форму в зависимости от её текущего состояния
        if (editForm.style.display === 'block') {
            editForm.style.display = 'none';
        } else {
            // Скрываем все открытые формы перед отображением текущей
            document.querySelectorAll('.editForm').forEach(function(form) {
                form.style.display = 'none';
            });
            editForm.style.display = 'block';
        }
    });
});

var editIcons = document.querySelectorAll('.editCategoryIcon');

// Проходимся по каждому элементу и навешиваем обработчик события
editIcons.forEach(function(icon) {
    icon.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем стандартное поведение ссылки

        // Получаем форму, связанную с иконкой
        var editForm = icon.nextElementSibling;

        // Отображаем или скрываем форму в зависимости от её текущего состояния
        if (editForm.style.display === 'block') {
            editForm.style.display = 'none';
        } else {
            // Скрываем все открытые формы перед отображением текущей
            document.querySelectorAll('.editCategoryForm').forEach(function(form) {
                form.style.display = 'none';
            });
            editForm.style.display = 'block';
        }
    });
});