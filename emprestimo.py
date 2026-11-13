from datetime import date, timedelta

PRAZO_PADRAO_DIAS = 7


class Emprestimo:
    def __init__(self, aluno_id, livro_id, data_emprestimo=None, data_prevista=None,
                 data_devolucao=None, status="ATIVO", id=None):
        self.id = id
        self.aluno_id = aluno_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo or date.today().isoformat()
        self.data_prevista = data_prevista or (
            date.fromisoformat(self.data_emprestimo) + timedelta(days=PRAZO_PADRAO_DIAS)
        ).isoformat()
        self.data_devolucao = data_devolucao
        self.status = status

    def esta_ativo(self):
        return self.status == "ATIVO"

    def registrar_devolucao(self):
        if not self.esta_ativo():
            raise ValueError("Este empréstimo já foi devolvido.")
        self.data_devolucao = date.today().isoformat()
        self.status = "DEVOLVIDO"

    def to_dict(self):
        return {"id": self.id, "aluno_id": self.aluno_id, "livro_id": self.livro_id,
                "data_emprestimo": self.data_emprestimo, "data_prevista": self.data_prevista,
                "data_devolucao": self.data_devolucao, "status": self.status}

    @classmethod
    def from_row(cls, row):
        return cls(row["aluno_id"], row["livro_id"], row["data_emprestimo"],
                   row["data_prevista"], row["data_devolucao"], row["status"], row["id"])
