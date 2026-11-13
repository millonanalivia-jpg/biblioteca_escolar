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
            quantidade_total if quantidade_disponivel is None else quantidade_disponivel)

    def to_dict(self):
        return dict(vars(self))
