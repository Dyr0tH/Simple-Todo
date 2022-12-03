from datetime import datetime
from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# consider these following 4 lines as super mandatory ok
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SQLALCHEMY_BINDS'] = False

# This is another way to create a database

# meta=MetaData()
# userstable = Table('todo', meta, \
#     Column('task_id', Integer, primary_key = True, autoincrement=True), \
#     Column('task_name', String), \
#     Column('task_desc', String))
# meta.create_all(engine)


# defining a class to create a database.

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    task_desc = db.Column(db.String(200), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.utcnow)
    task_owner = db.Column(db.String(20), nullable=True)

    def __repr__(self) -> str:
        return f'{self.sno}, {self.task_name}\n'


@app.route('/', methods=['GET', 'POST'])
def page():

    if request.method == 'POST':
        print('method: post')
        task = request.form['todo_title']
        desc = request.form['description']
        owner = request.form['task_owner']

        data = todo(task_name=task, task_desc=desc, task_owner=owner)
        db.session.add(data)
        db.session.commit()

    todos = todo.query.all()

    cust_res = make_response(render_template('index.html', alltodo=todos))
    cust_res.headers['ngrok-skip-browser-warning'] = 0

    return cust_res

    # return render_template('index.html', alltodo=todos)


@app.route('/delete/<int:sno>')
def delete(sno):
    delete_task = todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_task)
    db.session.commit()

    return redirect(location="/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):

    if request.method == 'POST':
        update_task = todo.query.filter_by(sno=sno).first()
        update_task.task_name = request.form['update_todo_title']
        update_task.task_desc = request.form['update_todo_desc']
        db.session.commit()

        return redirect(location="/")

    update_task = todo.query.filter_by(sno=sno).first()

    return render_template('update.html', todo=update_task)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # this lines creates the database-file in the instance folder

    app.run(debug=True, host='0.0.0.0', port=8080)
