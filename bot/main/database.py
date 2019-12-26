from contextlib import contextmanager
import psycopg2
from psycopg2 import pool, sql
from main import settings

db_pool = pool.SimpleConnectionPool(1, 10, dsn=settings.DATABASE_URL, sslmode="require")

@contextmanager
def db():
    conn = db_pool.getconn()
    cur = conn.cursor()
    try:
        yield conn, cur
    finally:
        cur.close()
        db.putconn(conn)

def setup():
    with db() as (conn, cur):
        query = """CREATE SCHEMA IF NOT EXISTS core;
        
        CREATE TABLE IF NOT EXISTS core.Default_Config (
            default_config_id SMALLSERIAL PRIMARY KEY,
            config_key VARCHAR(30) NOT NULL,
            config_value VARCHAR NULL
        );

        CREATE TABLE IF NOT EXISTS core.Guild_Config (
            guild_config_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            config_key VARCHAR(30) NOT NULL,
            config_value VARCHAR NULL
        );

        CREATE TABLE IF NOT EXISTS core.Permission (
            permission_id SMALLINT PRIMARY KEY,
            permission_name VARCHAR(32)
        );

        CREATE TABLE IF NOT EXISTS core.Guild_Role_Permission (
            role_permission_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            permission_level SMALLINT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS core.Guild_Member_Permission (
            member_permission_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            permission_level SMALLINT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS core.Inactive_Member (
            inactive_member_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            last_notified TIMESTAMPTZ NULL,
            is_exempt BOOLEAN NOT NULL
        );
        """
        cur.execute(query)
        conn.commit()

def add_config_record(key, value):
    return

def get_config_value(key):
    return

def update_config_value(key, value):
    return

def delete_config_record(key):
    return

def get_all_inactive_members(guild_id):
    inactive_members = []
    with db() as (conn, cur):
        query = sql.SQL("""SELECT guild_id, member_id, last_notified, is_exempt
            FROM core.Inactive_Member WHERE guild_id = {}""".format(guild_id))
        cur.execute(query)
        inactive_members = cur.fetchall()

    return inactive_members

def get_inactive_members(guild_id):
    return

def get_exempt_inactive_members(guild_id):
    return

def update_inactive_member(guild_id, member_id, **kwargs):
    return

def add_inactive_member(guild_id, member_id):
    return
