from dotenv import load_dotenv
import psycopg2
import os
import sys

import database as db
import screenshot as ss

def log_message(message):
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(message)

##### ENTRY POINT #####

load_dotenv()
connection = psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))

try:
	records = db.get_expired_data_records(connection, int(os.getenv("WWW2PNG_SCREENSHOT_PRUNE_DELAY")))
	for record in records:
		data = {"pruned": "true"}
		db.update_data_record(connection, record["id"], data)
		log_message(f'Pruned record: {record["id"]}')
		screenshot_filename = ss.determine_screenshot_filename(record["uuid"])
		os.remove(screenshot_filename)
		log_message(f'Deleted screenshot: {screenshot_filename}')
except Exception as e:
	log_message("Buried.")
	raise e
finally:
	log_message("")
	sys.stdout.flush()
