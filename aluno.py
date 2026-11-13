class Aluno:
    def __init__(self, nome, matricula, turma=None, email=None, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.turma = turma
        self.email = email

    def to_dict(self):
        return dict(vars(self))
