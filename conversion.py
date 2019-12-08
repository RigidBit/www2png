import datetime
import json
import os

def data_record_to_web_view(data):
	if data["pruned"]:
		data["status"] = "pruned"
	elif data["removed"]:
		data["status"] = "removed"
	elif data["queued"]:
		data["status"] = "pending"
	else:
		data["status"] = "available"
	data["screenshot_available"] = data["queued"] == False and data["removed"] == False and data["pruned"] == False
	data["proof_available"] = True if int((datetime.datetime.now() - data["timestamp"]).total_seconds()) > int(os.getenv("RIGIDBIT_PROOF_DELAY")) else False
	data["timestamp"] = int(data["timestamp"].timestamp())
	return data

def html_dirs():
	data = {}
	data["image_dir"] = os.getenv("WWW2PNG_IMAGE_DIR")
	data["style_dir"] = os.getenv("WWW2PNG_STYLE_DIR")
	return data

def screenshot_settings(form_values):
	defaults = json.loads(os.getenv("WWW2PNG_SCREENSHOT_SETTINGS_DEFAULT"))

	settings = {}
	settings.update(defaults)
	settings.update(form_values)

	settings["delay"] = min(int(settings["delay"]), settings["maxDelay"])
	settings["height"] = min(list(map(int, settings["resolution"].split("x")))[1], list(map(int, settings["maxResolution"].split("x")))[1])
	settings["width"] = min(list(map(int, settings["resolution"].split("x")))[0], list(map(int, settings["maxResolution"].split("x")))[0])
	settings["maxHeight"] = list(map(int, settings["maxResolution"].split("x")))[1]
	settings["maxWidth"] = list(map(int, settings["maxResolution"].split("x")))[0]
	settings["full_page"] = settings["full_page"] == "true" or settings["full_page"] == "True" or settings["full_page"] == "1" or settings["full_page"] == True

	return settings
