"""
Database functions.
"""

from psycopg2 import sql
import os
import psycopg2
import psycopg2.extras
import time

def connect():
	"""Connect to the PostgreSQL database."""
	return psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))

def check_api_key_exists(connection, api_key):
	"""Check if an API key exists."""
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) FROM api_keys WHERE api_key=%s", (api_key,))
	return cursor.fetchone()[0] >= 1

def check_pending_request(connection, url, user_id):
	"""Check if a pending request exists."""
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) FROM data WHERE url=%s AND user_id=%s AND queued=true", (url, user_id))
	return cursor.fetchone()[0] >= 1

def create_api_key_record(connection, data):
	"""Create a new API Key record."""
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO api_keys ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_data_record(connection, data):
	"""Create a new data record."""
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO data ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_unverified_user_record(connection, data):
	"""Create a new unverified user record."""
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO unverified_users ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_user_record(connection, data):
	"""Create a new user record."""
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO users ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def delete_api_key_record_by_user_id(connection, user_id):
	"""Delete an API Key record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("DELETE FROM api_keys WHERE user_id=%s RETURNING *;", (user_id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def delete_unverified_user_record(connection, id):
	"""Delete an unverified user record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("DELETE FROM unverified_users WHERE id=%s RETURNING *;", (id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_data_record(connection, id):
	"""Retrieve a data record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE id=%s", (id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_api_key_count(connection):
	"""Retrieve the number of API key."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT COUNT(*) as count FROM api_keys;")
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_api_key_record_by_api_key(connection, api_key):
	"""Retrieve an API key record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM api_keys WHERE api_key=%s", (api_key,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_api_key_use_counts(connection):
	"""Retrieve the usage for the top API keys."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT api_key, user_id, email, use_count FROM api_keys LEFT JOIN users ON user_id=users.id ORDER BY use_count DESC LIMIT 50;")
	return cursor.fetchall()

def get_data_record_by_request_id(connection, request_id):
	"""Retrieve a data record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE request_id=%s", (request_id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_data_record_count(connection):
	"""Retrieve the number of data records."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT COUNT(*) as count FROM data;")
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_recent_data_records(connection, count):
	"""Retrieve the recent data records."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data ORDER BY id DESC LIMIT "+str(count))
	return cursor.fetchall()

def get_unverified_user_record_by_challenge(connection, challenge):
	"""Retrieve a unverified user record."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM unverified_users WHERE challenge=%s", (challenge,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_user_count(connection):
	"""Retrieve the number of users."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT COUNT(*) as count FROM users;")
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_user_record_by_email(connection, email):
	"""Retrieve a user record by email address."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def lock_data_table(connection):
	"""Lock the data table in exclusive mode."""
	cursor = connection.cursor()
	cursor.execute("BEGIN;")
	cursor.execute("LOCK TABLE data IN ACCESS EXCLUSIVE MODE;")

def update_api_key_use_count(connection, api_key):
	"""Update the API key use count by 1."""
	query = sql.SQL("UPDATE api_keys SET use_count=use_count+1 WHERE api_key={} RETURNING use_count;").format(sql.Literal(api_key))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def update_data_record(connection, id, data):
	"""Update a data record."""
	query = sql.SQL("UPDATE data SET {} WHERE id={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(id))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return id

def update_data_record_by_request_id(connection, request_id, data):
	"""Update a data record by the request ID."""
	query = sql.SQL("UPDATE data SET {} WHERE request_id={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(request_id))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return request_id

def get_expired_data_records(connection, delay):
	"""Retrieve all expired data records for pruning."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE timestamp < NOW() - INTERVAL '%s seconds' AND pruned=false ORDER BY id", (delay,))
	return cursor.fetchall()

def get_expired_unverified_user_records(connection, delay):
	"""Retrieve all expired unverified user records for deletion."""
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM unverified_users WHERE timestamp < NOW() - INTERVAL '%s seconds' ORDER BY id", (delay,))
	return cursor.fetchall()
