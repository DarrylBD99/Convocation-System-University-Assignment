from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session
from extentions import db, send_mail
from models import *

blueprints = Blueprint("admin", __name__, template_folder="templates")

def is_logged_in():
    if 'admin' in session: return True
    return False

@blueprints.route("/admin/")
def admin_index():
    if not is_logged_in(): return redirect('/admin/login')
    return render_template("admin/index.jinja")

#Admin Acceptance

@blueprints.route("/admin/acceptance", methods=['GET'])
def acceptance():
    if not is_logged_in(): return redirect('/admin/login')
    students = Student.query.order_by(Student.student_id).all()
    registration = Registration.query.all()

    pending = Registration.query.filter_by(accepted = False).all()
    accepted = Registration.query.filter_by(accepted = True).all()

    return render_template('admin/acceptance.jinja', students = students, registration = registration, pending = pending, accepted = accepted)

@blueprints.route("/admin/decline_registration/<int:id>")
def decline_registration(id):
    if not is_logged_in(): return redirect('/admin/acceptance')
    student_to_decline = Registration.query.filter_by(student_id = id).first()
    try:
        if (student_to_decline.robe): db.session.delete(student_to_decline.robe)
        if (student_to_decline.payment): db.session.delete(student_to_decline.payment)        
        db.session.delete(student_to_decline)
        db.session.commit()
        flash('Registration of student ' + str(id) + ' has been declined')

    except:
        flash('Error: Unable to declined registration of student: ' + str(id))

    return redirect('/admin/acceptance')

@blueprints.route("/admin/accept_registration/<int:id>")
def accept_registration(id):
    if not is_logged_in(): return redirect('/admin/acceptance')
    student_to_accept = Registration.query.filter_by(student_id=id).first()
    try:
        student_to_accept.accepted = True
        db.session.commit()
        flash('Registration of student ' + str(id) + ' has been accepted')
    except:
        flash('Error: Unable to accept registration of student: ' + str(id))
    
    return redirect('/admin/acceptance')

@blueprints.route("/admin/send_invitation/<student_id>")
def admin_registration_send_invite(student_id):
    if not is_logged_in(): return redirect('/admin/acceptance')
    
    body = """Dear Student,
    
Here is your QR code invitation to use during the convocation. Please do not send this to anyone else. The convocation plans will be provided in the attatchment below.
[insert qr code here]

If the qr code doesn't work, please use the link below:
[insert link here]

Thank you for registering!

Regards

(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)
"""

    title = "Convocation Invitation"
    try:
        send_mail(student_id, title, body)
        flash("Invitation has been sent to student " + student_id)
            
    except:
        flash("Error: invitation was not sent.")
    return redirect('/admin/acceptance')
#Admin Invite

@blueprints.route("/admin/students", methods=['GET'])
def admin_invite():
    if not is_logged_in(): return redirect('/admin/login')
    students = Student.query.order_by(Student.student_id).all()
    
    return render_template('admin/students.jinja', students = students)

@blueprints.route("/admin/send_invite/<id>", methods = ['GET'])
def admin_send_invite(id):
    if not is_logged_in(): return redirect('/admin/students')
    title = "Invitation to MMU Convocation"
    body = """Dear Student,

You have been invited to the 2024 MMU Convocation. Please accept the invitation using the link provided: http://127.0.0.1:5000/register/ More information regarding the convocation can be found in the pdf attatched below.

Regards

(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)
"""
    try:
        send_mail(id, title, body)
        flash('An email has been sent to student ' + id)
    except:
        flash('Error: Unable to send email to student' + id)
    
    return redirect('/admin/students')

#Admin Robe Management
@blueprints.route("/admin/robe")
def admin_robe_manage():
    if not is_logged_in(): return redirect('/admin/login')
    registration = Registration.query.order_by(Registration.student_id).all()
    robe = Robe.query.all()
    
    #Calculate the number of robes per size
    robe_size_quantities = []
    robe_sizes = []
    min_size = 15
    max_size = 30

    for size in range(min_size, (max_size + 1)):
        robes = Robe.query.filter_by(robe_size = size).all()
        
        if len(robes) > 0:
            robe_size_quantities.append(len(robes))
            robe_sizes.append(size)
        print(robe_size_quantities)
        print(robe_sizes)
    return render_template("admin/robe.jinja", registration = registration, robe = robe, robe_sizes = robe_sizes, robe_size_quantities = robe_size_quantities)

#Admin Payment Management
@blueprints.route("/admin/payment")
def admin_payment_manage():
    if not is_logged_in(): return redirect('/admin/login')
    registration = Registration.query.order_by(Registration.student_id).all()
    payment = Payment.query.all()

    return render_template("admin/payment.jinja", registration = registration, payment = payment)

@blueprints.route("/admin/send_bill/<student_id>")
def admin_payment_bill(student_id):
    if not is_logged_in(): return redirect('/admin/payment')
    registration = Registration.query.filter_by(student_id = student_id).first()
    payment = registration.payment
    
    current_datetime = datetime.now()
    payment.date = current_datetime
    body = """Dear Student,

Here is your bill for the convocation. To pay it, please use the link provided: http://127.0.0.1:5000/bill/

Date Bill Issued: """ + current_datetime.strftime("%m/%d/%Y") + """
Time Bill Issued: """ + current_datetime.strftime("%H:%M:%S") + """
Total bill amount: MYR """ + str(payment.amount) + """

Regards

(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)
"""
    title = "Convocation Bill"
    try:
        send_mail(student_id, title, body)
        
        try:
            db.session.commit()
            flash("Bill has been sent to student " + student_id)
        except:
            flash("Error: Bill has been sent, but database is not updated")
            
    except:
        flash("Error: billing email was not sent.")
    return redirect('/admin/payment')

@blueprints.route("/admin/send_reminder/<student_id>")
def admin_payment_reminder(student_id):
    if not is_logged_in(): return redirect('/admin/payment')
    registration = Registration.query.filter_by(student_id = student_id).first()
    payment = registration.payment
    body = """Dear Student,

We have not recieved your payment. Please pay as soom as possible or else your registration will be declined. Please use the link provided to pay the bill: http://127.0.0.1:5000/bill/

Date Bill Issued: """ + payment.date.strftime("%m/%d/%Y") + """
Time Bill Issued: """ + payment.date.strftime("%H:%M:%S") + """
Total bill amount: MYR """ + str(payment.amount) + """

Regards

(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)
"""
    title = "Convocation Bill Reminder"
    try:
        send_mail(student_id, title, body)
        flash("Reminder has been sent to student " + student_id)
            
    except:
        flash("Error: reminder email was not sent.")
    return redirect('/admin/payment')

@blueprints.route("/admin/send_receipt/<student_id>")
def admin_payment_receipt(student_id):
    if not is_logged_in(): return redirect('/admin/payment')
    registration = Registration.query.filter_by(student_id = student_id).first()
    
    seats = registration.number_of_seats
    
    body = """Dear Student,
    
Thank you for paying for the convocation. Here is your receipt:

Seats: """ + str(seats) + " - MYR " + str(float(seats * 30)) + "\n"

    if registration.robe:
        body += "+ Robe (size " + str(registration.robe.robe_size) + ") - MYR 20.0 \n"
    
    body += """Total bill amount: MYR """ + str(registration.payment.amount) + """

Regards

(This is meant to be a test for my Software Engineering Project. If you are receeiving this, please ignore as it is most likely accidental.)
"""

    title = "Convocation Receipt"
    try:
        send_mail(student_id, title, body)
        flash("Receipt has been sent to student " + student_id)
            
    except:
        flash("Error: receipt was not sent.")
    return redirect('/admin/payment')

#Admin Log In
@blueprints.route('/admin/login', methods=['GET', 'POST'])
def login():
    if is_logged_in(): return redirect('/admin')

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']

        admin = Administration.query.filter_by(name=username).first()

        if admin and admin.password == password:
            # Successful login, you can redirect or perform other actions here
            session['admin'] = admin.admin_id
            return redirect('/admin')
        else:
            flash('Invalid ID or password. Please try again.', 'error')

    return render_template('admin/login.jinja')

@blueprints.route('/admin/logout')
def logout():
    if is_logged_in(): session.pop('admin', None)
    return redirect('/admin/login')