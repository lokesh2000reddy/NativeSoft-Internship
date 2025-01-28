from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the To-Do model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Home route
@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_task = Todo(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Mark task as complete
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    task = Todo.query.get(todo_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    task = Todo.query.get(todo_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
