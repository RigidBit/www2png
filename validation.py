from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, URL

class CaptureForm(FlaskForm):
	class Meta:
		csrf = False
	resolution = StringField("resolution", validators=[DataRequired()])
	url = StringField("url", validators=[DataRequired(), URL()])
	# name = StringField("name", validators=[DataRequired()])
