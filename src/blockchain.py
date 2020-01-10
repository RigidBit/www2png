"""
Blockchain related functions.
"""

import json
import mimetypes
import os
import requests

def generate_screenshot_block(screenshot_filename):
	"""Generate a new RigidBit block using the provided screenshot."""
	content_type = mimetypes.guess_type(screenshot_filename)[0]
	rburl = os.getenv("RIGIDBIT_BASE_URL") + "/api/file"
	rbdata = {"file0": (screenshot_filename, open(screenshot_filename, "rb"), content_type), "store_hash_only": "true"}
	headers = {"api_key": os.getenv("RIGIDBIT_API_KEY")}
	r = requests.post(rburl, files=rbdata, headers=headers)
	r.raise_for_status()
	block = json.loads(r.text)
	return block
