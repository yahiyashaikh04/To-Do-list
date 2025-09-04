from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    students = Student.query.order_by(Student.date_created.desc()).all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']

    if name and age:
        new_student = Student(name=name, age=int(age))
        db.session.add(new_student)
        db.session.commit()

    return redirect('/')

# Update route
@app.route('/update<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = int(request.form['age'])
        db.session.commit()
        return redirect('/')

    return render_template('update.html', student=student)


@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
            db.create_all()
    app.run(debug=True)
