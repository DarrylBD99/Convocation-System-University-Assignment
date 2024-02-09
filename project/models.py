from sqlalchemy import null
from extentions import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True, nullable = False, unique=True)
    name = db.Column(db.String(255), nullable = False, unique=True)
    email = db.Column(db.String(255), nullable = False, unique=True)
    phone_number = db.Column(db.Integer, nullable = False, unique = True)
    faculty = db.Column(db.String(3))
    course = db.Column(db.String(3))

    registration = db.relationship('Registration', backref='student', uselist=False)

    def __init__(self, student_id, name, phone_number, email, course, faculty):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.faculty = faculty
        self.course = course

    def __repr__(self):
        return '<Student : %r>' % str(self.student_id)

class Registration(db.Model):
    registration_id = db.Column(db.Integer, primary_key = True, nullable = False, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable = False)
    number_of_seats = db.Column(db.Integer, nullable = False)
    requests = db.Column(db.String)
    accepted = db.Column(db.Boolean, default=False, nullable = False)

    payment = db.relationship('Payment', backref='registration', uselist=False)
    robe = db.relationship('Robe', backref='registration', uselist=False)

    def __init__(self, registration_id, student_id, number_of_seats,  requests="", accepted=False):
        self.registration_id = registration_id
        self.student_id = student_id
        self.number_of_seats = number_of_seats
        self.accepted = accepted
        self.requests = requests

    def __repr__(self):
        return '<Registration : %r>' % self.registration_id

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key = True, nullable = False, unique=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.registration_id'), nullable = False)
    amount = db.Column(db.Double, nullable = False)
    date = db.Column(db.DateTime)
    has_payed = db.Column(db.Boolean, default=False, nullable = False)

    def __init__(self, payment_id, registration_id, amount, has_payed = False):
        self.payment_id = payment_id
        self.registration_id = registration_id
        self.amount = amount
        self.has_payed = has_payed

    def __repr__(self):
        return '<Payment : %r>' % str(self.payment_id)

class Robe(db.Model):
    robe_id = db.Column(db.Integer, primary_key = True, nullable = False, unique=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.registration_id'), nullable = False)
    robe_size = db.Column(db.Integer, nullable = False)

    def __init__(self, robe_id, registration_id, robe_size):
        self.robe_id = robe_id
        self.registration_id = registration_id
        self.robe_size = robe_size

    def __repr__(self):
        return '<Robe : %r>' % str(self.robe_id)
    
class Administration(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, admin_id, name, email, password):
        self.admin_id = admin_id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Administration : %r>' % (self.admin_id)