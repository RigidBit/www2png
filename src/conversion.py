import datetime
import json
import os

def data_record_to_api_status(data):
	"""Convert a data record to and API status record."""
	data_web_view = data_record_to_web_view(data)
	data = {
		"request_id": data["request_id"],
		"url": data["url"],
		"status": data_web_view["status"],
		"screenshot_available": data_web_view["screenshot_available"],
		"proof_available": data_web_view["proof_available"],
		"timestamp": data["timestamp"],
		"prune_timestamp": data["prune_timestamp"]
	}
	return data

def data_record_to_web_view(data):
	"""Convert a data record into a web view record."""
	if data["failed"]:
		data["status"] = "failed"
	elif data["removed"]:
		data["status"] = "removed"
	elif data["queued"]:
		data["status"] = "pending"
	elif data["pruned"]:
		data["status"] = "pruned"
	else:
		data["status"] = "available"
	data["screenshot_available"] = data["status"] == "available"
	data["proof_available"] = True if int((datetime.datetime.now() - data["timestamp"]).total_seconds()) > int(os.getenv("RIGIDBIT_PROOF_DELAY")) else False
	data["timestamp"] = int(data["timestamp"].timestamp())
	data["prune_timestamp"] = data["timestamp"] + int(os.getenv("WWW2PNG_SCREENSHOT_PRUNE_DELAY"))
	return data

def html_dirs():
	"""Determine the required HTML directories."""
	data = {}
	data["image_dir"] = os.getenv("WWW2PNG_IMAGE_DIR")
	data["style_dir"] = os.getenv("WWW2PNG_STYLE_DIR")
	return data

def screenshot_settings(form_values):
	"""Generate the screenshot settings."""
	defaults = json.loads(os.getenv("WWW2PNG_SCREENSHOT_SETTINGS_DEFAULT"))

	settings = {}
	settings.update(defaults)
	settings.update(form_values)

	settings["delay"] = min(int(settings["delay"]), settings["maxDelay"])
	settings["height"] = min(list(map(int, settings["resolution"].split("x")))[1], list(map(int, settings["maxResolution"].split("x")))[1])
	settings["height"] = max(settings["height"], list(map(int, settings["minResolution"].split("x")))[1])
	settings["width"] = min(list(map(int, settings["resolution"].split("x")))[0], list(map(int, settings["maxResolution"].split("x")))[0])
	settings["width"] = max(settings["width"], list(map(int, settings["minResolution"].split("x")))[0])
	settings["maxHeight"] = list(map(int, settings["maxResolution"].split("x")))[1]
	settings["maxWidth"] = list(map(int, settings["maxResolution"].split("x")))[0]
	settings["full_page"] = settings["full_page"] == "true" or settings["full_page"] == "True" or settings["full_page"] == "1" or settings["full_page"] == True

	return settings

def page_title(id):
	"""Determine the page title."""
	switcher = {
		"404": "Error 404: Not Found - WWW2PNG",
		"api_activate": "API Key Activated - WWW2PNG",
		"api_help": "API Help - WWW2PNG",
		"api_request": "API Key Requested - WWW2PNG",
		"buried": "Manage Buried - WWW2PNG",
		"contact": "Contact Us - WWW2PNG",
		"default": "Free Webpage Screenshot Service API with Blockchain Anchoring - WWW2PNG",
		"error": "Error - WWW2PNG",
		"pp": "Privacy Policy - WWW2PNG",
		"tos": "Terms of Service - WWW2PNG",
	}
	return switcher.get(id, "WWW2PNG")
