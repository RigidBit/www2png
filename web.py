from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, send_from_directory, Response, redirect
import datetime
import greenstalk
import json
import mimetypes
import os
import requests
import uuid as UUID

import conversion as conv
import database as db
import validation as v

##### ENTRY POINT #####

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
queue = greenstalk.Client(host=os.getenv("GREENSTALK_HOST"), port=os.getenv("GREENSTALK_PORT"), use=os.getenv("GREENSTALK_TUBE_QUEUE"))

##### STATIC ROUTES #####

@app.route("/ping", methods=["GET"])
def ping():
	db.connect()
	return "Pong!"

@app.route("/contact", methods=["GET"])
def contact():
	dirs = conv.html_dirs()
	return render_template("contact.html", page_title="WWW2PNG - Webpage Screenshot Service with Blockchain Anchoring", dirs=dirs)

@app.route("/terms_of_service", methods=["GET"])
def terms_of_service():
	dirs = conv.html_dirs()
	return render_template("terms_of_service.html", page_title="WWW2PNG - Terms of Service", dirs=dirs)

@app.route("/privacy_policy", methods=["GET"])
def privacy_policy():
	dirs = conv.html_dirs()
	return render_template("privacy_policy.html", page_title="WWW2PNG - Privacy Policy", dirs=dirs)

##### DYNAMIC ROUTES #####

@app.route("/web/buried", methods=["GET"])
@app.route("/web/buried/<action>/<int:job_id>", methods=["GET"])
def web_buried(action=None, job_id=None):
	try:
		if action == "delete" and job_id is not None:
			queue.delete(job_id)
		elif action == "kick" and job_id is not None:
			queue.kick_job(job_id)
	except greenstalk.NotFoundError:
		return redirect("/web/buried", code=302)
	try:
		job = queue.peek_buried()
		data = {"job_body": job.body, "job_id": job.id}
	except greenstalk.NotFoundError:
		data = {}
	dirs = conv.html_dirs()
	return render_template("buried.html", page_title="WWW2PNG - Manage Buried", data=data, dirs=dirs)

@app.route("/web/capture", methods=["POST"])
def web_capture():
	connection = db.connect()
	form = v.CaptureForm()
	if form.validate_on_submit():
		uuid = str(UUID.uuid4())
		settings = conv.screenshot_settings(request.values)
		data = {"uuid": uuid, "url": settings["url"], "block_id": 0, "user_id": 1, "queued": "true", "pruned": "false", "flagged": "false", "removed": "false"}
		db.create_data_record(connection, data)
		payload = {"uuid": uuid, "settings": settings}
		queue.put(json.dumps(payload))
		return redirect("/web/view/"+uuid, code=303)
	else:
		for key in form.errors:
			raise ValueError(f"{key}: {form.errors[key][0]}")

@app.route("/web/image/<uuid>", methods=["GET"])
def web_image(uuid):
	connection = db.connect()
	data = db.get_data_record_by_uuid(connection, uuid)
	if data["removed"] or data["pruned"] or data["queued"]:
		dirs = conv.html_dirs()
		return render_template("404.html", page_title="WWW2PNG - Error 404: Not Found", data={"uuid": uuid}, dirs=dirs), 404
	else:
		filename = uuid+".png"
		return send_from_directory(os.getenv("WWW2PNG_SCREENSHOT_DIR"), filename, mimetype=mimetypes.guess_type(filename)[0])

@app.route("/web/proof/<uuid>", methods=["GET"])
def web_proof(uuid):
	connection = db.connect()
	exists = db.check_data_uuid_exists(connection, uuid)
	if exists:
		data_record = db.get_data_record_by_uuid(connection, uuid)
		proof_available = True if int((datetime.datetime.now() - data_record["timestamp"]).total_seconds()) > int(os.getenv("RIGIDBIT_PROOF_DELAY")) else False
		if proof_available:
			headers = {"api_key": os.getenv("RIGIDBIT_API_KEY")}
			url = os.getenv("RIGIDBIT_BASE_URL") + "/api/trace-block/" + str(data_record["block_id"])
			content = requests.get(url, headers=headers).content
			return Response(content, mimetype="application/json", headers={"Content-disposition": f"attachment; filename={uuid}.json"})
	dirs = conv.html_dirs()
	return render_template("404.html", page_title="WWW2PNG - Error 404: Not Found", data={"uuid": uuid}, dirs=dirs), 404

@app.route("/web/view/<uuid>", methods=["GET"])
def web_view(uuid):
	connection = db.connect()
	dirs = conv.html_dirs()
	exists = db.check_data_uuid_exists(connection, uuid)
	if exists:
		data = db.get_data_record_by_uuid(connection, uuid)
		data = conv.data_record_to_web_view(data)
		return render_template("web_view.html", page_title="WWW2PNG - Webpage Screenshot Service with Blockchain Anchoring", dirs=dirs, data=data)
	else:
		return render_template("404.html", page_title="WWW2PNG - Error 404: Not Found", data={"uuid": uuid}, dirs=dirs), 404

@app.route("/", methods=["GET"])
def root():
	dirs = conv.html_dirs()
	form = v.CaptureForm()
	return render_template("index.html", page_title="WWW2PNG - Webpage Screenshot Service with Blockchain Anchoring", dirs=dirs, form=form)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
