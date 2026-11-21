"""
RecruitTrack ATS - Database Connection Layer
CIS 407 - Database Management Systems
Handles PostgreSQL 14 connections, query execution, transactions, and security.
"""

import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union
import bcrypt
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


def get_db_config() -> Dict[str, Any]:
    """
    Retrieve database configuration from Streamlit secrets or environment variables.
    Never hardcodes sensitive credentials.
    """
    config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "4919")),
        "database": os.getenv("DB_NAME", "recruittrack_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", os.getenv("PGPASSWORD", "")),
        "connect_timeout": int(os.getenv("DB_TIMEOUT", "5")),
    }

    # Attempt to load from streamlit secrets if running inside Streamlit
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "postgres" in st.secrets:
            pg_secrets = st.secrets["postgres"]
            config["host"] = pg_secrets.get("host", config["host"])
            config["port"] = int(pg_secrets.get("port", config["port"]))
            config["database"] = pg_secrets.get("database", config["database"])
            config["user"] = pg_secrets.get("user", config["user"])
            config["password"] = pg_secrets.get("password", config["password"])
    except Exception:
        pass

    return config


def get_connection():
    """
    Establish and return a new PostgreSQL connection.
    Raises psycopg2.Error with helpful diagnostic messages.
    """
    config = get_db_config()
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=config["database"],
            user=config["user"],
            password=config["password"],
            connect_timeout=config["connect_timeout"],
        )
        return conn
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "authentication failed" in error_msg.lower():
            raise RuntimeError(
                f"PostgreSQL authentication failed for user '{config['user']}'. "
                f"Please verify DB_PASSWORD in your .env or environment on port {config['port']}."
            ) from e
        elif "connection refused" in error_msg.lower() or "is the server running" in error_msg.lower():
            raise RuntimeError(
                f"Could not connect to PostgreSQL on {config['host']}:{config['port']}. "
                f"Please ensure PostgreSQL is running and port {config['port']} is correct."
            ) from e
        else:
            raise RuntimeError(f"Database operational error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected database connection failure: {e}") from e


def test_connection() -> Tuple[bool, str]:
    """
    Test database connectivity using a basic 'SELECT 1;' query.
    Returns (True, success_message) or (False, error_message).
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()
        conn.close()
        if result and result[0] == 1:
            config = get_db_config()
            return True, f"Successfully connected to {config['database']} on {config['host']}:{config['port']}."
        return False, "Query executed but returned unexpected result."
    except Exception as e:
        return False, str(e)


@contextmanager
def get_db_cursor(commit: bool = False):
    """
    Context manager providing a database cursor with automatic cleanup,
    commit on success (if requested), and rollback on exception.
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(
    query: str,
    params: Optional[Union[Tuple, Dict, List]] = None,
    fetch: bool = True,
    commit: bool = False,
) -> Union[List[Dict[str, Any]], int]:
    """
    Execute a parameterized SQL query safely.
    - If fetch=True, returns rows as a list of dictionaries.
    - If fetch=False, returns the affected rowcount.
    - If commit=True, commits the transaction.
    """
    with get_db_cursor(commit=commit) as cur:
        if params is not None:
            cur.execute(query, params)
        else:
            cur.execute(query)
        if fetch:
            try:
                rows = cur.fetchall()
                return [dict(row) for row in rows]
            except psycopg2.ProgrammingError:
                # Query does not produce result rows (e.g. DDL or DML without RETURNING)
                return []
        return cur.rowcount


def execute_procedure(procedure_name: str, params: Optional[Tuple] = None) -> None:
    """
    Execute a PostgreSQL stored procedure using 'CALL procedure_name(%s, ...);'.
    Safely commits the transaction.
    """
    placeholders = ", ".join(["%s"] * len(params)) if params else ""
    call_sql = f"CALL {procedure_name}({placeholders});"
    with get_db_cursor(commit=True) as cur:
        cur.execute(call_sql, params or ())


# =========================================================
# AUTHENTICATION & PASSWORD HASHING UTILITIES
# =========================================================

def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt with salt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    if not hashed_password or not plain_password:
        return False
    # If the database still has placeholder hashes (e.g. DEMO_HASH_001), do not authenticate
    if hashed_password.startswith("DEMO_HASH_"):
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False
