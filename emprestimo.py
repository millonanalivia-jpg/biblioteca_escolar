from datetime import date, timedelta


class Emprestimo:
    def __init__(self, aluno_id, livro_id, data_emprestimo=None, data_prevista=None,
                 data_devolucao=None, status="ATIVO", id=None):
        self.id = id
        self.aluno_id = aluno_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo or date.today().isoformat()
        self.data_prevista = data_prevista or (date.today() + timedelta(days=7)).isoformat()
        self.data_devolucao = data_devolucao
        self.status = status

    def to_dict(self):
        return dict(vars(self))
