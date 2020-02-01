import unittest
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

	def test_terms_of_service(self):
		response = requests.get(self.get_server_url() + "/terms_of_service")
		self.assertEqual(response.status_code, 200)

	def test_api_capture_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/capture/x")
		self.assertEqual(response.status_code, 403)

	def test_api_image_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/image/x/x")
		self.assertEqual(response.status_code, 403)

	def test_api_proof_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/proof/x/x")
		self.assertEqual(response.status_code, 403)

	def test_api_status_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/status/x/x")
		self.assertEqual(response.status_code, 403)

	def test_api_request_invalid_method(self):
		response = requests.get(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 405)

	def test_api_request_invalid_payload(self):
		response = requests.post(self.get_server_url() + "/api/request")
		self.assertEqual(response.status_code, 400)

	def test_api_request_valid(self):
		data = {"email": "test@test.com"}
		response = requests.post(self.get_server_url() + "/api/request", data=data)
		self.assertEqual(response.status_code, 200)

	def test_api_activate_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/activate/x")
		self.assertEqual(response.status_code, 404)

	def test_api_upload_to_imgur_invalid_key(self):
		response = requests.get(self.get_server_url() + "/api/upload-to-imgur/x/x")
		self.assertEqual(response.status_code, 403)

	def test_web_buried_invalid_auth(self):
		response = requests.post(self.get_server_url() + "/web/buried")
		self.assertEqual(response.status_code, 401)

	def test_web_capture_invalid_method(self):
		response = requests.get(self.get_server_url() + "/web/capture")
		self.assertEqual(response.status_code, 405)

	def test_web_capture_invalid_data(self):
		data = {}
		response = requests.post(self.get_server_url() + "/web/capture", data=data)
		self.assertEqual(response.status_code, 400)

	def test_web_capture(self):
		data = {"url": "https://www.google.com/"}
		response = requests.post(self.get_server_url() + "/web/capture", data=data)
		self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
	unittest.main()
