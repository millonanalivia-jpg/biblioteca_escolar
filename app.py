import sqlite3

from flask import Flask, jsonify, request

from database import criar_tabelas
from aluno import Aluno
from livro import Livro
from aluno_dao import AlunoDAO
from livro_dao import LivroDAO
from emprestimo_dao import EmprestimoDAO

app = Flask(__name__, static_folder="static", static_url_path="/static")
criar_tabelas()

aluno_dao = AlunoDAO()
livro_dao = LivroDAO()
emprestimo_dao = EmprestimoDAO()


def erro(msg, codigo=400):
    return jsonify({"erro": msg}), codigo


@app.route("/")
def index():
    return app.send_static_file("index.html")


# ---------------- ALUNOS ----------------
@app.route("/api/alunos", methods=["GET"])
def listar_alunos():
    return jsonify([a.to_dict() for a in aluno_dao.listar()])


@app.route("/api/alunos", methods=["POST"])
def criar_aluno():
    d = request.get_json(silent=True) or {}
    if not d.get("nome") or not d.get("matricula"):
        return erro("Nome e matrícula são obrigatórios.")
    try:
        aluno = aluno_dao.inserir(Aluno(d["nome"].strip(), d["matricula"].strip(), d.get("turma", "").strip()))
    except sqlite3.IntegrityError:
        return erro("Já existe um aluno com essa matrícula.")
    return jsonify(aluno.to_dict()), 201


@app.route("/api/alunos/<int:id>", methods=["PUT"])
def editar_aluno(id):
    d = request.get_json(silent=True) or {}
    if not d.get("nome") or not d.get("matricula"):
        return erro("Nome e matrícula são obrigatórios.")
    try:
        ok = aluno_dao.atualizar(Aluno(d["nome"].strip(), d["matricula"].strip(), d.get("turma", "").strip(), id))
    except sqlite3.IntegrityError:
        return erro("Já existe um aluno com essa matrícula.")
    if not ok:
        return erro("Aluno não encontrado.", 404)
    return jsonify({"mensagem": "Aluno atualizado."})


@app.route("/api/alunos/<int:id>", methods=["DELETE"])
def excluir_aluno(id):
    try:
        ok = aluno_dao.excluir(id)
    except sqlite3.IntegrityError:
        return erro("Não é possível excluir: aluno possui empréstimos.")
    if not ok:
        return erro("Aluno não encontrado.", 404)
    return jsonify({"mensagem": "Aluno excluído."})


# ---------------- LIVROS ----------------
@app.route("/api/livros", methods=["GET"])
def listar_livros():
    return jsonify([l.to_dict() for l in livro_dao.listar()])


def _ano(valor):
    try:
        return int(valor) if valor not in (None, "") else None
    except (TypeError, ValueError):
        raise ValueError("Ano inválido.")


@app.route("/api/livros", methods=["POST"])
def criar_livro():
    d = request.get_json(silent=True) or {}
    if not d.get("titulo") or not d.get("autor"):
        return erro("Título e autor são obrigatórios.")
    try:
        ano = _ano(d.get("ano"))
    except ValueError as e:
        return erro(str(e))
    livro = livro_dao.inserir(Livro(d["titulo"].strip(), d["autor"].strip(), ano))
    return jsonify(livro.to_dict()), 201


@app.route("/api/livros/<int:id>", methods=["PUT"])
def editar_livro(id):
    d = request.get_json(silent=True) or {}
    if not d.get("titulo") or not d.get("autor"):
        return erro("Título e autor são obrigatórios.")
    try:
        ano = _ano(d.get("ano"))
    except ValueError as e:
        return erro(str(e))
    if not livro_dao.atualizar(Livro(d["titulo"].strip(), d["autor"].strip(), ano, id=id)):
        return erro("Livro não encontrado.", 404)
    return jsonify({"mensagem": "Livro atualizado."})


@app.route("/api/livros/<int:id>", methods=["DELETE"])
def excluir_livro(id):
    try:
        ok = livro_dao.excluir(id)
    except sqlite3.IntegrityError:
        return erro("Não é possível excluir: livro possui empréstimos.")
    if not ok:
        return erro("Livro não encontrado.", 404)
    return jsonify({"mensagem": "Livro excluído."})


# ---------------- EMPRÉSTIMOS ----------------
@app.route("/api/emprestimos", methods=["GET"])
def listar_emprestimos():
    return jsonify(emprestimo_dao.listar())


@app.route("/api/emprestimos", methods=["POST"])
def criar_emprestimo():
    d = request.get_json(silent=True) or {}
    try:
        aluno_id = int(d.get("aluno_id"))
        livro_id = int(d.get("livro_id"))
    except (TypeError, ValueError):
        return erro("Selecione um aluno e um livro.")
    if aluno_dao.buscar(aluno_id) is None:
        return erro("Aluno não encontrado.", 404)
    livro = livro_dao.buscar(livro_id)
    if livro is None:
        return erro("Livro não encontrado.", 404)
    if not livro.disponivel:
        return erro("Este livro já está emprestado.")
    emp = emprestimo_dao.registrar(aluno_id, livro_id)
    return jsonify(emp.to_dict()), 201


@app.route("/api/emprestimos/<int:id>/devolver", methods=["PUT"])
def devolver_emprestimo(id):
    r = emprestimo_dao.devolver(id)
    if r == "nao_encontrado":
        return erro("Empréstimo não encontrado.", 404)
    if r == "ja_devolvido":
        return erro("Este empréstimo já foi devolvido.")
    return jsonify({"mensagem": "Livro devolvido."})


if __name__ == "__main__":
    app.run(debug=True)
