"""Teste rápido de todas as rotas. Execute: python teste_api.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["BIBLIOTECA_DB"] = os.path.join(tempfile.mkdtemp(), "teste.db")
from DWS.app import app  # noqa: E402

c = app.test_client()


def check(desc, resp, esperado):
    ok = resp.status_code == esperado
    print(("OK   " if ok else "FALHA"), desc, "->", resp.status_code)
    assert ok, resp.get_data(as_text=True)
    return resp.get_json(silent=True)


a = check("criar aluno", c.post("/alunos", json={"nome": "Ana", "matricula": "001", "turma": "3A"}), 201)
check("matrícula duplicada", c.post("/alunos", json={"nome": "Bia", "matricula": "001"}), 409)
check("aluno sem nome", c.post("/alunos", json={"matricula": "002"}), 400)
check("listar alunos", c.get("/alunos"), 200)
check("atualizar aluno", c.put(f"/alunos/{a['id']}", json={"turma": "3B"}), 200)
check("aluno inexistente", c.get("/alunos/999"), 404)

l = check("criar livro", c.post("/livros", json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "quantidade_total": 1}), 201)
check("buscar livro", c.get("/livros?busca=machado"), 200)

e = check("criar empréstimo", c.post("/emprestimos", json={"aluno_id": a["id"], "livro_id": l["id"]}), 201)
check("estoque zerou", c.get(f"/livros/{l['id']}"), 200)
assert c.get(f"/livros/{l['id']}").get_json()["quantidade_disponivel"] == 0
check("empréstimo repetido", c.post("/emprestimos", json={"aluno_id": a["id"], "livro_id": l["id"]}), 409)
b = check("criar 2º aluno", c.post("/alunos", json={"nome": "Caio", "matricula": "003"}), 201)
check("livro indisponível", c.post("/emprestimos", json={"aluno_id": b["id"], "livro_id": l["id"]}), 409)
check("remover aluno com empréstimo", c.delete(f"/alunos/{a['id']}"), 409)
check("listar detalhado", c.get("/emprestimos?detalhado=true&status=ativo"), 200)
check("devolver", c.put(f"/emprestimos/{e['id']}/devolucao"), 200)
check("devolver de novo", c.put(f"/emprestimos/{e['id']}/devolucao"), 409)
assert c.get(f"/livros/{l['id']}").get_json()["quantidade_disponivel"] == 1
check("remover aluno sem empréstimo", c.delete(f"/alunos/{b['id']}"), 204)
print("\nTodos os testes passaram.")
