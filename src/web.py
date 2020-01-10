"""
Primary program logic for all web and API endpoints.
"""

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, send_from_directory, Response, redirect
from uuid import uuid4
import datetime
import greenstalk
import json
import mimetypes
import os
import requests

from decorators import api_key_required, api_key_and_request_id_required
import misc
import database as db
import validation as v

##### ENTRY POINT #####

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

##### STATIC ROUTES #####

@app.route("/api/help", methods=["GET"])
def api_help():
	"""Web endpoint for API Help page."""
	data = {"base_url": os.getenv("WWW2PNG_BASE_URL")}
	return render_template("api_help.html", page_title=misc.page_title("api_help"), data=data)

@app.route("/contact", methods=["GET"])
def contact():
	"""Web endpoint for Contact page."""
	return render_template("contact.html", page_title=misc.page_title("contact"))

@app.route("/ping", methods=["GET"])
def ping():
	"""Web endpoint for testing connectivity. This is good for uptime checkers."""
	connection = db.connect()
	db.check_api_key_exists(connection, "")
	return "Pong!"

@app.route("/terms_of_service", methods=["GET"])
def terms_of_service():
	"""Web endpoint for the Terms of Service page."""
	return render_template("terms_of_service.html", page_title=misc.page_title("tos"))

@app.route("/privacy_policy", methods=["GET"])
def privacy_policy():
	"""Web endpoint for the Privacy Policy page."""
	return render_template("privacy_policy.html", page_title=misc.page_title("pp"))

##### DYNAMIC API ROUTES #####

@app.route("/api/capture/<api_key>", methods=["GET"])
@api_key_required
def api_capture(api_key):
	"""API endpoint for capturing a new screenshot."""
	connection = db.connect()
	db.lock_data_table(connection)
	queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), use=os.getenv("GREENSTALK_TUBE_QUEUE"))
	form = v.CaptureForm(request.values)
	if form.validate():
		request_id = str(uuid4())
		settings = misc.screenshot_settings(request.values)
		user_id = db.get_api_key_record_by_api_key(connection, api_key)["user_id"]
		if db.check_pending_request(connection, settings["url"], user_id):
			return json.dumps({"error": "A request for this exact URL is currently pending."}), 429
		data = {"request_id": request_id, "url": settings["url"], "block_id": 0, "user_id": user_id, "queued": "true", "pruned": "false", "flagged": "false", "removed": "false", "failed": "false"}
		db.create_data_record(connection, data)
		db.update_api_key_use_count(connection, api_key)
		connection.commit()
		payload = {"request_id": request_id, "settings": settings}
		queue.put(json.dumps(payload), ttr=int(os.getenv("WWW2PNG_PROCESSING_TTR")))
		payload = {
			"request_id": request_id,
			"status_url": f"""{os.getenv("WWW2PNG_BASE_URL")}/api/status/{api_key}/{request_id}""",
			"image_url": f"""{os.getenv("WWW2PNG_BASE_URL")}/api/image/{api_key}/{request_id}""",
			"proof_url": f"""{os.getenv("WWW2PNG_BASE_URL")}/api/proof/{api_key}/{request_id}""",
		}
		return (json.dumps(payload), 200)
	else:
		for key in form.errors:
			return json.dumps({"error": form.errors[key][0]}), 400

@app.route("/api/image/<api_key>/<request_id>", methods=["GET"])
@api_key_and_request_id_required
def api_image(api_key, request_id):
	"""API endpoint for requesting an image once it is available."""
	connection = db.connect()
	data = db.get_data_record_by_request_id(connection, request_id)
	if data["queued"]:
		return (json.dumps({"error": "Request ID is valid, but image is not yet available."}), 202)
	elif data["removed"] or data["pruned"]:
		return (json.dumps({"error": "Image not available."}), 410)
	else:
		filename = request_id+".png"
		as_attachment = "download" in request.values and request.values["download"] == "true"
		return send_from_directory(os.getenv("WWW2PNG_SCREENSHOT_DIR"), filename, mimetype=mimetypes.guess_type(filename)[0], as_attachment=as_attachment)

@app.route("/api/proof/<api_key>/<request_id>", methods=["GET"])
@api_key_and_request_id_required
def api_proof(api_key, request_id):
	"""API endpoint to download a blockchain proof once available."""
	connection = db.connect()
	data_record = db.get_data_record_by_request_id(connection, request_id)
	proof_available = True if int((datetime.datetime.now() - data_record["timestamp"]).total_seconds()) > int(os.getenv("RIGIDBIT_PROOF_DELAY")) else False
	if proof_available:
		headers = {"api_key": os.getenv("RIGIDBIT_API_KEY")}
		url = os.getenv("RIGIDBIT_BASE_URL") + "/api/trace-block/" + str(data_record["block_id"])
		content = requests.get(url, headers=headers).content
		return Response(content, mimetype="application/json", headers={"Content-disposition": f"attachment; filename={request_id}.json"})
	else:
		return json.dumps({"error": "Request ID is valid, but proof is not yet available."}), 202

@app.route("/api/status/<api_key>/<request_id>", methods=["GET"])
@api_key_and_request_id_required
def api_status(api_key, request_id):
	"""API endpoint for checking the status of an existing capture."""
	connection = db.connect()
	if not db.check_api_key_exists(connection, api_key):
		return (json.dumps({"error": "Invalid API Key provided."}), 403)
	data = db.get_data_record_by_request_id(connection, request_id)
	if data == None:
		return (json.dumps({"error": "Invalid Request ID provided."}), 404)
	payload = misc.data_record_to_api_status(data)
	return (json.dumps(payload), 200)

@app.route("/api/request", methods=["POST"])
def api_request():
	"""API endpoint to register a user and request a new API key."""
	connection = db.connect()
	actions = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), use=os.getenv("GREENSTALK_TUBE_ACTIONS"))
	form = v.ApiKeyForm()
	if form.validate_on_submit():
		challenge = str(uuid4())
		email = request.values["email"]
		data = {"email": email, "challenge": challenge}
		db.create_unverified_user_record(connection, data)
		connection.commit()
		data = {"email": email, "challenge": challenge}
		payload = {"action": "send_api_request_email", "data": data}
		actions.put(json.dumps(payload), ttr=int(os.getenv("WWW2PNG_PROCESSING_TTR")))
		return render_template("web_api_key_requested.html", page_title=misc.page_title("api_request"), data=data)
	else:
		for key in form.errors:
			return json.dumps({"error": form.errors[key][0]}), 400

@app.route("/api/activate/<api_key>", methods=["GET"])
def api_activate(api_key):
	"""API endpoint to activate an API key."""
	connection = db.connect()
	record = db.get_unverified_user_record_by_challenge(connection, api_key)
	if record != None:
		db.delete_unverified_user_record(connection, record["id"])
		user_record = db.get_user_record_by_email(connection, record["email"])
		if user_record != None:
			user_id = user_record["id"]
		else:
			data = {"email": record["email"], "disabled": False}
			user_id = db.create_user_record(connection, data)
		data = {"email": record["email"], "api_key": api_key}
		db.delete_api_key_record_by_user_id(connection, user_id)
		data = {"api_key": api_key, "user_id": user_id}
		db.create_api_key_record(connection, data)
		connection.commit()
		data = {"api_key": api_key, "base_url": os.getenv("WWW2PNG_BASE_URL")}
		return render_template("web_api_key_activated.html", page_title=misc.page_title("api_activate"), data=data)
	else:
		data = {"header": "ERROR", "error": "The API Key you specified is not valid or has already been activated."}
		return render_template("error.html", page_title=misc.page_title("error"), data=data)

@app.route("/web/buried", methods=["GET", "POST"])
def web_buried():
	"""Web endpoint for viewing buried entries."""
	queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), use=os.getenv("GREENSTALK_TUBE_QUEUE"))
	form = v.BuriedForm()
	if form.validate_on_submit():
		try:
			print(form.data)
			if form.data["action"] == "delete" and form.data["job_id"] is not None:
				queue.delete(form.data["job_id"])
			elif form.data["action"] == "kick" and form.data["job_id"] is not None:
				queue.kick_job(form.data["job_id"])
		except greenstalk.NotFoundError:
			return redirect("/buried", code=302)
	try:
		job = queue.peek_buried()
		data = {"job_body": job.body, "job_id": job.id}
	except greenstalk.NotFoundError:
		data = {}
	return render_template("buried.html", page_title=misc.page_title("buried"), data=data)

@app.route("/web/capture", methods=["POST"])
def web_capture():
	"""Web endpoint to capture a new screenshot."""
	connection = db.connect()
	db.lock_data_table(connection)
	queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), use=os.getenv("GREENSTALK_TUBE_QUEUE"))
	form = v.CaptureForm()
	if form.validate_on_submit():
		request_id = str(uuid4())
		settings = misc.screenshot_settings(request.values)
		data = {"request_id": request_id, "url": settings["url"], "block_id": 0, "user_id": 1, "queued": "true", "pruned": "false", "flagged": "false", "removed": "false", "failed": "false"}
		db.create_data_record(connection, data)
		connection.commit()
		payload = {"request_id": request_id, "settings": settings}
		queue.put(json.dumps(payload), ttr=int(os.getenv("WWW2PNG_PROCESSING_TTR")))
		return redirect("/web/view/"+request_id, code=303)
	else:
		for key in form.errors:
			return render_template("error.html", page_title=misc.page_title("500"), data={"header": "Error", "error": f"""{key}: {form.errors[key][0]}"""}), 400

@app.route("/web/image/<request_id>", methods=["GET"])
def web_image(request_id):
	"""Web endpoint to download an image once available."""
	connection = db.connect()
	data = db.get_data_record_by_request_id(connection, request_id)
	if data == None or data["removed"] or data["pruned"] or data["queued"]:
		return render_template("error.html", page_title=misc.page_title("404"), data={"header": "404", "error": f"""Request ID not found: {request_id}"""}), 404
	else:
		filename = request_id+".png"
		as_attachment = "download" in request.values and request.values["download"] == "true"
		return send_from_directory(os.getenv("WWW2PNG_SCREENSHOT_DIR"), filename, mimetype=mimetypes.guess_type(filename)[0], as_attachment=as_attachment)

@app.route("/web/proof/<request_id>", methods=["GET"])
def web_proof(request_id):
	"""Web endpoint to download a blockchain proof once available."""
	connection = db.connect()
	data_record = db.get_data_record_by_request_id(connection, request_id)
	if data_record != None:
		proof_available = True if int((datetime.datetime.now() - data_record["timestamp"]).total_seconds()) > int(os.getenv("RIGIDBIT_PROOF_DELAY")) else False
		if proof_available:
			headers = {"api_key": os.getenv("RIGIDBIT_API_KEY")}
			url = os.getenv("RIGIDBIT_BASE_URL") + "/api/trace-block/" + str(data_record["block_id"])
			content = requests.get(url, headers=headers).content
			return Response(content, mimetype="application/json", headers={"Content-disposition": f"attachment; filename={request_id}.json"})
	return render_template("error.html", page_title=misc.page_title("404"), data={"header": "404", "error": f"""Request ID not found: {request_id}"""}), 404

@app.route("/web/stats", methods=["GET"])
def web_stats():
	"""Web endpoint to view site stats."""
	connection = db.connect()
	data = \
	{
		"count": db.get_data_record_count(connection)["count"],
		"count_api_keys": db.get_api_key_count(connection)["count"],
		"count_users": db.get_user_count(connection)["count"],
		"recent": db.get_recent_data_records(connection, 100),
		"api_key_use_counts": db.get_api_key_use_counts(connection)
	}
	return render_template("web_stats.html", page_title=misc.page_title("Count"), data=data)

@app.route("/web/view/<request_id>", methods=["GET"])
def web_view(request_id):
	"""Web endpoint to view the status and content of a request."""
	connection = db.connect()
	data = db.get_data_record_by_request_id(connection, request_id)
	if data != None:
		data = misc.data_record_to_web_view(data)
		data["base_url"] = os.getenv("WWW2PNG_BASE_URL")
		return render_template("web_view.html", page_title="WWW2PNG - Webpage Screenshot Service with Blockchain Anchoring", data=data)
	else:
		return render_template("error.html", page_title=misc.page_title("404"), data={"header": "404", "error": f"""Request ID not found: {request_id}"""}), 404

@app.route("/", methods=["GET"])
def root():
	"""Web endpoint for the landing page."""
	return render_template("index.html", page_title=misc.page_title("default"))

if __name__ == "__main__":
	app.run(host="0.0.0.0")
