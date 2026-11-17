# Biblioteca Escolar — Projeto Integrado (DWS, POO e BD)

Sistema web para uma biblioteca escolar: cadastro de **alunos** e **livros** e controle de **empréstimos e devoluções**.

- **Back-end:** Python + Flask, com classes (POO) e DAOs
- **Banco de dados:** SQLite (`schema.sql`; o arquivo `biblioteca.db` é criado automaticamente)
- **Front-end:** HTML, CSS e JavaScript (Fetch) em `static/`

## Estrutura
| Arquivo | Função |
|---|---|
| `aluno.py`, `livro.py`, `emprestimo.py` | Classes do modelo (POO) |
| `aluno_dao.py`, `livro_dao.py`, `emprestimo_dao.py` | Acesso ao banco (DAO) |
| `database.py` | Conexão e criação das tabelas |
| `schema.sql` | Estrutura das tabelas |
| `app.py` | Rotas Flask (API) e servidor da página |
| `static/index.html`, `style.css`, `script.js` | Front-end |
| `diagrama_de_classes_UML.png` | Diagrama de classes |

## Como executar
```bash
pip install -r requirements.txt
python app.py
```
Abra no navegador: http://127.0.0.1:5000

## Rotas da API
| Método | Rota | Função |
|---|---|---|
| GET / POST | `/api/alunos` | Listar / cadastrar aluno |
| PUT / DELETE | `/api/alunos/<id>` | Editar / excluir aluno |
| GET / POST | `/api/livros` | Listar / cadastrar livro |
| PUT / DELETE | `/api/livros/<id>` | Editar / excluir livro |
| GET / POST | `/api/emprestimos` | Listar / registrar empréstimo |
| PUT | `/api/emprestimos/<id>/devolver` | Registrar devolução |

## Regras de negócio
- A matrícula do aluno é única.
- Um livro emprestado fica indisponível até ser devolvido.
- Não é possível excluir aluno ou livro que tenha empréstimos.
