from dotenv import load_dotenv
import psycopg2
import os
import sys
import time

import database as db
import screenshot as ss

def log_message(message):
	"""Log a message the console."""
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(message)
		print("")

def prune_expired_data_records(connection):
	records = db.get_expired_data_records(connection, int(os.getenv("WWW2PNG_SCREENSHOT_PRUNE_DELAY")))
	for record in records:
		try:
			data = {"pruned": "true"}
			db.update_data_record(connection, record["id"], data)
			log_message(f'Pruned data record: {record["id"]}')
			screenshot_filename = ss.determine_screenshot_filename(record["request_id"])
			os.remove(screenshot_filename)
			log_message(f'Deleted screenshot: {screenshot_filename}')
		except FileNotFoundError:
			log_message(f'Failed to delete screenshot: {screenshot_filename}')

def prune_expired_unverified_user_records(connection):
	records = db.get_expired_unverified_user_records(connection, int(os.getenv("WWW2PNG_UNVERIFIED_USER_PRUNE_DELAY")))
	for record in records:
		db.delete_unverified_user_record(connection, record["id"])
		log_message(f'Pruned unverified user record: {record["id"]} {record["email"]}')

##### ENTRY POINT #####

load_dotenv()
connection = psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))

while True:
	try:
		prune_expired_data_records(connection)
		connection.commit()
		prune_expired_unverified_user_records(connection)
		connection.commit()
	except Exception as e:
		log_message("Buried.")
		raise e
	finally:
		sys.stdout.flush()
	time.sleep(int(os.getenv("WWW2PNG_PRUNE_LOOP_DELAY")))
