from datetime import date

from database import conexao
from emprestimo import Emprestimo


class EmprestimoDAO:
    def listar(self):
        """Retorna dicts já com nome do aluno e título do livro (JOIN)."""
        with conexao() as conn:
            linhas = conn.execute(
                """
                SELECT e.*, a.nome AS aluno_nome, l.titulo AS livro_titulo
                FROM emprestimo e
                JOIN aluno a ON a.id = e.aluno_id
                JOIN livro l ON l.id = e.livro_id
                ORDER BY e.id DESC
                """
            ).fetchall()
        return [dict(l) for l in linhas]

    def registrar(self, aluno_id, livro_id):
        """Cria o empréstimo e marca o livro como indisponível (mesma transação)."""
        hoje = date.today().isoformat()
        with conexao() as conn:
            cur = conn.execute(
                "INSERT INTO emprestimo (aluno_id, livro_id, data_emprestimo) VALUES (?, ?, ?)",
                (aluno_id, livro_id, hoje),
            )
            conn.execute("UPDATE livro SET disponivel=0 WHERE id=?", (livro_id,))
        return Emprestimo(aluno_id, livro_id, hoje, None, cur.lastrowid)

    def devolver(self, id):
        with conexao() as conn:
            e = conn.execute("SELECT * FROM emprestimo WHERE id=?", (id,)).fetchone()
            if e is None:
                return "nao_encontrado"
            if e["data_devolucao"] is not None:
                return "ja_devolvido"
            conn.execute("UPDATE emprestimo SET data_devolucao=? WHERE id=?",
                         (date.today().isoformat(), id))
            conn.execute("UPDATE livro SET disponivel=1 WHERE id=?", (e["livro_id"],))
        return "ok"
