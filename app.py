from todo.routes import db, app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(port=app.config['PORT'])
