class Livro:
    def __init__(self, titulo, autor, ano=None, disponivel=True, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.disponivel = disponivel

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "autor": self.autor,
                "ano": self.ano, "disponivel": bool(self.disponivel)}
