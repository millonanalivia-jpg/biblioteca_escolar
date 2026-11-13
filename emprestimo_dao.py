from datetime import date

from database import get_connection
from POO.models.emprestimo import Emprestimo


class EmprestimoDAO:
    def registrar(self, emp):
        """Cria o empréstimo e diminui o estoque do livro."""
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE livro SET quantidade_disponivel = quantidade_disponivel - 1 "
                "WHERE id = ? AND quantidade_disponivel > 0", (emp.livro_id,))
            if cur.rowcount == 0:
                raise ValueError("Livro indisponível.")
            cur = conn.execute(
                "INSERT INTO emprestimo (aluno_id, livro_id, data_emprestimo, data_prevista, status) "
                "VALUES (?, ?, ?, ?, ?)",
                (emp.aluno_id, emp.livro_id, emp.data_emprestimo, emp.data_prevista, emp.status))
            emp.id = cur.lastrowid
        return emp

    def listar(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM emprestimo ORDER BY id DESC").fetchall()
        return [Emprestimo(**dict(r)) for r in rows]

    def buscar_por_id(self, emp_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM emprestimo WHERE id = ?", (emp_id,)).fetchone()
        return Emprestimo(**dict(row)) if row else None

    def devolver(self, emp):
        """Marca como devolvido e devolve o exemplar ao estoque."""
        emp.data_devolucao = date.today().isoformat()
        emp.status = "DEVOLVIDO"
        with get_connection() as conn:
            conn.execute("UPDATE emprestimo SET data_devolucao = ?, status = ? WHERE id = ?",
                         (emp.data_devolucao, emp.status, emp.id))
            conn.execute("UPDATE livro SET quantidade_disponivel = quantidade_disponivel + 1 "
                         "WHERE id = ?", (emp.livro_id,))
        return emp
