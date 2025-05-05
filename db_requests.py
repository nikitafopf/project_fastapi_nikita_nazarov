import psycopg2
import json


def get_db_connection() -> psycopg2.extensions.connection:
    with open("config.json") as f:
        conf = json.load(f)
    DATABASE = conf["DATABASE"]
    USER = conf["USER"]
    PASSWORD = conf["PASSWORD"]
    HOST = conf["HOST"]
    PORT = conf["PORT"]
    conn = psycopg2.connect(
        dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    return conn


def get_all_notes(cur: psycopg2.extensions.cursor) -> list[tuple]:
    cur.execute("select * from Notes")
    return cur.fetchall()

def add_new_note(conn: psycopg2.extensions.connection, name: str, note: str) -> None:
    cur  = conn.cursor()
    cur.execute("insert into notes(name, note) values (%s, %s)", (name, note))
    conn.commit()


def get_note(cur: psycopg2.extensions.cursor) -> dict:
    notes = {}
    for name, note in get_all_notes(cur):
        notes[name] = note
    return notes