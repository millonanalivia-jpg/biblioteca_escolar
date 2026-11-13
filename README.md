# Biblioteca Escolar – Etapa 2

## Organização
- `POO/models/` – classes Aluno, Livro, Emprestimo
- `POO/dao/` – AlunoDAO, LivroDAO, EmprestimoDAO
- `DWS/app.py` – rotas Flask (API REST)
- `DWS/teste_api.py` – teste das rotas
- Parte de BD (`database.py` e `schema.sql`) fica na raiz do projeto, ao lado de `DWS/` e `POO/`

## Como rodar (na pasta raiz do projeto)
```
pip3 install -r DWS/requirements.txt
python3 DWS/app.py        # http://127.0.0.1:5000
python3 DWS/teste_api.py
```

## Rotas
| Método | Rota | Descrição |
|---|---|---|
| POST/GET | `/alunos` | cadastrar / listar (`?nome=`) |
| GET/PUT/DELETE | `/alunos/<id>` | consultar / atualizar / remover |
| POST/GET | `/livros` | cadastrar / listar (`?busca=`) |
| GET/PUT/DELETE | `/livros/<id>` | consultar / atualizar / remover |
| POST | `/emprestimos` | registrar (`aluno_id`, `livro_id`) |
| GET | `/emprestimos` | listar (`?status=`, `?aluno_id=`, `?detalhado=true`) |
| GET | `/emprestimos/<id>` | consultar |
| PUT | `/emprestimos/<id>/devolucao` | registrar devolução |
