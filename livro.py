class Livro:
    def __init__(self, titulo, autor, isbn=None, ano=None,
                 quantidade_total=1, quantidade_disponivel=None, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano = ano
        self.quantidade_total = quantidade_total
        self.quantidade_disponivel = (
            self.quantidade_total if quantidade_disponivel is None else quantidade_disponivel
        )

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O título do livro é obrigatório.")
        self._titulo = str(valor).strip()

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("O autor do livro é obrigatório.")
        self._autor = str(valor).strip()

    @property
    def quantidade_total(self):
        return self._quantidade_total

    @quantidade_total.setter
    def quantidade_total(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("A quantidade deve ser um número inteiro.")
        if valor < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        self._quantidade_total = valor

    def tem_disponibilidade(self):
        return self.quantidade_disponivel > 0

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "autor": self.autor,
                "isbn": self.isbn, "ano": self.ano,
                "quantidade_total": self.quantidade_total,
                "quantidade_disponivel": self.quantidade_disponivel}

    @classmethod
    def from_row(cls, row):
        return cls(row["titulo"], row["autor"], row["isbn"], row["ano"],
                   row["quantidade_total"], row["quantidade_disponivel"], row["id"])
