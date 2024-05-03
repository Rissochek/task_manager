# Miro: 
      https://miro.com/app/board/uXjVKcKL6jM=/?share_link_id=203327160856
      https://miro.com/app/board/uXjVKcKL6nE=/?share_link_id=471608715154
      https://miro.com/app/board/uXjVKcKLtu8=/?share_link_id=521561907189
# Trello: 
      https://trello.com/b/wpxqJ8Ux/task-manager
## Описание проекта:
Проект является программным приложением, разработанным для эффективного управления задачами с использованием нейронной сети GigaChat.

Было разработано Web-приложение с набором базовых функций: создание, редактирование заголовка, удаление задачи, фильтрация, сортировка задач, а также добавление описание и его редактирования.

Задачам можно присваивать приоритет, статус выполнено/не выполнено, выставлять дэдлайн. Дополнительно была возможность создавать категории для задач разного типа.  

Хранение данных приложения происходит при помощи базы данных SQLlite (работу с которой осуществляем при помощи sqlalchemy). 

Важной особенностью проекта является интеграция нейронной сети Gigachat, с помощью которой можно удобно в пару кликов сгенерировать описание к задаче.

Приложение обладает простым и понятным пользовательским интерфейсом, достаточно удобно в использовании, имеет необходимый функционал для эффективного распределения задач и отслеживания их выполнения.

## Инструкция:
Установка необходимых библиотек происходит при помощи библиотеки poetry, с помощью команды poetry install. Предварительно необходимо установить библиотеку poetry через pip.

Также после установки библиотек необходимо прописать в cmd 2 команды:

set FLASK_APP=app.py\
set FLASK_RUN_PORT=5555

После выполнения этих действий можно запускать приложение при помощи команд flask run или python app.py 
