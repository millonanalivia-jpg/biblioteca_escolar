"""API da Biblioteca Escolar (Flask). Rode na pasta raiz: python3 DWS/app.py"""
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
aluno_dao = AlunoDAO()
livro_dao = LivroDAO()
emprestimo_dao = EmprestimoDAO()


@app.after_request
def liberar_cors(resp):  # permite o front-end (Fetch) chamar a API
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return resp


def erro(msg, codigo):
    return jsonify({"erro": msg}), codigo


# ---------- ALUNOS ----------
@app.post("/alunos")
def cadastrar_aluno():
    d = request.get_json(silent=True) or {}
    if not d.get("nome") or not d.get("matricula"):
        return erro("nome e matricula são obrigatórios", 400)
    aluno = Aluno(d["nome"], d["matricula"], d.get("turma"), d.get("email"))
    try:
        aluno_dao.inserir(aluno)
    except sqlite3.IntegrityError:
        return erro("matrícula já cadastrada", 400)
    return jsonify(aluno.to_dict()), 201


@app.get("/alunos")
def listar_alunos():
    return jsonify([a.to_dict() for a in aluno_dao.listar()])


@app.get("/alunos/<int:aluno_id>")
def consultar_aluno(aluno_id):
    aluno = aluno_dao.buscar_por_id(aluno_id)
    return jsonify(aluno.to_dict()) if aluno else erro("aluno não encontrado", 404)


# ---------- LIVROS ----------
@app.post("/livros")
def cadastrar_livro():
    d = request.get_json(silent=True) or {}
    if not d.get("titulo") or not d.get("autor"):
        return erro("titulo e autor são obrigatórios", 400)
    livro = Livro(d["titulo"], d["autor"], d.get("isbn"), d.get("ano"),
                  d.get("quantidade_total", 1))
    try:
        livro_dao.inserir(livro)
    except sqlite3.IntegrityError:
        return erro("ISBN já cadastrado", 400)
    return jsonify(livro.to_dict()), 201


@app.get("/livros")
def listar_livros():
    return jsonify([l.to_dict() for l in livro_dao.listar()])


@app.get("/livros/<int:livro_id>")
def consultar_livro(livro_id):
    livro = livro_dao.buscar_por_id(livro_id)
    return jsonify(livro.to_dict()) if livro else erro("livro não encontrado", 404)


# ---------- EMPRÉSTIMOS ----------
@app.post("/emprestimos")
def registrar_emprestimo():
    d = request.get_json(silent=True) or {}
    if not aluno_dao.buscar_por_id(d.get("aluno_id")):
        return erro("aluno não encontrado", 404)
    if not livro_dao.buscar_por_id(d.get("livro_id")):
        return erro("livro não encontrado", 404)
    emp = Emprestimo(d["aluno_id"], d["livro_id"])
    try:
        emprestimo_dao.registrar(emp)
    except ValueError as e:
        return erro(str(e), 400)
    return jsonify(emp.to_dict()), 201


@app.get("/emprestimos")
def listar_emprestimos():
    return jsonify([e.to_dict() for e in emprestimo_dao.listar()])


@app.put("/emprestimos/<int:emp_id>/devolucao")
def devolver_emprestimo(emp_id):
    emp = emprestimo_dao.buscar_por_id(emp_id)
    if not emp:
        return erro("empréstimo não encontrado", 404)
    if emp.status == "DEVOLVIDO":
        return erro("empréstimo já devolvido", 400)
    return jsonify(emprestimo_dao.devolver(emp).to_dict())


init_db()

if __name__ == "__main__":
    app.run(debug=True)
