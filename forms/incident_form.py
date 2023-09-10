from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired


class IncidentForm(FlaskForm):
    system = StringField('System', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    issue = TextAreaField('Issue Description', validators=[DataRequired()])
    time_of_occurrence = DateTimeField('Time of First Occurrence', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Ongoing', 'Ongoing'), ('Resolved', 'Resolved')])
    submit = SubmitField('Submit')
