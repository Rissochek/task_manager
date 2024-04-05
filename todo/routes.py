from flask import Flask, request, render_template, url_for, redirect
from todo.models import db, Tasks, Category
from sqlalchemy import func


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


@app.get('/delete/<int:task_id>')
def delete(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))
