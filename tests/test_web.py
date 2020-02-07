from flask import Flask
from flask_testing import LiveServerTestCase
import os
import psycopg2
import requests
import sys
import time
import unittest
import uuid

# Fix path to allow application import.
sys.path.insert(2, os.path.abspath(os.path.join(sys.path[0], "..", "www2png")))
from web import app as application
from database import connect

# Suppress logging output.
import os
import logging
logging.getLogger("werkzeug").disabled = True
os.environ["WERKZEUG_RUN_MAIN"] = "true"

def get_unverified_user_record(connection):
	"""Retrieve a recent unverified user record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM unverified_users ORDER BY id DESC LIMIT 1")
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def create_unverified_challenge(connection, server_url):
	"""Setup a unverified challenge to be used later."""
	data = {"email": f"""{uuid.uuid4()}@mailinator.com"""}
	requests.post(server_url + "/api/request", data=data)
	record = get_unverified_user_record(connection)
	return record["challenge"]

def create_api_key(connection, server_url):
	data = {"email": f"""{uuid.uuid4()}@test.com"""}
	requests.post(server_url + "/api/request", data=data)
	record = get_unverified_user_record(connection)
	requests.get(server_url + f"""/api/activate/{record["challenge"]}""")
	return record["challenge"]

class TestWeb(LiveServerTestCase):

	@classmethod
	def setUpClass(self):
		self.connection = connect()
		self.test_data = {}
		self.test_data["api_key"] = None # Placeholder
		self.test_data["invalid_api_key"] = str(uuid.uuid4())
		self.test_data["invalid_request_id"] = str(uuid.uuid4())
		self.test_data["pending_request_id"] = "ed0ccb03-0d69-425b-a1d7-e8cea3bd2420"
		self.test_data["session_id"] = str(uuid.uuid4())
		self.test_data["unverified_challenge"] = None # Placeholder

	def create_app(self):
		app = application
		app.config["TESTING"] = True
		app.config["LIVESERVER_PORT"] = 0
		return app

	# Static Routes

	def test_root(self):
		response = requests.get(self.get_server_url())
		self.assertEqual(response.status_code, 200)

	def test_api_help(self):
		response = requests.get(self.get_server_url() + "/api/help")
		self.assertEqual(response.status_code, 200)

	def test_contact(self):
		response = requests.get(self.get_server_url() + "/contact")
		self.assertEqual(response.status_code, 200)

	def test_ping(self):
		response = requests.get(self.get_server_url() + "/ping")
		self.assertEqual(response.status_code, 200)

	def test_privacy_policy(self):
		response = requests.get(self.get_server_url() + "/privacy_policy")
		self.assertEqual(response.status_code, 200)

	def test_terms_of_service(self):
		response = requests.get(self.get_server_url() + "/terms_of_service")
		self.assertEqual(response.status_code, 200)

	# API Routes

	# This needs to be updated so it doesn't fail on dev systems with 429.
	def test_api_capture(self):
		self.test_data["api_key"] = create_api_key(self.connection, self.get_server_url())
		response = requests.get(self.get_server_url() + f"""/api/capture/{self.test_data["api_key"]}?url=https%3A%2F%2Fyahoo.com%3Fsession_id%3D{self.test_data["session_id"]}""")
		self.assertEqual(response.status_code, 200)
		self.test_data["request_id"] = response.json()["request_id"]

	def test_api_capture_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/capture/{self.test_data["invalid_api_key"]}""")
		self.assertEqual(response.status_code, 403)

	def test_api_capture_too_fast(self):
		response = requests.get(self.get_server_url() + f"""/api/capture/{self.test_data["api_key"]}?url=https%3A%2F%2Fyahoo.com%3Fsession_id%3D{self.test_data["session_id"]}""")
		self.assertEqual(response.status_code, 429)

	# This test is broken because the image file will not be present.
	# def test_api_image(self):
	# 	response = requests.get(self.get_server_url() + f"""/api/image/{self.test_data["api_key"]}/{self.test_data["request_id"]}""")
	# 	self.assertEqual(response.status_code, 200)

	def test_api_image_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/image/{self.test_data["invalid_api_key"]}/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 403)

	def test_api_image_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/api/image/{self.test_data["api_key"]}/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	def test_api_image_not_ready(self):
		response = requests.get(self.get_server_url() + f"""/api/image/{self.test_data["api_key"]}/{self.test_data["pending_request_id"]}""")
		self.assertEqual(response.status_code, 202)

	# Needs RigidBit installation to proceed. Full validation will not be possible due to time delay.
	# def test_api_proof(self):
	# 	response = requests.get(self.get_server_url() + f"""/api/proof/{self.test_data["api_key"]}/{self.test_data["request_id"]}""")
	# 	self.assertEqual(response.status_code, 403)

	def test_api_proof_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/proof/{self.test_data["invalid_api_key"]}/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 403)

	def test_api_proof_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/api/proof/{self.test_data["api_key"]}/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	def test_api_status(self):
		response = requests.get(self.get_server_url() + f"""/api/status/{self.test_data["api_key"]}/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 200)

	def test_api_status_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/status/{self.test_data["invalid_api_key"]}/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 403)

	def test_api_status_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/api/status/{self.test_data["api_key"]}/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	def test_api_request(self):
		data = {"email": f"""{uuid.uuid4()}@mailinator.com"""}
		response = requests.post(self.get_server_url() + "/api/request", data=data)
		self.assertEqual(response.status_code, 200)

	def test_api_request_invalid_method(self):
		response = requests.get(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 405)

	def test_api_request_invalid_payload(self):
		response = requests.post(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 400)

	def test_api_activate(self):
		self.test_data["unverified_challenge"] = create_unverified_challenge(self.connection, self.get_server_url())
		response = requests.get(self.get_server_url() + f"""/api/activate/{self.test_data["unverified_challenge"]}""")
		self.assertEqual(response.status_code, 200)

	def test_api_activate_already_used(self):
		response = requests.get(self.get_server_url() + f"""/api/activate/{self.test_data["unverified_challenge"]}""")
		self.assertEqual(response.status_code, 404)

	def test_api_activate_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/activate/{self.test_data["invalid_api_key"]}""")
		self.assertEqual(response.status_code, 404)

	# This cannot be done publicly since it would expose the secret key.
	# def test_api_upload_to_imgur(self):
	# 	response = requests.get(self.get_server_url() + f"""/api/upload-to-imgur/{self.test_data["api_key"]}/{self.test_data["request_id"]}""")
	# 	self.assertEqual(response.status_code, 200)

	def test_api_upload_to_imgur_invalid_key(self):
		response = requests.get(self.get_server_url() + f"""/api/upload-to-imgur/{self.test_data["invalid_api_key"]}/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 403)

	def test_api_upload_to_imgur_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/api/upload-to-imgur/{self.test_data["api_key"]}/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	# Web Routes

	def test_web_buried(self):
		response = requests.get(self.get_server_url() + "/web/buried", auth=requests.auth.HTTPBasicAuth("", "password"))
		self.assertEqual(response.status_code, 200)

	def test_web_buried_invalid_auth(self):
		response = requests.get(self.get_server_url() + "/web/buried")
		self.assertEqual(response.status_code, 401)

	# This needs to be updated so it doesn't fail on dev systems with 429.
	def test_web_capture(self):
		data = {"url": "https://www.google.com/"}
		response = requests.post(self.get_server_url() + "/web/capture", data=data)
		self.assertEqual(response.status_code, 200)

	def test_web_capture_invalid_method(self):
		response = requests.get(self.get_server_url() + "/web/capture")
		self.assertEqual(response.status_code, 405)

	def test_web_capture_invalid_data(self):
		data = {}
		response = requests.post(self.get_server_url() + "/web/capture", data=data)
		self.assertEqual(response.status_code, 400)

	# This test is broken because the image file will not be present.
	# def test_web_image(self):
	# 	response = requests.get(self.get_server_url() + "/web/image/{self.test_data["request_id"]}")
	# 	self.assertEqual(response.status_code, 200)

	def test_web_image_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/web/image/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	def test_web_image_not_ready(self):
		response = requests.get(self.get_server_url() + f"""/web/image/{self.test_data["pending_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	# Needs RigidBit installation to proceed. Full validation will not be possible due to time delay.
	# def test_web_proof(self):
	# 	response = requests.get(self.get_server_url() + "/web/proof/{self.test_data["request_id"]}")
	# 	self.assertEqual(response.status_code, 200)

	def test_web_proof_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/web/proof/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)

	def test_web_stats(self):
		response = requests.get(self.get_server_url() + "/web/stats", auth=requests.auth.HTTPBasicAuth("", "password"))
		self.assertEqual(response.status_code, 200)

	def test_web_stats_invalid_auth(self):
		response = requests.get(self.get_server_url() + "/web/stats")
		self.assertEqual(response.status_code, 401)

	# This cannot be done publicly since it would expose the secret key.
	# def test_web_upload_to_imgur(self):
	# 	response = requests.get(self.get_server_url() + f"""/web/upload-to-imgur/{self.test_data["request_id"]}""")
	# 	self.assertEqual(response.status_code, 200)

	# This cannot be done publicly since it would expose the secret key.
	# def test_web_upload_to_imgur_invalid_request(self):
	# 	response = requests.get(self.get_server_url() + f"""/web/upload-to-imgur/{str(uuid.uuid4())}""")
	# 	self.assertEqual(response.status_code, 404)

	def test_web_view(self):
		response = requests.get(self.get_server_url() + f"""/web/view/{self.test_data["request_id"]}""")
		self.assertEqual(response.status_code, 200)

	def test_web_view_invalid_request(self):
		response = requests.get(self.get_server_url() + f"""/web/view/{self.test_data["invalid_request_id"]}""")
		self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
	unittest.main()
