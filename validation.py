from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField
from wtforms.validators import DataRequired, Email, Optional, URL, regexp as regexp_validator

class CaptureForm(FlaskForm):
	class Meta:
		csrf = False
	delay = StringField("delay", validators=[Optional(), regexp_validator(r"^\d+$")])
	full_page = StringField("full_page", validators=[Optional(), regexp_validator(r"^(true|false)$")])
	resolution = StringField("resolution", validators=[Optional(), regexp_validator(r"^\d+x\d+$")])
	url = StringField("url", validators=[DataRequired(), URL()])

class ApiKeyForm(FlaskForm):
	class Meta:
		csrf = False
	email = StringField("email", validators=[DataRequired(), Email()])

class BuriedForm(FlaskForm):
	class Meta:
		csrf = False
	action = StringField("action", validators=[DataRequired()])
	job_id = IntegerField("job_id", validators=[DataRequired()])