from dotenv import load_dotenv
import greenstalk
import json
import os
import psycopg2
import sys

import blockchain as b
import database as db
import screenshot as ss

def log_message(message):
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(message)
		print("")

##### ENTRY POINT #####

load_dotenv()
connection = psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))
queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), watch=[os.getenv("GREENSTALK_TUBE_QUEUE")])

while True:
	job = queue.reserve()

	try:
		payload = json.loads(job.body)

		# Generate screenshot
		ss.generate_screenshot(payload["uuid"], payload["settings"])
		filename_screenshot = ss.determine_screenshot_filename(payload["uuid"])
		log_message(f"Generated screenshot: {filename_screenshot}")

		# Generate blocks.
		block = b.generate_screenshot_block(filename_screenshot)
		log_message(f"Block created: {block['id']}")

		# Update data record.
		data = {"queued": "false", "block_id": block["id"]}
		db.update_data_record_by_uuid(connection, payload["uuid"], data)
		connection.commit()
		log_message(f"Updated data record: {payload['uuid']}")

		queue.delete(job)
	except Exception as e:
		queue.bury(job)
		log_message("Buried.")
		raise e
	finally:
		sys.stdout.flush()
