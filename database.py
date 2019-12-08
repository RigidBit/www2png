from psycopg2 import sql
import os
import psycopg2
import psycopg2.extras
import time

def connect():
	return psycopg2.connect(dbname=os.getenv("POSTGRESQL_DB"), host=os.getenv("POSTGRESQL_HOST"), port=os.getenv("POSTGRESQL_PORT"), user=os.getenv("POSTGRESQL_USER"), password=os.getenv("POSTGRESQL_PASS"))

def create_data_record(connection, data):
	keys = list(data.keys())
	values = list(map(str, data.values()))
	query = sql.SQL("INSERT INTO data ({}) VALUES ({}) RETURNING id;").format(sql.SQL(", ").join(map(sql.Identifier, keys)), sql.SQL(", ").join(map(sql.Literal, values)))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	connection.commit()
	return cursor.fetchone()[0]

def get_data_record(connection, id):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE id=%s", (id,))
	return dict(cursor.fetchone())

def get_data_record_by_uuid(connection, uuid):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE uuid=%s", (uuid,))
	return dict(cursor.fetchone())

def update_data_record(connection, id, data):
	query = sql.SQL("UPDATE data SET {} WHERE id={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(id))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	connection.commit()
	return id

def update_data_record_by_uuid(connection, uuid, data):
	query = sql.SQL("UPDATE data SET {} WHERE uuid={};").format(sql.SQL(", ").join(map(lambda kv: sql.SQL("{}={}").format(sql.Identifier(kv[0]), sql.Literal(kv[1])), data.items())), sql.Literal(uuid))
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)	
	cursor.execute(query)
	connection.commit()
	return uuid

def get_expired_data_records(connection, delay):
	cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cursor.execute("SELECT * FROM data WHERE timestamp < NOW() - INTERVAL '%s seconds' AND pruned=false ORDER BY id", (delay,))
	return cursor.fetchall()
