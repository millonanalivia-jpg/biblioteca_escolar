"""Teste rápido das rotas. Rode na pasta raiz: python3 DWS/teste_api.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["BIBLIOTECA_DB"] = os.path.join(tempfile.mkdtemp(), "teste.db")
from DWS.app import app  # noqa: E402

c = app.test_client()


def ok(desc, resp, esperado):
    print("OK   " if resp.status_code == esperado else "FALHA", desc, resp.status_code)
    assert resp.status_code == esperado
    return resp.get_json(silent=True)


aluno = ok("cadastrar aluno", c.post("/alunos", json={"nome": "Ana", "matricula": "001"}), 201)
ok("aluno sem nome", c.post("/alunos", json={"matricula": "002"}), 400)
ok("listar alunos", c.get("/alunos"), 200)
ok("consultar aluno", c.get(f"/alunos/{aluno['id']}"), 200)
livro = ok("cadastrar livro", c.post("/livros", json={"titulo": "Dom Casmurro", "autor": "Machado"}), 201)
ok("listar livros", c.get("/livros"), 200)
emp = ok("registrar empréstimo", c.post("/emprestimos", json={"aluno_id": aluno["id"], "livro_id": livro["id"]}), 201)
ok("livro sem estoque", c.post("/emprestimos", json={"aluno_id": aluno["id"], "livro_id": livro["id"]}), 400)
ok("devolver", c.put(f"/emprestimos/{emp['id']}/devolucao"), 200)
ok("listar empréstimos", c.get("/emprestimos"), 200)
print("\nTodos os testes passaram.")
