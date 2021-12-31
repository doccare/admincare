from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField, SelectField,DateField,TimeField,IntegerField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Doctor, Appointment,Labtest_Post,Labtest_Appointment,Patientcare_Post,Patientcare_Appointment
#from wtforms.fields.html5 import DateField
#from flask DatePickerWidget

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    type1=SelectField('Type',choices=[('Doctor', 'Doctor'),('client','client'),('labtest','labtest'),('Patient_care','Patient_care')],
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DoctorAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    categorgy =SelectField('Categorgy',choices=[('General Physicians', 'General Physicians'),('Pediatricians', 'Pediatricians'),('General Surgeon', 'General Surgeon'),('Cardiologist', 'Cardiologist'),('Dentist', 'Dentist'),('Dermatologists', 'Dermatologists'),('Gynecologist', 'Gynecologist'),('ENT Specialist', 'ENT Specialist')],validators=[DataRequired()])
    year =IntegerField('Year of experience',validators=[DataRequired()])
    fees =IntegerField('FEE',validators=[DataRequired()])
    contact =IntegerField('Mobile Number',validators=[DataRequired()])
    state =SelectField('State',choices=[('Pondicherry', 'Pondicherry')],validators=[DataRequired()])
    locality =SelectField('locality',choices=[('Lawspet', 'Lawspet'),('Morattandi', 'Morattandi'),('Sedarapet', 'Sedarapet'),('Muthailpet', 'Muthailpet')],validators=[DataRequired()])
    address =StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class LABAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    categorgy =SelectField('Categorgy',choices=[('General', 'General'),('General1', 'General1'),('General2', 'General2')],
                           validators=[DataRequired()])
    year =SelectField('Year of experience',choices=[('1', '1'),('2','2'),('3','3')],
                           validators=[DataRequired()])
    fees =IntegerField('FEE',validators=[DataRequired()])
    contact =IntegerField('Mobile Number',validators=[DataRequired()])
    state =SelectField('State',choices=[('Pondicherry', 'Pondicherry')],validators=[DataRequired()])
    locality =SelectField('locality',choices=[('Lawspet', 'Lawspet'),('Morattandi', 'Morattandi'),('Sedarapet', 'Sedarapet'),('Muthailpet', 'Muthailpet')],validators=[DataRequired()])
    address =StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class CareAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    categorgy =SelectField('Categorgy',choices=[('General', 'General'),('General1', 'General1'),('General2', 'General2')],
                           validators=[DataRequired()])
    year =SelectField('Year of experience',choices=[('1', '1'),('2','2'),('3','3')],
                           validators=[DataRequired()])
    fees =IntegerField('FEE',validators=[DataRequired()])
    contact =IntegerField('Mobile Number',validators=[DataRequired()])
    state =SelectField('State',choices=[('Pondicherry', 'Pondicherry')],validators=[DataRequired()])
    locality =SelectField('locality',choices=[('Lawspet', 'Lawspet'),('Morattandi', 'Morattandi'),('Sedarapet', 'Sedarapet'),('Muthailpet', 'Muthailpet')],validators=[DataRequired()])
    address =StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    #date = DateTimeField('Which date is your favorite?', format='%m/%d/%y', validators=[DataRequired()])
    #title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    slot_time = TextAreaField('Slot time', validators=[DataRequired()])
    multi = SelectMultipleField('Select day',choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')],coerce=int)
    submit = SubmitField('Post')


class LabtestForm(FlaskForm):
    #date = DateTimeField('Which date is your favorite?', format='%m/%d/%y', validators=[DataRequired()])
    #title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    slot_time = TextAreaField('Slot time', validators=[DataRequired()])
    submit = SubmitField('Post')

class PatientcareForm(FlaskForm):
    #date = DateTimeField('Which date is your favorite?', format='%m/%d/%y', validators=[DataRequired()])
    #title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start time', validators=[DataRequired()])
    end_time = TimeField('End time', validators=[DataRequired()])
    slot_time = TextAreaField('Slot time', validators=[DataRequired()])
    submit = SubmitField('Post')



class AppointmentForm(FlaskForm):
    #date = DateTimeField('Which date is your favorite?', format='%m/%d/%y', validators=[DataRequired()])

    end_date1 = DateField('End Date', validators=[DataRequired()])
    start_time1 = TimeField('Start time', validators=[DataRequired()])

    submit = SubmitField('Post')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
