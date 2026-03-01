"""Database connection helper using mysql-connector-python.

Centralises connection creation so every DAO can reuse it.
"""

from __future__ import annotations

import mysql.connector
from mysql.connector.connection import MySQLConnection

# Default connection parameters — override via environment or settings.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "201204",          # ← set your password
    "database": "smart_inventory",
    "charset": "utf8mb4",
    "autocommit": False,
}


def get_connection(**overrides) -> MySQLConnection:
    """Return a new MySQL connection.

    Any keyword argument overrides the defaults in *DB_CONFIG*.
    """
    config = {**DB_CONFIG, **overrides}
    return mysql.connector.connect(**config)
