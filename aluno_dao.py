from database import get_connection
from POO.models.aluno import Aluno


class AlunoDAO:
    def inserir(self, aluno):
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO aluno (nome, matricula, turma, email) VALUES (?, ?, ?, ?)",
                (aluno.nome, aluno.matricula, aluno.turma, aluno.email))
            aluno.id = cur.lastrowid
        return aluno

    def listar(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM aluno ORDER BY nome").fetchall()
        return [Aluno.from_row(r) for r in rows]

    def buscar_por_id(self, aluno_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM aluno WHERE id = ?", (aluno_id,)).fetchone()
        return Aluno.from_row(row) if row else None

    def buscar_por_nome(self, termo):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM aluno WHERE nome LIKE ? ORDER BY nome", (f"%{termo}%",)).fetchall()
        return [Aluno.from_row(r) for r in rows]

    def atualizar(self, aluno):
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE aluno SET nome = ?, matricula = ?, turma = ?, email = ? WHERE id = ?",
                (aluno.nome, aluno.matricula, aluno.turma, aluno.email, aluno.id))
        return cur.rowcount > 0

    def remover(self, aluno_id):
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM aluno WHERE id = ?", (aluno_id,))
        return cur.rowcount > 0
