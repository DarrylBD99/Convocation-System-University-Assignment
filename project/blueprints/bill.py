from flask import Blueprint, flash, redirect, render_template, request, session
from extentions import send_mail, db

from models import Registration, Payment

blueprints = Blueprint("bill", __name__, template_folder="templates")

def is_logged_in(id = ""):
    if 'student_bill' in session and (not id or id != session['student_bill']): return True
    return False

def has_payed():
    student_payed = Registration.query.filter_by(student_id = session['student_bill']).first()
    if student_payed.payment.has_payed:
        session.pop('student_bill', None)
    return student_payed.payment.has_payed

@blueprints.route("/bill/")
def invite_base():
    if is_logged_in():
        id = session['student_bill']
        if has_payed():
            return "Student " + id + " has already payed. If this is a mistake, please contact ###-#######"
        else:
            registration = Registration.query.filter_by(student_id = id).first()
            payment = Payment.query.filter_by(registration_id = registration.registration_id).first()
            payment.has_payed = True
            session.pop('student_bill', None)
            try:
                db.session.commit()
                return "Student " + id + " has successfully paid. Receipt will be sent to you shortly."
            except:
                return "Error: Unable to pay. Database cannot be updated."
    else:
        return redirect("/bill/login")

@blueprints.route("/bill/login", methods = ['POST', 'GET'])
def invite_login():
    if is_logged_in():
        redirect('/bill')
        
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        registration = Registration.query.filter_by(student_id = student_id).first()
        
        if registration:
            session['student_bill'] = student_id
            return redirect("/bill")
        else:
            flash("Error, student " + student_id + " has not registered. If this is a mistake, please contact ###-#######")
        
    return render_template("login.jinja")
