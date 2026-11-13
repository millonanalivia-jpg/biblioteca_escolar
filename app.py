"""API REST da Biblioteca Escolar (Flask).

Execução:  python3 DWS/app.py   ->  http://127.0.0.1:5000
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request

from database import init_db
from POO.dao.aluno_dao import AlunoDAO
from POO.dao.livro_dao import LivroDAO
from POO.dao.emprestimo_dao import EmprestimoDAO
from POO.models.aluno import Aluno
from POO.models.livro import Livro
from POO.models.emprestimo import Emprestimo

app = Flask(__name__)


@app.after_request
def liberar_cors(resp):
    """Permite que o front-end (Fetch) acesse a API de outra origem."""
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return resp

aluno_dao = AlunoDAO()
livro_dao = LivroDAO()
emprestimo_dao = EmprestimoDAO()


# ---------- tratamento de erros ----------
def erro(msg, status):
    return jsonify({"erro": msg}), status


@app.errorhandler(ValueError)
def tratar_value_error(e):
    return erro(str(e), 400)


@app.errorhandler(sqlite3.IntegrityError)
def tratar_integridade(e):
    return erro("Violação de integridade (registro duplicado ou em uso).", 409)


@app.errorhandler(404)
def tratar_404(e):
    return erro("Rota não encontrada.", 404)


def corpo_json():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        raise ValueError("Envie um corpo JSON válido.")
    return dados


@app.get("/")
def index():
    return jsonify({"api": "Biblioteca Escolar", "status": "ok"})


# ---------- ALUNOS ----------
@app.post("/alunos")
def criar_aluno():
    d = corpo_json()
    aluno = Aluno(d.get("nome"), d.get("matricula"), d.get("turma"), d.get("email"))
    return jsonify(aluno_dao.inserir(aluno).to_dict()), 201


@app.get("/alunos")
def listar_alunos():
    busca = request.args.get("nome")
    alunos = aluno_dao.buscar_por_nome(busca) if busca else aluno_dao.listar()
    return jsonify([a.to_dict() for a in alunos])


@app.get("/alunos/<int:aluno_id>")
def obter_aluno(aluno_id):
    aluno = aluno_dao.buscar_por_id(aluno_id)
    return jsonify(aluno.to_dict()) if aluno else erro("Aluno não encontrado.", 404)


@app.put("/alunos/<int:aluno_id>")
def atualizar_aluno(aluno_id):
    aluno = aluno_dao.buscar_por_id(aluno_id)
    if not aluno:
        return erro("Aluno não encontrado.", 404)
    d = corpo_json()
    aluno.nome = d.get("nome", aluno.nome)
    aluno.matricula = d.get("matricula", aluno.matricula)
    aluno.turma = d.get("turma", aluno.turma)
    aluno.email = d.get("email", aluno.email)
    aluno_dao.atualizar(aluno)
    return jsonify(aluno.to_dict())


@app.delete("/alunos/<int:aluno_id>")
def remover_aluno(aluno_id):
    if emprestimo_dao.aluno_possui_emprestimos(aluno_id):
        return erro("Aluno possui empréstimos registrados e não pode ser removido.", 409)
    if not aluno_dao.remover(aluno_id):
        return erro("Aluno não encontrado.", 404)
    return "", 204


# ---------- LIVROS ----------
@app.post("/livros")
def criar_livro():
    d = corpo_json()
    livro = Livro(d.get("titulo"), d.get("autor"), d.get("isbn"), d.get("ano"),
                  d.get("quantidade_total", 1))
    return jsonify(livro_dao.inserir(livro).to_dict()), 201


@app.get("/livros")
def listar_livros():
    busca = request.args.get("busca")
    livros = livro_dao.buscar(busca) if busca else livro_dao.listar()
    return jsonify([l.to_dict() for l in livros])


@app.get("/livros/<int:livro_id>")
def obter_livro(livro_id):
    livro = livro_dao.buscar_por_id(livro_id)
    return jsonify(livro.to_dict()) if livro else erro("Livro não encontrado.", 404)


@app.put("/livros/<int:livro_id>")
def atualizar_livro(livro_id):
    livro = livro_dao.buscar_por_id(livro_id)
    if not livro:
        return erro("Livro não encontrado.", 404)
    d = corpo_json()
    livro.titulo = d.get("titulo", livro.titulo)
    livro.autor = d.get("autor", livro.autor)
    livro.isbn = d.get("isbn", livro.isbn)
    livro.ano = d.get("ano", livro.ano)
    if "quantidade_total" in d:
        emprestados = livro.quantidade_total - livro.quantidade_disponivel
        livro.quantidade_total = d["quantidade_total"]
        if livro.quantidade_total < emprestados:
            raise ValueError("Quantidade total menor que o número de exemplares emprestados.")
        livro.quantidade_disponivel = livro.quantidade_total - emprestados
    livro_dao.atualizar(livro)
    return jsonify(livro.to_dict())


@app.delete("/livros/<int:livro_id>")
def remover_livro(livro_id):
    if emprestimo_dao.livro_possui_emprestimos(livro_id):
        return erro("Livro possui empréstimos registrados e não pode ser removido.", 409)
    if not livro_dao.remover(livro_id):
        return erro("Livro não encontrado.", 404)
    return "", 204


# ---------- EMPRÉSTIMOS ----------
@app.post("/emprestimos")
def criar_emprestimo():
    d = corpo_json()
    aluno_id, livro_id = d.get("aluno_id"), d.get("livro_id")
    if not isinstance(aluno_id, int) or not isinstance(livro_id, int):
        raise ValueError("aluno_id e livro_id são obrigatórios (inteiros).")
    if not aluno_dao.buscar_por_id(aluno_id):
        return erro("Aluno não encontrado.", 404)
    if not livro_dao.buscar_por_id(livro_id):
        return erro("Livro não encontrado.", 404)
    if emprestimo_dao.aluno_tem_emprestimo_ativo(aluno_id, livro_id):
        return erro("O aluno já possui um empréstimo ativo deste livro.", 409)
    emp = Emprestimo(aluno_id, livro_id, data_prevista=d.get("data_prevista"))
    try:
        emprestimo_dao.registrar(emp)
    except ValueError as e:
        return erro(str(e), 409)
    return jsonify(emp.to_dict()), 201


@app.get("/emprestimos")
def listar_emprestimos():
    status = request.args.get("status")
    if request.args.get("detalhado") == "true":
        return jsonify(emprestimo_dao.listar_detalhado(status))
    aluno_id = request.args.get("aluno_id", type=int)
    return jsonify([e.to_dict() for e in emprestimo_dao.listar(status, aluno_id)])


@app.get("/emprestimos/<int:emprestimo_id>")
def obter_emprestimo(emprestimo_id):
    emp = emprestimo_dao.buscar_por_id(emprestimo_id)
    return jsonify(emp.to_dict()) if emp else erro("Empréstimo não encontrado.", 404)


@app.put("/emprestimos/<int:emprestimo_id>/devolucao")
def devolver_emprestimo(emprestimo_id):
    emp = emprestimo_dao.buscar_por_id(emprestimo_id)
    if not emp:
        return erro("Empréstimo não encontrado.", 404)
    try:
        emp.registrar_devolucao()
    except ValueError as e:
        return erro(str(e), 409)
    emprestimo_dao.devolver(emp)
    return jsonify(emp.to_dict())


init_db()

if __name__ == "__main__":
    app.run(debug=True)
