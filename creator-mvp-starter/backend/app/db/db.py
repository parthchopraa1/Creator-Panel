import os
import psycopg
from ..core.config import settings

def get_conn():
    if not settings.DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg.connect(settings.DATABASE_URL, autocommit=True)

def create_user_if_missing(email: str):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into users (email) values (%s) on conflict (email) do nothing", (email,))

def insert_connector(user_email: str, platform: str, access_enc: str, refresh_enc: str|None, scopes_json: dict):
    with get_conn() as conn:
        with conn.cursor() as cur:
            # find user id
            cur.execute("select id from users where email=%s", (user_email,))
            row = cur.fetchone()
            if not row:
                raise RuntimeError("User not found; ensure create_user_if_missing was called")
            user_id = row[0]
            cur.execute(
                "insert into connectors (user_id, platform, access_token_enc, refresh_token_enc, scopes) values (%s,%s,%s,%s,%s)",
                (user_id, platform, access_enc, refresh_enc, scopes_json)
            )
