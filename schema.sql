CREATE TABLE IF NOT EXISTS aluno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    turma TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS livro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    isbn TEXT UNIQUE,
    ano INTEGER,
    quantidade_total INTEGER NOT NULL DEFAULT 1 CHECK (quantidade_total >= 0),
    quantidade_disponivel INTEGER NOT NULL DEFAULT 1 CHECK (quantidade_disponivel >= 0)
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_prevista TEXT NOT NULL,
    data_devolucao TEXT,
    status TEXT NOT NULL DEFAULT 'ATIVO' CHECK (status IN ('ATIVO', 'DEVOLVIDO')),
    FOREIGN KEY (aluno_id) REFERENCES aluno(id),
    FOREIGN KEY (livro_id) REFERENCES livro(id)
);
