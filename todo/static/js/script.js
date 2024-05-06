// calendar
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

// edit task
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

// edit category
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

// modal window
let isModalOpen = false;

function openModal() {
    isModalOpen = true;
}

function closeModal() {
    isModalOpen = false;
}

window.addEventListener('beforeunload', function (event) {
    if (isModalOpen) {
        event.preventDefault();
        event.returnValue = '';
    }
});


var taskHeaders = document.querySelectorAll('.open-modal');
taskHeaders.forEach(function (header) {
    header.addEventListener('click', function () {
        var taskId = header.getAttribute('data-task-id');
        var modal = document.getElementById('description-' + taskId);
        modal.style.display = "block";
        localStorage.setItem('openModalId', taskId);
    });
});

var openModalId = localStorage.getItem('openModalId');
if (openModalId) {
    var modal = document.getElementById('description-' + openModalId);
    if (modal) {
        modal.style.display = "block";
    }
}

window.addEventListener('click', function (event) {
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function (modal) {
        if (event.target == modal) {
            modal.style.display = "none";
            localStorage.removeItem('openModalId');
        }
    });
});
