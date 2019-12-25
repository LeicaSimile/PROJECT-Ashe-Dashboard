import psycopg2
from main import settings

def setup():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        query = """CREATE SCHEMA IF NOT EXISTS core
        
        CREATE TABLE IF NOT EXISTS core.Default_Config (
            default_config_id SERIAL PRIMARY KEY,
            config_key VARCHAR(32) NOT NULL,
            config_value VARCHAR NULL
        );

        CREATE TABLE IF NOT EXISTS core.Guild_Config (
            guild_config_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            config_key VARCHAR(32) NOT NULL,
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
    finally:
        if conn:
            cur.close()
            conn.close()

def add_config_record(key, value):
    return

def get_config_value(key):
    return

def update_config_value(key, value):
    return

def delete_config_record(key):
    return

def get_inactive_members():
    return

def update_inactive_members():
    return
