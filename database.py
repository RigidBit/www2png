from psycopg2 import sql
import os
import psycopg2
import psycopg2.extras
import time

def connect():
	return psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))

def check_data_uuid_exists(connection, uuid):
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) FROM data WHERE uuid=%s", (uuid,))
	return cursor.fetchone()[0] >= 1

def check_unverified_user_challenge_exists(connection, challenge):
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) FROM unverified_users WHERE challenge=%s", (challenge,))
	return cursor.fetchone()[0] >= 1

def check_user_email_exists(connection, email):
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) FROM users WHERE email=%s", (email,))
	return cursor.fetchone()[0] >= 1

def create_api_key_record(connection, data):
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO api_keys ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_data_record(connection, data):
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO data ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_unverified_user_record(connection, data):
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO unverified_users ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def create_user_record(connection, data):
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO users ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return cursor.fetchone()[0]

def delete_api_key_record_by_user_id(connection, user_id):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("DELETE FROM api_keys WHERE user_id=%s RETURNING *;", (user_id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def delete_unverified_user_record(connection, id):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("DELETE FROM unverified_users WHERE id=%s RETURNING *;", (id,))
	record = cursor.fetchone()
	return dict(record) if record is not None else None

def get_data_record(connection, id):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE id=%s", (id,))
	return dict(cursor.fetchone())

def get_data_record_by_uuid(connection, uuid):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE uuid=%s", (uuid,))
	return dict(cursor.fetchone())

def get_unverified_user_record_by_challenge(connection, challenge):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM unverified_users WHERE challenge=%s", (challenge,))
	return dict(cursor.fetchone())

def get_user_record_by_email(connection, email):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
	return dict(cursor.fetchone())

def update_data_record(connection, id, data):
	query = sql.SQL("UPDATE data SET {} WHERE id={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(id))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return id

def update_data_record_by_uuid(connection, uuid, data):
	query = sql.SQL("UPDATE data SET {} WHERE uuid={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(uuid))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	return uuid

def get_expired_data_records(connection, delay):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE timestamp < NOW() - INTERVAL '%s seconds' AND pruned=false ORDER BY id", (delay,))
	return cursor.fetchall()

def get_expired_unverified_user_records(connection, delay):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM unverified_users WHERE timestamp < NOW() - INTERVAL '%s seconds' ORDER BY id", (delay,))
	return cursor.fetchall()
