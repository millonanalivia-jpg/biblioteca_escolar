from database import get_connection
from POO.models.emprestimo import Emprestimo


class EmprestimoDAO:
    def registrar(self, emprestimo):
        """Cria o empréstimo e baixa o estoque do livro na mesma transação."""
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE livro SET quantidade_disponivel = quantidade_disponivel - 1 "
                "WHERE id = ? AND quantidade_disponivel > 0", (emprestimo.livro_id,))
            if cur.rowcount == 0:
                raise ValueError("Livro indisponível para empréstimo.")
            cur = conn.execute(
                """INSERT INTO emprestimo (aluno_id, livro_id, data_emprestimo, data_prevista, status)
                   VALUES (?, ?, ?, ?, ?)""",
                (emprestimo.aluno_id, emprestimo.livro_id, emprestimo.data_emprestimo,
                 emprestimo.data_prevista, emprestimo.status))
            emprestimo.id = cur.lastrowid
        return emprestimo

    def devolver(self, emprestimo):
        """Marca como devolvido e devolve o exemplar ao estoque."""
        with get_connection() as conn:
            conn.execute(
                "UPDATE emprestimo SET data_devolucao = ?, status = ? WHERE id = ?",
                (emprestimo.data_devolucao, emprestimo.status, emprestimo.id))
            conn.execute(
                "UPDATE livro SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id = ?",
                (emprestimo.livro_id,))
        return emprestimo

    def listar(self, status=None, aluno_id=None):
        sql, params = "SELECT * FROM emprestimo WHERE 1=1", []
        if status:
            sql += " AND status = ?"
            params.append(status.upper())
        if aluno_id:
            sql += " AND aluno_id = ?"
            params.append(aluno_id)
        sql += " ORDER BY data_emprestimo DESC, id DESC"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [Emprestimo.from_row(r) for r in rows]

    def buscar_por_id(self, emprestimo_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM emprestimo WHERE id = ?", (emprestimo_id,)).fetchone()
        return Emprestimo.from_row(row) if row else None

    def aluno_tem_emprestimo_ativo(self, aluno_id, livro_id):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT 1 FROM emprestimo WHERE aluno_id = ? AND livro_id = ? AND status = 'ATIVO'",
                (aluno_id, livro_id)).fetchone()
        return row is not None

    def listar_detalhado(self, status=None):
        """Empréstimos com nome do aluno e título do livro (útil para o front-end)."""
        sql = """SELECT e.*, a.nome AS aluno_nome, l.titulo AS livro_titulo
                 FROM emprestimo e
                 JOIN aluno a ON a.id = e.aluno_id
                 JOIN livro l ON l.id = e.livro_id"""
        params = []
        if status:
            sql += " WHERE e.status = ?"
            params.append(status.upper())
        sql += " ORDER BY e.data_emprestimo DESC, e.id DESC"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

    def aluno_possui_emprestimos(self, aluno_id):
        with get_connection() as conn:
            return conn.execute(
                "SELECT 1 FROM emprestimo WHERE aluno_id = ? LIMIT 1", (aluno_id,)).fetchone() is not None

    def livro_possui_emprestimos(self, livro_id):
        with get_connection() as conn:
            return conn.execute(
                "SELECT 1 FROM emprestimo WHERE livro_id = ? LIMIT 1", (livro_id,)).fetchone() is not None
