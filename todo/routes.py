from datetime import datetime
from typing import List, Union

from flask import Flask, request, render_template, url_for, redirect, jsonify, Response, make_response
from sqlalchemy import func, desc

from todo.models import db, Tasks, Category
from todo.gigachat import get_chat_completion, giga_token


def create_app() -> Flask:
    """
    Создает экземпляр приложения Flask.

    Returns:
        Flask: Экземпляр приложения Flask.
    """
    task_manager = Flask(__name__)
    task_manager.secret_key = '12345'
    task_manager.config['PORT'] = 5555
    task_manager.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    task_manager.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(task_manager)
    return task_manager


app = create_app()


@app.route('/')
def home() -> str:
    """
    Отображает главную страницу приложения.

    Returns:
        str: HTML-страница с задачами и категориями.
    """
    task_list: List[Tasks] = []
    category_list: List[Category] = Category.query.all()
    for category in category_list:
        if category.filtering != 'skip' and isinstance(category.filtering, str):
            temp_tasks: List[Tasks] = Tasks.query.filter_by(category_id=category.id,
                                                            status=int(category.filtering)).all()
            task_list.extend(temp_tasks)
        else:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)
    db.session.commit()
    return render_template('todo/index.html', task_list=task_list, title='Главная страница',
                           category_list=category_list)


def delete_tasks() -> None:
    """
    Удаляет все задачи из базы данных.
    """
    db.session.query(Tasks).delete()
    db.session.commit()


def write_tasks(task_list: List[Tasks]) -> None:
    """
    Записывает задачи в базу данных.

    Args:
        task_list (List[Tasks]): Список задач для записи.
    """
    for idx, task in enumerate(task_list, start=1):
        new_task = Tasks(id=idx, title=task.title, description=task.description, status=task.status,
                         deadline=task.deadline, priority=task.priority, category_id=task.category_id)
        db.session.add(new_task)
    db.session.commit()


@app.route('/sorting/<int:index>', methods=['POST'])
def sorting(index: int) -> Union[str, 'Response']:
    """
    Сортирует задачи по заданному критерию и обновляет базу данных.

    Args:
        index (int): Идентификатор категории для сортировки.

    Returns:
        Union[str, Response]: Редирект на главную страницу.
    """
    sorting_value: str = request.form.get('param') or ''
    category_list: List[Category] = Category.query.all()

    if sorting_value == 'skip':
        category = Category.query.filter_by(id=index).first()
        category.sorting = sorting_value
        db.session.commit()
        return make_response(redirect(url_for('home')))

    sorted_task_list: List[Tasks] = Tasks.query.filter_by(category_id=index).order_by(
        Tasks.title if sorting_value == 'title' else desc(sorting_value)).all()

    task_list: List[Tasks] = sorted_task_list

    for category in category_list:
        if category.id != index:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)

    delete_tasks()
    write_tasks(task_list)

    category = Category.query.filter_by(id=index).first()
    category.sorting = sorting_value
    db.session.commit()

    return make_response(redirect(url_for('home')))


@app.route('/filtering/<int:index>', methods=['POST'])
def filtering(index: int) -> Union[str, 'Response']:
    """
    Фильтрует задачи по заданному критерию и обновляет главную страницу.

    Args:
        index (int): Идентификатор категории для фильтрации.

    Returns:
        Union[str, Response]: HTML-страница с отфильтрованными задачами или редирект на главную страницу.
    """
    filter_value: str = request.form.get('param') or ''
    category_list: List[Category] = Category.query.all()

    if filter_value == 'skip':
        category = Category.query.filter_by(id=index).first()
        category.filtering = filter_value
        db.session.commit()
        return make_response(redirect(url_for('home')))

    filtered_task_list: List[Tasks] = Tasks.query.filter_by(category_id=index, status=int(filter_value)).all()
    task_list: List[Tasks] = filtered_task_list

    for category in category_list:
        if category.filtering != 'skip' and category.id != index and isinstance(category.filtering, str):
            temp_tasks: List[Tasks] = Tasks.query.filter_by(category_id=category.id,
                                                            status=int(category.filtering)).all()
            task_list.extend(temp_tasks)
        elif category.id != index:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)

    category = Category.query.filter_by(id=index).first()
    category.filtering = filter_value
    db.session.commit()

    return make_response(render_template('todo/index.html', task_list=task_list, title='Главная страница',
                                         category_list=category_list))


@app.post('/add_category')
def add_category() -> 'Response':
    """
    Добавляет новую категорию.

    Returns:
        Response: Перенаправляет на главную страницу.
    """
    name: str = request.form.get('name') or ''
    max_id: int = db.session.query(func.max(Category.id)).scalar()
    if max_id is not None:
        new_category = Category(name=name, id=max_id + 1)
    else:
        new_category = Category(name=name, id=1)
    db.session.add(new_category)
    db.session.commit()
    return make_response(redirect(url_for('home')))


@app.post('/add_task/<int:index>')
def add_task(index: int):
    """
    Добавляет новую задачу в определенную категорию.

    Parameters:
        index (int): Индекс категории, в которую добавляется задача.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    title: str = request.form.get('title') or ''
    new_task = Tasks(title=title, status=False, category_id=index)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/edit_task/<int:index>')
def edit_task(index: int):
    """
    Редактирует задачу.

    Parameters:
        index (int): Индекс задачи для редактирования.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    title: str = request.form.get('title') or ''
    task = Tasks.query.filter_by(id=index).first()
    task.title = title
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/edit_category/<int:index>')
def edit_category(index: int):
    """
    Редактирует категорию.

    Parameters:
        index (int): Индекс категории для редактирования.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    title: str = request.form.get('title') or ''
    category = Category.query.filter_by(id=index).first()
    category.name = title
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/update_description/<int:task_id>')
def update_description(task_id: int) -> 'Response':
    """
    Обновляет описание задачи.

    Parameters:
        task_id (int): ID задачи для обновления.

    Returns:
        Response: Перенаправляет на главную страницу.
    """
    task = Tasks.query.filter_by(id=task_id).first()
    description: str = request.form.get('description') or ''
    if task:
        task.description = description
        db.session.commit()
        return make_response(redirect(url_for('home')))
    else:
        return make_response('Задача не найдена', 404)


@app.get('/update/<int:task_id>')
def update(task_id: int):
    """
    Обновляет статус задачи.

    Parameters:
        task_id (int): ID задачи для обновления.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    task = Tasks.query.filter_by(id=task_id).first()
    task.status = not task.status
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete_task/<int:task_id>')
def delete_task(task_id: int):
    """
    Удаляет задачу.

    Parameters:
        task_id (int): ID задачи для удаления.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    task = Tasks.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete_category/<int:category_id>')
def delete_category(category_id: int):
    """
    Удаляет категорию и все связанные с ней задачи.

    Parameters:
        category_id (int): ID категории для удаления.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    for task in Tasks.query.filter_by(category_id=category_id).all():
        db.session.delete(task)
    category = Category.query.filter_by(id=category_id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/add_calendar')
def add_calendar():
    """
    Добавляет срок выполнения задачи.

    Returns:
        Redirect: Перенаправляет на главную страницу.
    """
    try:
        data: dict = request.json
        print("Received data:", data)
        calendar_date: str = data['date']
        task_id: int = data['taskId']
        deadline_datetime: datetime = datetime.strptime(calendar_date, '%B %d, %Y %I:%M %p')

        task = Tasks.query.filter_by(id=task_id).first()
        task.deadline = deadline_datetime
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.post('/set_priority/<int:task_id>')
def set_priority(task_id: int) -> 'Response':
    """
    Устанавливает приоритет задачи.

    Parameters:
        task_id (int): ID задачи для установки приоритета.

    Returns:
        Response: Перенаправляет на главную страницу в случае успеха, в противном случае возвращает
        'Задача не найдена'.
    """
    priority: int = int(request.form['value'])
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        task.priority = priority
        db.session.commit()
        return make_response(redirect(url_for('home')))
    else:
        return make_response('Задача не найдена', 404)


@app.get('/generate_description/<int:task_id>')
def generate_description(task_id: int) -> 'Response':
    """
    Генерирует описание задачи с помощью модели искусственного интеллекта.

    Parameters:
        task_id (int): ID задачи для генерации описания.

    Returns:
        Response: Перенаправляет на главную страницу.
    """
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        description = get_chat_completion(giga_token,
                                          user_message=f'Напиши опиcание задачи по заголовку. Заголовок: {task.title}.'
                                                       f'Сделай предложение законченным, размером 50 слов.')
        description.json()
        task.description = description.json()['choices'][0]['message']['content']
        db.session.commit()
        return make_response(redirect(url_for('home')))
    else:
        return make_response('Задача не найдена', 404)
