from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,\
    SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import Length, InputRequired, Regexp, Email,\
    NumberRange


class GradeForm(FlaskForm):
    name = StringField('New Grade',
                       validators=[InputRequired(), Length(min=2, max=25)])
    submit = SubmitField('')


class WorkerForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[InputRequired(),
                                         Length(min=2, max=50),
                                         Regexp('[A-Z][a-z]+')])
    last_name = StringField('Last name',
                            validators=[InputRequired(),
                                        Length(min=2, max=50),
                                        Regexp('[A-Z][a-z]+')])
    surname = StringField('Surname',
                          validators=[InputRequired(),
                                      Length(min=2, max=50),
                                      Regexp('[A-Z][a-z]+')])
    address = StringField('Address',
                          validators=[InputRequired(),
                                      Length(min=2, max=100)])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    mobile = StringField('Mobile phone',
                         validators=[InputRequired(),
                                     Regexp('\\+380[0-9]{2}\\s?[0-9]{3}\\s?[0-9]{4}')])
    grade = SelectField('Grade', validators=[InputRequired()])
    salary = IntegerField('Salary',
                          widget=NumberInput(),
                          validators=[InputRequired(), NumberRange(min=0)])
    hired_at = DateField('Hired ad',
                         validators=[InputRequired()])
    submit = SubmitField('')
