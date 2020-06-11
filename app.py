from distutils.log import Log

import psycopg2,sys
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_migrate import Migrate
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:kittu@localhost:5432/todo"
class Todo(db.Model):
   __tablename__ = 'todos'
   id =  db.Column(db.Integer,primary_key=True)
   description = db.Column(db.String,nullable=False)
   completed = db.Column(db.Boolean,nullable=True)
   def __repr__(self):
       return f'{self.id} and {self.description}'

@app.route('/')
def hello_world():
    print(Todo.query.all())
    return render_template('index.html',data = Todo.query.all())
@app.route('/todos/create/', methods = ['POST'])
def hello_worlds():
    body = {}
    try:
        value = request.get_json()['description']
        todo = Todo(description=value)
        db.session.add(todo)
        body['description'] = todo.description
        db.session.commit()
        return body
    except:
        db.session.rollback()
    finally:
        db.session.close()

@app.route('/todos/<todo_id>/sur/',methods=['POST'])
def hello(todo_id):
    value = request.get_json()['completed']
    todo = Todo.query.get(todo_id)
    todo.completed = value
    db.session.add(todo)
    db.session.commit()
    return  redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run()
