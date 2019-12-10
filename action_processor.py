from dotenv import load_dotenv
import greenstalk
import json
import os
import sys
import time

import emails as e

def log_message(message):
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(message)
		print("")

##### ENTRY POINT #####

load_dotenv()

action_queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), watch=[os.getenv("GREENSTALK_TUBE_ACTIONS")])

while True:
	job = action_queue.reserve()

	try:
		payload = json.loads(job.body)

		if payload["action"] == "send_api_request_email":
			email = payload["data"]["email"]
			challenge = payload["data"]["challenge"]
			e.send_api_request_email(email, challenge)
			log_message(f"Send API Request E-mail to: {email}")
		else:
			raise Exception("Invalid payload action")

		action_queue.delete(job)
	except Exception as e:
		action_queue.bury(job)
		log_message("Buried.")
		raise e
	finally:
		sys.stdout.flush()
