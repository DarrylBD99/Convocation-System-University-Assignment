from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

db = SQLAlchemy()
mail = Mail()

def send_mail(id, title, body):
    from models import Student

    student = Student.query.filter_by(student_id = id).first()

    sender = "noreply@mmu.my"
    
    email = student.email
    message = Message(title, sender = sender, recipients=[email])
    message.body = body
    mail.send(message)