from dotenv import load_dotenv
import greenstalk
import json
import os
import psycopg2
import sys

import database as db
import screenshot as ss

def log_message(message):
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(message)

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
		# block_summary = generate_twitter_summary_block(summary, summary["data"]["id_str"])
		# block_image = generate_twitter_screenshot_block(filename_screenshot, summary["data"]["id_str"])

		# Update data record.
		data = {"queued": "false"}
		db.update_data_record_by_uuid(connection, payload["uuid"], data)
		log_message(f"Updated data record: {payload['uuid']}")

		queue.delete(job)
	except Exception as e:
		queue.bury(job)
		log_message("Buried.")
		raise e
	finally:
		log_message("")
		sys.stdout.flush()
