"""
Decorators for the web and API endpoints.
"""

from flask import request
from functools import wraps
import json
import os

import database as db

def admin_required(func):
	"""Guard to ensure a valid admin password is provided."""
	def wrapper(*args, **kwargs):
		if not request.authorization or request.authorization.password != os.getenv("WWW2PNG_ADMIN_PASSWORD"):
			return ("Could not authenticate!", 401, {"WWW-Authenticate": "Basic realm=\"Login Required\""})
		return func(*args, **kwargs)
	wrapper.__name__ = func.__name__
	return wrapper

def api_key_required(func):
	"""Guard to ensure a valid API key is provided."""
	@wraps(func)
	def wrapper(api_key, *args, **kwargs):
		connection = db.connect()
		if not db.check_api_key_exists(connection, api_key):
			return ({"error": "Invalid API Key provided."}, 403)
		return func(api_key, *args, **kwargs)
	wrapper.__name__ = func.__name__
	return wrapper

def request_id_required(func):
	"""Guard to ensure a valid Request ID is provided."""
	@wraps(func)
	def wrapper(request_id, *args, **kwargs):
		connection = db.connect()
		if not db.get_data_record_by_request_id(connection, request_id):
			return ({"error": "Request ID is not valid."}, 404)
		return func(request_id, *args, **kwargs)
	wrapper.__name__ = func.__name__
	return wrapper

def api_key_and_request_id_required(func):
	"""Guard to ensure a valid API key and Request ID are provided."""
	@wraps(func)
	def wrapper(api_key, request_id, *args, **kwargs):
		connection = db.connect()
		if not db.check_api_key_exists(connection, api_key):
			return ({"error": "Invalid API Key provided."}, 403)
		if not db.get_data_record_by_request_id(connection, request_id):
			return ({"error": "Request ID is not valid."}, 404)
		return func(api_key, request_id, *args, **kwargs)
	wrapper.__name__ = func.__name__
	return wrapper
