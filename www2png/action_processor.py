"""
Handles the processing of actions in the action queue.
"""

from dotenv import load_dotenv
import greenstalk
import json
import os
import sys
import time

from misc import log_message
import emails as e

##### ENTRY POINT #####

if __name__ == "__main__":
	load_dotenv()
	with greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), watch=[os.getenv("GREENSTALK_TUBE_ACTIONS")]) as action_queue:
		while True:
			job = action_queue.reserve()
			try:
				payload = json.loads(job.body)
				if payload["action"] == "send_api_request_email":
					email = payload["data"]["email"]
					challenge = payload["data"]["challenge"]
					e.send_api_request_email(email, challenge)
					log_message(f"Send API Request Email to: {email}")
				else:
					raise Exception("Invalid payload action")
				action_queue.delete(job)
			except Exception as e:
				action_queue.bury(job)
				log_message("Buried.")
				raise e
			finally:
				sys.stdout.flush()
