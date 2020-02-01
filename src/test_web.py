import unittest
import uuid
import requests
from flask import Flask
from flask_testing import LiveServerTestCase
from web import app as application

# Suppress logging output.
import os
import logging
logging.getLogger("werkzeug").disabled = True
os.environ["WERKZEUG_RUN_MAIN"] = "true"

class TestWeb(LiveServerTestCase):

	def create_app(self):
		app = application
		app.config["TESTING"] = True
		app.config['LIVESERVER_PORT'] = 15000
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
	def test_api_capture(self):
		response = requests.get(self.get_server_url() + "/api/capture/b813d0a3-f82f-4128-b1b6-a13957a42440?url=https%3A%2F%2Fyahoo.com")
		self.assertEqual(response.status_code, 200)

	def test_api_capture_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/capture/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 403)

	def test_api_capture_too_fast(self):
		response = requests.get(self.get_server_url() + "/api/capture/b813d0a3-f82f-4128-b1b6-a13957a42440?url=https%3A%2F%2Fyahoo.com")
		self.assertEqual(response.status_code, 429)

	def test_api_image(self):
		response = requests.get(self.get_server_url() + "/api/image/b813d0a3-f82f-4128-b1b6-a13957a42440/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 200)

	def test_api_image_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/image/{str(uuid.uuid4())}/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 403)

	def test_api_image_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/api/image/b813d0a3-f82f-4128-b1b6-a13957a42440/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	def test_api_image_not_ready(self):
		response = requests.get(self.get_server_url() + "/api/image/b813d0a3-f82f-4128-b1b6-a13957a42440/ed0ccb03-0d69-425b-a1d7-e8cea3bd2420")
		self.assertEqual(response.status_code, 202)

	# Needs RigidBit installation to proceed. Full validation will not be possible due to time delay.
	# def test_api_proof(self):
	# 	response = requests.get(self.get_server_url() + f"/api/proof/b813d0a3-f82f-4128-b1b6-a13957a42440/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
	# 	self.assertEqual(response.status_code, 403)

	def test_api_proof_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/proof/{str(uuid.uuid4())}/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 403)

	def test_api_proof_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/api/proof/b813d0a3-f82f-4128-b1b6-a13957a42440/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	def test_api_status(self):
		response = requests.get(self.get_server_url() + f"/api/status/b813d0a3-f82f-4128-b1b6-a13957a42440/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 200)

	def test_api_status_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/status/{str(uuid.uuid4())}/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 403)

	def test_api_status_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/api/status/b813d0a3-f82f-4128-b1b6-a13957a42440/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	def test_api_request(self):
		data = {"email": "test@test.com"}
		response = requests.post(self.get_server_url() + "/api/request", data=data)
		self.assertEqual(response.status_code, 200)

	def test_api_request_invalid_method(self):
		response = requests.get(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 405)

	def test_api_request_invalid_payload(self):
		response = requests.post(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 400)

	def test_api_activate(self):
		response = requests.get(self.get_server_url() + f"/api/activate/8723971f-b44b-4d83-aead-634d7e6b2eac")
		self.assertEqual(response.status_code, 200)

	def test_api_activate_already_used(self):
		response = requests.get(self.get_server_url() + f"/api/activate/8723971f-b44b-4d83-aead-634d7e6b2eac")
		self.assertEqual(response.status_code, 404)

	def test_api_activate_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/activate/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	# This cannot be done publicly since it would expose the secret key.
	# def test_api_upload_to_imgur(self):
	# 	response = requests.get(self.get_server_url() + f"/api/upload-to-imgur/b813d0a3-f82f-4128-b1b6-a13957a42440/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
	# 	self.assertEqual(response.status_code, 200)

	def test_api_upload_to_imgur_invalid_key(self):
		response = requests.get(self.get_server_url() + f"/api/upload-to-imgur/{str(uuid.uuid4())}/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 403)

	def test_api_upload_to_imgur_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/api/upload-to-imgur/b813d0a3-f82f-4128-b1b6-a13957a42440/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	# Web Routes
	def test_web_buried(self):
		response = requests.get(self.get_server_url() + "/web/buried", auth=requests.auth.HTTPBasicAuth("", "password"))
		self.assertEqual(response.status_code, 200)

	def test_web_buried_invalid_auth(self):
		response = requests.get(self.get_server_url() + "/web/buried")
		self.assertEqual(response.status_code, 401)

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

	def test_web_image(self):
		response = requests.get(self.get_server_url() + "/web/image/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 200)

	def test_web_image_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/web/image/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	def test_web_image_not_ready(self):
		response = requests.get(self.get_server_url() + "/web/image/ed0ccb03-0d69-425b-a1d7-e8cea3bd2420")
		self.assertEqual(response.status_code, 404)

	# Needs RigidBit installation to proceed. Full validation will not be possible due to time delay.
	# def test_web_proof(self):
	# 	response = requests.get(self.get_server_url() + "/web/proof/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
	# 	self.assertEqual(response.status_code, 200)

	def test_web_proof_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/web/proof/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)

	def test_web_stats(self):
		response = requests.get(self.get_server_url() + "/web/stats", auth=requests.auth.HTTPBasicAuth("", "password"))
		self.assertEqual(response.status_code, 200)

	def test_web_stats_invalid_auth(self):
		response = requests.get(self.get_server_url() + "/web/stats")
		self.assertEqual(response.status_code, 401)

	# This cannot be done publicly since it would expose the secret key.
	# def test_web_upload_to_imgur(self):
	# 	response = requests.get(self.get_server_url() + f"/web/upload-to-imgur/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
	# 	self.assertEqual(response.status_code, 200)

	# This cannot be done publicly since it would expose the secret key.
	# def test_web_upload_to_imgur_invalid_request(self):
	# 	response = requests.get(self.get_server_url() + f"/web/upload-to-imgur/{str(uuid.uuid4())}")
	# 	self.assertEqual(response.status_code, 404)

	def test_web_view(self):
		response = requests.get(self.get_server_url() + "/web/view/5f4bf25b-9bf7-4269-89a3-7d2ffd3e9605")
		self.assertEqual(response.status_code, 200)

	def test_web_view_invalid_request(self):
		response = requests.get(self.get_server_url() + f"/web/view/{str(uuid.uuid4())}")
		self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
	unittest.main()
