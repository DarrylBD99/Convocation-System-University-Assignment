from flask import Blueprint, flash, redirect, render_template, request, session
from extentions import send_mail

from models import *

blueprints = Blueprint("invitation", __name__, template_folder="templates")

def is_logged_in(id = ""):
    if 'student' in session and (not id or id != session['student']): return True
    return False

def has_registered():
    student_registered = Student.query.filter_by(student_id = session['student']).first()
    if student_registered.registration:
        flash("Error, student " + session['student'] + " has already registered. If this is a mistake or you would like to change the submitted info, please contact ###-#######")
        session.pop('student', None)

    return student_registered.registration

@blueprints.route("/register/")
def invite_base():
    if is_logged_in() and not has_registered():
        return redirect("/register/form")
    return redirect("/register/login")

@blueprints.route("/register/login", methods = ['POST', 'GET'])
def invite_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        student = Student.query.filter_by(student_id = student_id).first()
        
        if student:
            session['student'] = student_id
            return redirect("/register")
        else:
            flash("Error, student " + student_id + " doesn't exist in database or hasn't graduated. If this is a mistake, please contact ###-#######")
        
    return render_template("login.jinja")

@blueprints.route("/register/form", methods = ['POST', 'GET'])
def invite_form():
    if not is_logged_in(): return redirect("/register/login")

    id = session['student']

    if request.method == 'POST':
        registration = Registration.query.all()

        payment = Payment.query.all()

        seats = int(request.form.get('seats'))
        robe_size = request.form.get('robe_size')
        
        requests = request.form.get('requests')

        registration_id = int(len(registration) + 1) 
        payment_id = int(len(payment) + 1)
        
        price = seats * 30
        if robe_size: price = price + 20
        
        new_register = Registration(registration_id, id, seats, requests, False)
        db.session.add(new_register)
        
        new_payment = Payment(payment_id, registration_id, price)
        db.session.add(new_payment)
        
        if robe_size:
            robes = Robe.query.all()
            robe_id = len(robes) + 1
            new_robe = Robe(robe_id, registration_id, robe_size)
            db.session.add(new_robe)
        
        body = """Dear Student,

Thank you for filling in your Convocation Registration Form. Here are the details regarding your registration: 

ID: """ + id + "\nSeats Booked: " + str(seats) + "\n"
        if robe_size: body += "Robe Size: " + str(robe_size)
        else: body += "Robe: Not booked"

        body += "\nRequests: "
        if requests: body += requests
        else: body += "None"

        body += "\n\nIf there is any inquiries or mistakes found, contact ###-#######. Please do so before the bill is sent, or else it will become more complicated.\n\nRegards\n\n(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)"

        title = "Convocation Registration Complete"

        print("start")
        try:
            db.session.commit()
            try:
                send_mail(id, title, body)
                flash("Thank you for filling in the form! An auto-generated email will be sent shortly.")
                session.pop('student', None)
                return redirect('/register/login')
            except:
                flash("Error: Registration to the database, but email sending has failed")
        except:
            flash("Error: Unable to add your registration to the database")

    student = Student.query.filter_by(student_id=id).first()
    return render_template("invite/form.jinja", student = student)