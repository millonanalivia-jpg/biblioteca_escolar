from database import get_connection
from livro import Livro


class LivroDAO:
    def inserir(self, livro):
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO livro (titulo, autor, isbn, ano, quantidade_total, quantidade_disponivel)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (livro.titulo, livro.autor, livro.isbn, livro.ano,
                 livro.quantidade_total, livro.quantidade_disponivel))
            livro.id = cur.lastrowid
        return livro

    def listar(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM livro ORDER BY titulo").fetchall()
        return [Livro(**dict(r)) for r in rows]

    def buscar_por_id(self, livro_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM livro WHERE id = ?", (livro_id,)).fetchone()
        return Livro(**dict(row)) if row else None
