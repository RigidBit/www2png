from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, send_from_directory, Response, redirect
from flask_scss import Scss
import database as db
import datetime
import greenstalk
import json
import mimetypes
import os
import requests

##### ENTRY POINT #####

load_dotenv()
app = Flask(__name__)
Scss(app, static_dir=os.getenv("WWW2PNG_STYLE_DIR"), asset_dir=os.getenv("WWW2PNG_STYLE_ASSET_DIR"))

@app.route("/ping", methods=["GET"])
def ping():
	db.connect()
	return "Pong!"

if __name__ == "__main__":
	app.run(host="0.0.0.0")
