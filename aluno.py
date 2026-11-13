class Aluno:
    def __init__(self, nome, matricula, turma=None, email=None, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.turma = turma
        self.email = email

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O nome do aluno é obrigatório.")
        self._nome = str(valor).strip()

    @property
    def matricula(self):
        return self._matricula

    @matricula.setter
    def matricula(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("A matrícula do aluno é obrigatória.")
        self._matricula = str(valor).strip()

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "matricula": self.matricula,
                "turma": self.turma, "email": self.email}

    @classmethod
    def from_row(cls, row):
        return cls(row["nome"], row["matricula"], row["turma"], row["email"], row["id"])
