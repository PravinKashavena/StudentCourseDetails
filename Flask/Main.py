from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/pythondb1'
db = SQLAlchemy(app)


# Define the model for student registration
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    institute = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)


# Home route
@app.route("/")
def getHome():
    return render_template('home.html')


# Form submission route
@app.route('/register', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        institute = request.form['institute']
        course = request.form['course']

        new_student = Student(name=name, email=email, institute=institute, course=course)
        db.session.add(new_student)
        db.session.commit()

        return render_template('home.html')
    return render_template('register.html')


# API endpoint to get student registrations
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [{'id': student.id, 'name': student.name, 'email': student.email,
               'institute': student.institute, 'course': student.course}
              for student in students]
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
