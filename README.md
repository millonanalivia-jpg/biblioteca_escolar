# Biblioteca Escolar – Etapa 2

- `POO/models/` – classes Aluno, Livro, Emprestimo
- `POO/dao/` – AlunoDAO, LivroDAO, EmprestimoDAO
- `DWS/app.py` – rotas Flask
- `database.py` e `schema.sql` (BD) ficam na raiz, ao lado de `DWS/` e `POO/`

## Como rodar (na pasta raiz)
```
pip3 install -r DWS/requirements.txt
python3 DWS/app.py
python3 DWS/teste_api.py
```

## Rotas
| Método | Rota | Função |
|---|---|---|
| POST, GET | `/alunos` | cadastrar, listar |
| GET | `/alunos/<id>` | consultar |
| POST, GET | `/livros` | cadastrar, listar |
| GET | `/livros/<id>` | consultar |
| POST, GET | `/emprestimos` | registrar, listar |
| PUT | `/emprestimos/<id>/devolucao` | devolver |
