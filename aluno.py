class Aluno:
    def __init__(self, nome, matricula, turma="", id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.turma = turma

    def to_dict(self):
        return {"id": self.id, "nome": self.nome,
                "matricula": self.matricula, "turma": self.turma}
        
