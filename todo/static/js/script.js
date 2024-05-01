
$(document).ready(function () {
    $('[id^="example-"]').each(function () {
        var taskId = $(this).data('task-id');
        $(this).calendar({
            onChange: function (date, text, mode) {
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

document.addEventListener("DOMContentLoaded", function () {
    var editIcons = document.querySelectorAll(".edit_task");

    editIcons.forEach(function (icon) {
        icon.addEventListener("click", function () {
            var task_id = icon.getAttribute("data-task-id");
            var title = document.getElementById("task_title_" + task_id);
            var save_button = document.getElementById("edit_task_save_button_" + task_id);

            var inputField = document.createElement("input");
            inputField.setAttribute("type", "text");
            inputField.setAttribute("value", title.textContent);
            inputField.setAttribute("name", "title");
            inputField.setAttribute("class", "ui small header");
            inputField.required = true;
            title.parentNode.replaceChild(inputField, title);


            save_button.style.display = "inline-block";


            inputField.focus();
        });
    });
});



document.addEventListener("DOMContentLoaded", function () {
    var editIcons = document.querySelectorAll(".edit_category");

    editIcons.forEach(function (icon) {
        icon.addEventListener("click", function () {
            var category_id = icon.getAttribute("data-category-id");
            var title = document.getElementById("category_name_" + category_id);
            var save_button = document.getElementById("edit_category_save_button_" + category_id);

            var inputField = document.createElement("input");
            inputField.setAttribute("type", "text");
            inputField.setAttribute("value", title.textContent);
            inputField.setAttribute("name", "title");
            inputField.setAttribute("class", "ui small header");
            inputField.required = true;
            title.parentNode.replaceChild(inputField, title);


            save_button.style.display = "inline-block";


            inputField.focus();
        });
    });
});


let isModalOpen = false;

// Обработчик события открытия модального окна
function openModal() {
    isModalOpen = true;
}

// Обработчик события закрытия модального окна
function closeModal() {
    isModalOpen = false;
}

// Проверка состояния модального окна перед обновлением страницы
window.addEventListener('beforeunload', function (event) {
    if (isModalOpen) {
        // Отмена события закрытия окна
        event.preventDefault();
        // Возвращение текста, который будет отображаться в диалоговом окне браузера
        event.returnValue = '';
    }
});


// Найти все заголовки задач и добавить обработчик клика
var taskHeaders = document.querySelectorAll('.open-modal');
taskHeaders.forEach(function (header) {
    header.addEventListener('click', function () {
        // Найти id задачи из data-атрибута
        var taskId = header.getAttribute('data-task-id');
        // Показать модальное окно для этой задачи
        var modal = document.getElementById('description-' + taskId);
        modal.style.display = "block";
        // Сохранить ID открытого модального окна в Local Storage
        localStorage.setItem('openModalId', taskId);
    });
});

// Проверить, было ли сохранено ID открытого модального окна в Local Storage
var openModalId = localStorage.getItem('openModalId');
if (openModalId) {
    // Показать сохраненное модальное окно
    var modal = document.getElementById('description-' + openModalId);
    if (modal) {
        modal.style.display = "block";
    }
}

// Закрыть модальное окно при клике вне его области
window.addEventListener('click', function (event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function (modal) {
        if (event.target == modal) {
            modal.style.display = "none";
            // Удалить ID открытого модального окна из Local Storage при закрытии модального окна
            localStorage.removeItem('openModalId');
        }
    });
});