class Emprestimo:
    def __init__(self, aluno_id, livro_id, data_emprestimo, data_devolucao=None, id=None):
        self.id = id
        self.aluno_id = aluno_id
        self.livro_id = livro_id
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao

    def to_dict(self):
        return {"id": self.id, "aluno_id": self.aluno_id, "livro_id": self.livro_id,
                "data_emprestimo": self.data_emprestimo,
                "data_devolucao": self.data_devolucao}
