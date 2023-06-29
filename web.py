import os

from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from pyservicebinding import binding

try:
    sb = binding.ServiceBinding()
    bindings_list = sb.bindings("postgresql")
    if len(bindings_list) < 1:
        print("expected to find a binding with postgresql type")
        os._exit(1)
    binding = bindings_list[0]
    db_uri = 'postgresql://%s:%s@%s/%s' % (binding['username'], binding['password'], binding['host'], binding['database'])
except binding.ServiceBindingRootMissingError as msg:
    print("SERVICE_BINDING_ROOT env var not set")
    os._exit(1)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print('connected to DB host %s' % (binding['host']))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

@app.route('/')
def index():
    db.create_all()
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        student = Student(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:student_id>/edit/', methods=('GET', 'POST'))
def edit(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/<int:student_id>/')
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)
