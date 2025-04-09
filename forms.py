from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class PersonalRecordForm(FlaskForm):
    type = SelectField('Record Type', 
                      choices=[('self', 'Self'), 
                              ('spouse', 'Spouse'),
                              ('child', 'Child'),
                              ('account', 'Account')],
                      validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[Optional()])
    ssn = StringField('Social Security Number', validators=[Optional()])
    account_number = StringField('Account Number', validators=[Optional()])
    account_type = StringField('Account Type', validators=[Optional()])
    notes = TextAreaField('Additional Notes', validators=[Optional()])
    submit = SubmitField('Submit')