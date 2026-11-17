from database import conexao
from aluno import Aluno


class AlunoDAO:
    def listar(self):
        with conexao() as conn:
            linhas = conn.execute("SELECT * FROM aluno ORDER BY nome").fetchall()
        return [Aluno(l["nome"], l["matricula"], l["turma"], l["id"]) for l in linhas]

    def buscar(self, id):
        with conexao() as conn:
            l = conn.execute("SELECT * FROM aluno WHERE id=?", (id,)).fetchone()
        if l is None:
            return None
        return Aluno(l["nome"], l["matricula"], l["turma"], l["id"])

    def inserir(self, aluno):
        with conexao() as conn:
            cur = conn.execute(
                "INSERT INTO aluno (nome, matricula, turma) VALUES (?, ?, ?)",
                (aluno.nome, aluno.matricula, aluno.turma),
            )
            aluno.id = cur.lastrowid
        return aluno

    def atualizar(self, aluno):
        with conexao() as conn:
            cur = conn.execute(
                "UPDATE aluno SET nome=?, matricula=?, turma=? WHERE id=?",
                (aluno.nome, aluno.matricula, aluno.turma, aluno.id),
            )
        return cur.rowcount > 0

    def excluir(self, id):
        with conexao() as conn:
            cur = conn.execute("DELETE FROM aluno WHERE id=?", (id,))
        return cur.rowcount > 0
