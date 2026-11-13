# Biblioteca Escolar – Etapa 2

Back-end em Python (Flask) com POO e DAOs.

- **POO (classes):** `aluno.py`, `livro.py`, `emprestimo.py`
- **POO (DAOs):** `aluno_dao.py`, `livro_dao.py`, `emprestimo_dao.py`
- **DWS (rotas Flask):** `app.py`
- **BD:** `database.py` e `schema.sql`

## Como rodar
```
pip3 install -r requirements.txt
python3 app.py
```
A API sobe em http://127.0.0.1:5000

## Rotas
| Método | Rota | Função |
|---|---|---|
| POST, GET | `/alunos` | cadastrar, listar |
| GET | `/alunos/<id>` | consultar |
| POST, GET | `/livros` | cadastrar, listar |
| GET | `/livros/<id>` | consultar |
| POST, GET | `/emprestimos` | registrar, listar |
| PUT | `/emprestimos/<id>/devolucao` | devolver |
