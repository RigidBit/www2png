from dotenv import load_dotenv
import greenstalk
import json
import os
import psycopg2
import sys
import threading
import time

import blockchain as b
import database as db
import screenshot as ss

def log_message(message):
	if os.getenv("WWW2PNG_VERBOSE") == "true":
		print(threading.current_thread().name, message)
		print("")
		sys.stdout.flush()

def start_processing_thread():
	connection = psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))
	queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), watch=[os.getenv("GREENSTALK_TUBE_QUEUE")])
	while True:
		job = queue.reserve()

		try:
			payload = json.loads(job.body)
			log_message(f"Processing job: {job.body}")

			# Generate screenshot
			ss.generate_screenshot(payload["request_id"], payload["settings"])
			filename_screenshot = ss.determine_screenshot_filename(payload["request_id"])
			log_message(f"Generated screenshot: {filename_screenshot}")

			# Generate blocks.
			block = b.generate_screenshot_block(filename_screenshot)
			log_message(f"Block created: {block['id']}")

			# Update data record.
			data = {"queued": "false", "block_id": block["id"]}
			db.update_data_record_by_request_id(connection, payload["request_id"], data)
			connection.commit()
			log_message(f"Updated data record: {payload['request_id']}")

			queue.delete(job)
		except:
			queue.release(job)
			log_message("Released.")
			raise
		finally:
			sys.stdout.flush()

##### ENTRY POINT #####

load_dotenv()

thread_count = int(os.getenv("WWW2PNG_PROCESSING_THREADS"))
threads = []
while True:	
	if len(threads)	< thread_count:
		thread = threading.Thread(target=start_processing_thread, daemon=True)
		thread.start()
		threads.append(thread)
		log_message(f"Spawned thread: {thread.name}")
	for thread in threads:
		if not thread.is_alive():
			log_message(f"Removing dead thread: {thread.name}")
			threads.remove(thread)
			break
	time.sleep(1)
