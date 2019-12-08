from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired, URL, regexp as regexp_validator

class CaptureForm(FlaskForm):
	class Meta:
		csrf = False
	delay = StringField("delay", validators=[DataRequired(), regexp_validator(r"^\d+$")])
	full_page = StringField("full_page", validators=[DataRequired(), regexp_validator(r"^(true|false)$")])
	resolution = StringField("resolution", validators=[regexp_validator(r"^\d+x\d+$")])
	url = StringField("url", validators=[DataRequired(), URL()])
