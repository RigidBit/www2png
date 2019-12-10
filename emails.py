import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_api_request_email(smtp_receiver, challenge):
	smtp_sender = os.getenv("SMTP_SENDER")
	smtp_host = os.getenv("SMTP_HOST")
	smtp_port = int(os.getenv("SMTP_PORT"))
	smtp_user = os.getenv("SMTP_USER")
	smtp_pass = os.getenv("SMTP_PASS")

	message = MIMEMultipart("alternative")
	message["Subject"] = "Your WWW2PNG API Key"
	message["From"] = smtp_sender
	message["To"] = smtp_receiver

	message_text = f"Your API Key is: {challenge}\n\n"
	message_text += f"Please open the following URL to activate your API Key: https://www2png.com/api/activate/{challenge}\n\n"
	message_text += "Activating this key will deactivate any previous key associated with this e-mail address."

	message.attach(MIMEText(message_text, "plain"))

	try:
		context = ssl.create_default_context()
		server = smtplib.SMTP(smtp_host, smtp_port)
		server.starttls(context=context)
		server.login(smtp_user, smtp_pass)
		server.sendmail(smtp_sender, smtp_receiver, message.as_string())
	except Exception as e:
		raise e
	finally:
		server.quit()
