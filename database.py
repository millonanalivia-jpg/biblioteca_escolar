import os
import sqlite3
from contextlib import contextmanager

CAMINHO_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "biblioteca.db")
CAMINHO_SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema.sql")


def get_conexao():
    conn = sqlite3.connect(CAMINHO_BD)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def conexao():
    """Abre a conexão, faz commit se der certo, rollback se der erro e sempre fecha."""
    conn = get_conexao()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def criar_tabelas():
    """Cria as tabelas executando o schema.sql."""
    with open(CAMINHO_SCHEMA, encoding="utf-8") as f:
        script = f.read()
    conn = get_conexao()
    conn.executescript(script)
    conn.commit()
    conn.close()
