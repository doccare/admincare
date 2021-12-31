from datetime import datetime, date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin
import re
from sqlalchemy.dialects.sqlite import TIME


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    type1=db.Column(db.String(60), nullable=False)
    unique_id=db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    labtest_Post = db.relationship('Labtest_Post', backref='author1', lazy=True)
    patientcare_Post = db.relationship('Patientcare_Post', backref='author2', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.type1}', '{self.image_file}', '{self.unique_id}')"


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id=db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #date = db.Column(db.String(120), unique=True, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(400), nullable=False)
    state = db.Column(db.String(400), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}', '{self.date}', '{self.categorgy}', '{self.year}', '{self.address}', '{self.unique_id}','{self.fees}','{self.contact}','{self.state}','{self.locality}')"


    #posts = db.relationship('Post', backref='author', lazy=True)

    '''def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"'''

class Labtest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id=db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #date = db.Column(db.String(120), unique=True, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(400), nullable=False)
    state = db.Column(db.String(400), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date}', '{self.categorgy}', '{self.year}', '{self.address}', '{self.unique_id}','{self.fees}','{self.contact}','{self.state}','{self.locality}')"



class PatientCare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id=db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #date = db.Column(db.String(120), unique=True, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(400), nullable=False)
    state = db.Column(db.String(400), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date}', '{self.categorgy}', '{self.year}', '{self.address}', '{self.unique_id}','{self.fees}','{self.contact}','{self.state}','{self.locality}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    slot_time = db.Column(db.String(10), nullable=False)
    docunique_id=db.Column(db.String(100), nullable=False)
    weekday = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}', '{self.start_date}', '{self.end_date}', '{self.start_time}', '{self.end_time}', '{self.year}', '{self.categorgy},'{self.fees}','{self.contact}','{self.state}','{self.locality}','{self.docunique_id}','{self.weekday}')"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(100), nullable=False)
    client_UID = db.Column(db.String(100), nullable=False)
    docname = db.Column(db.String(100), nullable=False)
    doc_UID = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    app_date = db.Column(db.Date, nullable=False)
    app_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.String(100), nullable=True)
    appunique_id = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        return f"Appointment('{self.clientname}', '{self.client_UID}', '{self.docname}', '{self.doc_UID}', '{self.date_posted}', '{self.app_date}', '{self.app_time}', '{self.appunique_id}')"

class Labtest_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(400), nullable=False)
    state = db.Column(db.String(400), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    slot_time = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    labunique_id=db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Labtest_Post('{self.title}', '{self.date_posted}', '{self.content}', '{self.start_date}', '{self.end_date}', '{self.start_time}', '{self.end_time}', '{self.year}', '{self.categorgy}','{self.fees}','{self.contact}','{self.state}','{self.locality}','{self.labunique_id}')"

class Labtest_Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(100), nullable=False)
    client_UID = db.Column(db.String(100), nullable=False)
    docname = db.Column(db.String(100), nullable=False)
    doc_UID = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    app_date = db.Column(db.Date, nullable=False)
    app_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Labtest_Appointment('{self.clientname}', '{self.client_UID}', '{self.docname}', '{self.doc_UID}', '{self.date_posted}', '{self.app_date}', '{self.app_time}')"

class Patientcare_Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.TIME, nullable=False)
    end_time = db.Column(db.TIME, nullable=False)
    categorgy = db.Column(db.String(120),nullable=False)
    year = db.Column(db.String(120),nullable=False)
    fees= db.Column(db.String(12), nullable=False)
    contact= db.Column(db.String(400), nullable=False)
    state = db.Column(db.String(400), nullable=False)
    locality = db.Column(db.String(400), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    slot_time = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    careunique_id=db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Patientcare_Post('{self.title}', '{self.date_posted}', '{self.content}', '{self.start_date}', '{self.end_date}', '{self.start_time}', '{self.end_time}', '{self.year}', '{self.categorgy},'{self.fees}','{self.contact}','{self.state}','{self.locality}','{self.careunique_id}')"

class Patientcare_Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(100), nullable=False)
    client_UID = db.Column(db.String(100), nullable=False)
    docname = db.Column(db.String(100), nullable=False)
    doc_UID = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    app_date = db.Column(db.Date, nullable=False)
    app_time = db.Column(db.TIME, nullable=False)
    status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Patientcare_Appointment('{self.clientname}', '{self.client_UID}', '{self.docname}', '{self.doc_UID}', '{self.date_posted}', '{self.app_date}', '{self.app_time}')"


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"OTP('{self.email}', '{self.otp}')"
