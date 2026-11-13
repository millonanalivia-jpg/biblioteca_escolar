"""Conexão com o banco de dados (SQLite).

Toda a configuração do banco fica aqui. Para trocar de SGBD (ex.: MySQL),
basta alterar get_connection() e init_db().
"""
import os
import sqlite3

DB_PATH = os.environ.get("BIBLIOTECA_DB", os.path.join(os.path.dirname(__file__), "biblioteca.db"))
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None):
    """Cria as tabelas caso ainda não existam."""
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        script = f.read()
    conn = get_connection(db_path)
    try:
        conn.executescript(script)
        conn.commit()
    finally:
        conn.close()
