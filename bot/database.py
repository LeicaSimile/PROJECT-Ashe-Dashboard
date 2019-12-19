import psycopg2
import settings

def setup():
    try:
        conn = psycopg2.connect(settings.DATABASE_URL, sslmode="require")
        cur = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS Inactive_Member (
            inactive_member_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            last_notified TIMESTAMPTZ NULL,
            is_exempt BOOLEAN NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS Default_Config (
            default_config_id SERIAL PRIMARY KEY,
            config_key VARCHAR(32) NOT NULL,
            config_value VARCHAR NULL
        );

        CREATE TABLE IF NOT EXISTS Guild_Config (
            guild_config_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            config_key VARCHAR(32) NOT NULL,
            config_value VARCHAR NULL
        );

        CREATE TABLE IF NOT EXISTS Permission (
            permission_id PRIMARY KEY,
            permission_name VARCHAR(32)
        );

        CREATE TABLE IF NOT EXISTS Guild_Permission (
            guild_permission_id SERIAL PRIMARY KEY,
            guild_id INTEGER NOT NULL,
            role_id INTEGER NOT NULL,
            permissions SMALLINT NOT NULL
        );
        """

def get_config_value(value):
    return

def get_inactive_members():
    return

def update_inactive_members():
    pass
