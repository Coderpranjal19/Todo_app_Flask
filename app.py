from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICTAIONS'] = False
db = SQLAlchemy(app)

#app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc =  db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self) -> str:
    #     return f"{self.sno} - {self.title}"
    

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        if not title or not desc:
            allTodo = Todo.query.all()
            return render_template('index.html', allTodo=allTodo, error="Both title and description are required.")
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/export_csv')
def export_csv():
    todos = Todo.query.all()

    todo_data = []
    for todo in todos:
        todo_data.append({
            'S.No': todo.sno,
            'Title': todo.title,
            'Description': todo.desc,
            'Date Created': todo.date_created.strftime('%Y-%m-%d %H:%M:%S')
        })

    df = pd.DataFrame(todo_data)
        # Save the DataFrame to an in-memory buffer
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # Send the CSV file to the user
    return send_file(output, download_name="todos.csv", as_attachment=True, mimetype='text/csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    