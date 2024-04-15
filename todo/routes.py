from datetime import datetime

from flask import Flask, request, render_template, url_for, redirect, jsonify
from sqlalchemy import func, desc

from todo.models import db, Tasks, Category


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


@app.get('/')
def home():
    task_list = Tasks.query.all()
    category_list = Category.query.all()
    return render_template('todo/index.html', task_list=task_list, title='Главная страница',
                           category_list=category_list)


@app.post('/sorting/<int:index>')
def sorting(index):
    sorting_value = request.form.get('param')
    if sorting_value == 'skip':
        return redirect(url_for('home'))
    if sorting_value == 'title':
        task_list = Tasks.query.order_by(sorting_value).all()
    else:
        task_list = Tasks.query.order_by(desc(sorting_value)).all()
    category_list = Category.query.filter_by(id=index).all()
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
        data = request.json  # Получаем данные из JSON тела запроса
        print("Received data:", data)  # Выводим данные для отладки
        calendar_date = data['date']
        task_id = data['taskId']
        # Преобразовать строку в объект datetime
        deadline_datetime = datetime.strptime(calendar_date, '%B %d, %Y %I:%M %p')

        task = Tasks.query.filter_by(id=task_id).first()
        task.deadline = deadline_datetime
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)  # Выводим ошибку для отладки
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
