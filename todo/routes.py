from datetime import datetime

from flask import Flask, request, render_template, url_for, redirect, jsonify
from sqlalchemy import func, desc

from todo.models import db, Tasks, Category


def create_app():
    app = Flask(__name__)
    app.secret_key = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


@app.get('/')
def home():
    task_list = list()
    category_list = Category.query.all()
    for category in category_list:
        if category.filtering != 'skip':
            temp_tasks = Tasks.query.filter_by(category_id=category.id, status=int(category.filtering)).all()
            task_list.extend(temp_tasks)
        else:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)
    db.session.commit()
    return render_template('todo/index.html', task_list=task_list, title='Главная страница',
                           category_list=category_list)


def delete_tasks():
    db.session.query(Tasks).delete()
    db.session.commit()


def write_tasks(task_list):
    for idx, task in enumerate(task_list, start=1):
        new_task = Tasks(id=idx, title=task.title, description=task.description, status=task.status,
                         deadline=task.deadline, priority=task.priority, category_id=task.category_id)
        db.session.add(new_task)
    db.session.commit()


@app.post('/sorting/<int:index>')
def sorting(index):
    sorting_value = request.form.get('param')
    category_list = Category.query.all()

    if sorting_value == 'skip':
        category = Category.query.filter_by(id=index).first()
        category.sorting = sorting_value
        db.session.commit()
        return redirect(url_for('home'))

    sorted_task_list = Tasks.query.filter_by(category_id=index).order_by(
        Tasks.title if sorting_value == 'title' else desc(sorting_value)).all()

    task_list = sorted_task_list

    for category in category_list:
        if category.id != index:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)

    delete_tasks()
    write_tasks(task_list)

    category = Category.query.filter_by(id=index).first()
    category.sorting = sorting_value
    db.session.commit()

    return redirect(url_for('home'))


@app.post('/filtering/<int:index>')
def filtering(index):
    filter_value = request.form.get('param')
    category_list = Category.query.all()

    if filter_value == 'skip':
        category = Category.query.filter_by(id=index).first()
        category.filtering = filter_value
        db.session.commit()
        return redirect(url_for('home'))

    filtered_task_list = Tasks.query.filter_by(category_id=index, status=int(filter_value)).all()
    task_list = filtered_task_list

    for category in category_list:
        if category.filtering != 'skip' and category.id != index:
            temp_tasks = Tasks.query.filter_by(category_id=category.id, status=int(category.filtering)).all()
            task_list.extend(temp_tasks)
        elif category.id != index:
            temp_tasks = Tasks.query.filter_by(category_id=category.id).all()
            task_list.extend(temp_tasks)

    category = Category.query.filter_by(id=index).first()
    category.filtering = filter_value
    db.session.commit()

    return render_template('todo/index.html', task_list=task_list, title='Главная страница',
                           category_list=category_list)


@app.post('/add_category')
def add_category():
    name = request.form.get('name')
    max_id = db.session.query(func.max(Category.id)).scalar()
    if max_id is not None:
        new_category = Category(name=name, id=max_id + 1)
    else:
        new_category = Category(name=name, id=1)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/add_task/<int:index>')
def add_task(index):
    title = request.form.get('title')
    new_task = Tasks(title=title, status=False, category_id=index)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/edit_task/<int:index>')
def edit_task(index):
    title = request.form.get('title')
    task = Tasks.query.filter_by(id=index).first()
    task.title = title
    db.session.commit()
    return redirect(url_for('home'))
@app.post('/edit_category/<int:index>')
def edit_category(index):
    title = request.form.get('title')
    category = Category.query.filter_by(id=index).first()
    category.name = title
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/update_description/<int:task_id>')
def update_description(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    description = request.form.get('description')
    task.description = description
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/update/<int:task_id>')
def update(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    task.status = not task.status
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.get('/delete_category/<int:category_id>')
def delete_category(category_id):
    for task in Tasks.query.filter_by(category_id=category_id).all():
        db.session.delete(task)
    category = Category.query.filter_by(id=category_id).first()
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('home'))


@app.post('/add_calendar')
def add_calendar():
    try:
        data = request.json
        print("Received data:", data)
        calendar_date = data['date']
        task_id = data['taskId']
        deadline_datetime = datetime.strptime(calendar_date, '%B %d, %Y %I:%M %p')

        task = Tasks.query.filter_by(id=task_id).first()
        task.deadline = deadline_datetime
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500


@app.post('/set_priority/<int:task_id>')
def set_priority(task_id):
    priority = int(request.form['value'])
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        task.priority = priority
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return 'Task not found', 404
