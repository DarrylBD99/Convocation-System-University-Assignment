import os
from flask import Flask
from blueprints import admin, bill, registration
from extentions import db, mail

db_name = 'database.sqlite3'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_name
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

app.config['SECRET_KEY'] = 'se5dr6ft7yguhijo'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = <insert google account>
# app.config['MAIL_PASSWORD'] = <insert google app password>

db.init_app(app)
mail.init_app(app)

app.register_blueprint(admin.blueprints)
app.register_blueprint(registration.blueprints)
app.register_blueprint(bill.blueprints)

with app.app_context():
    db.create_all()

    from models import Student, Administration

    admin = Administration(1, "admin", "#####@mail.com", "mmu")
    id = admin.admin_id
    
    if (Administration.query.filter_by(admin_id = id).first()):
        db.session.add(admin)

    db.session.commit()

    

if __name__ == "__main__":
    app.run(debug=True)