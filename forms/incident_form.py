from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired


class IncidentForm(FlaskForm):
    system = StringField('System', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    issue = TextAreaField('Issue Description', validators=[DataRequired()])
    date_of_occurrence = DateField('Date of Occurrence', format='%Y-%m-%d', validators=[DataRequired()])
    time_of_occurrence = TimeField('Time of Occurrence', format='%H:%M:%S', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Ongoing', 'Ongoing'), ('Resolved', 'Resolved')])
    submit = SubmitField('Submit')
