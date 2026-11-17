from database import conexao
from livro import Livro


class LivroDAO:
    def listar(self):
        with conexao() as conn:
            linhas = conn.execute("SELECT * FROM livro ORDER BY titulo").fetchall()
        return [Livro(l["titulo"], l["autor"], l["ano"], l["disponivel"], l["id"])
                for l in linhas]

    def buscar(self, id):
        with conexao() as conn:
            l = conn.execute("SELECT * FROM livro WHERE id=?", (id,)).fetchone()
        if l is None:
            return None
        return Livro(l["titulo"], l["autor"], l["ano"], l["disponivel"], l["id"])

    def inserir(self, livro):
        with conexao() as conn:
            cur = conn.execute(
                "INSERT INTO livro (titulo, autor, ano, disponivel) VALUES (?, ?, ?, 1)",
                (livro.titulo, livro.autor, livro.ano),
            )
            livro.id = cur.lastrowid
        livro.disponivel = True
        return livro

    def atualizar(self, livro):
        with conexao() as conn:
            cur = conn.execute(
                "UPDATE livro SET titulo=?, autor=?, ano=? WHERE id=?",
                (livro.titulo, livro.autor, livro.ano, livro.id),
            )
        return cur.rowcount > 0

    def excluir(self, id):
        with conexao() as conn:
            cur = conn.execute("DELETE FROM livro WHERE id=?", (id,))
        return cur.rowcount > 0
