const API = "/api";

// ---------- utilidades ----------
async function requisicao(url, metodo = "GET", corpo = null) {
  const opcoes = { method: metodo, headers: {} };
  if (corpo) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }
  const resp = await fetch(API + url, opcoes);
  const dados = await resp.json();
  if (!resp.ok) throw new Error(dados.erro || "Erro inesperado.");
  return dados;
}

function mostrarMensagem(texto, tipo = "sucesso") {
  const el = document.getElementById("mensagem");
  el.textContent = texto;
  el.className = "mensagem " + tipo;
  setTimeout(() => el.classList.add("oculto"), 3500);
}

function escapar(texto) {
  const d = document.createElement("div");
  d.textContent = texto ?? "";
  return d.innerHTML;
}

function formatarData(iso) {
  if (!iso) return "—";
  const [a, m, d] = iso.split("-");
  return `${d}/${m}/${a}`;
}

// ---------- abas ----------
document.querySelectorAll(".aba").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".aba").forEach(b => b.classList.remove("ativa"));
    document.querySelectorAll(".painel").forEach(p => p.classList.add("oculto"));
    btn.classList.add("ativa");
    document.getElementById(btn.dataset.aba).classList.remove("oculto");
    if (btn.dataset.aba === "emprestimos") carregarEmprestimos();
  });
});

// ---------- ALUNOS ----------
async function carregarAlunos() {
  const alunos = await requisicao("/alunos");
  const tbody = document.getElementById("tabela-alunos");
  tbody.innerHTML = alunos.length ? "" : '<tr><td colspan="4" class="vazio">Nenhum aluno cadastrado.</td></tr>';
  alunos.forEach(a => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapar(a.nome)}</td><td>${escapar(a.matricula)}</td><td>${escapar(a.turma)}</td>
      <td>
        <button class="pequeno">Editar</button>
        <button class="pequeno perigo">Excluir</button>
      </td>`;
    const [bEditar, bExcluir] = tr.querySelectorAll("button");
    bEditar.onclick = () => editarAluno(a);
    bExcluir.onclick = () => excluirAluno(a.id);
    tbody.appendChild(tr);
  });
  return alunos;
}

function editarAluno(a) {
  document.getElementById("aluno-id").value = a.id;
  document.getElementById("aluno-nome").value = a.nome;
  document.getElementById("aluno-matricula").value = a.matricula;
  document.getElementById("aluno-turma").value = a.turma || "";
  document.getElementById("aluno-salvar").textContent = "Salvar";
  document.getElementById("aluno-cancelar").classList.remove("oculto");
}

function limparFormAluno() {
  document.getElementById("form-aluno").reset();
  document.getElementById("aluno-id").value = "";
  document.getElementById("aluno-salvar").textContent = "Cadastrar";
  document.getElementById("aluno-cancelar").classList.add("oculto");
}

document.getElementById("aluno-cancelar").onclick = limparFormAluno;

document.getElementById("form-aluno").addEventListener("submit", async e => {
  e.preventDefault();
  const id = document.getElementById("aluno-id").value;
  const corpo = {
    nome: document.getElementById("aluno-nome").value,
    matricula: document.getElementById("aluno-matricula").value,
    turma: document.getElementById("aluno-turma").value,
  };
  try {
    if (id) await requisicao(`/alunos/${id}`, "PUT", corpo);
    else await requisicao("/alunos", "POST", corpo);
    mostrarMensagem(id ? "Aluno atualizado!" : "Aluno cadastrado!");
    limparFormAluno();
    carregarAlunos();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
});

async function excluirAluno(id) {
  if (!confirm("Excluir este aluno?")) return;
  try {
    await requisicao(`/alunos/${id}`, "DELETE");
    mostrarMensagem("Aluno excluído.");
    carregarAlunos();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
}

// ---------- LIVROS ----------
async function carregarLivros() {
  const livros = await requisicao("/livros");
  const tbody = document.getElementById("tabela-livros");
  tbody.innerHTML = livros.length ? "" : '<tr><td colspan="5" class="vazio">Nenhum livro cadastrado.</td></tr>';
  livros.forEach(l => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapar(l.titulo)}</td><td>${escapar(l.autor)}</td><td>${l.ano ?? "—"}</td>
      <td><span class="badge ${l.disponivel ? "ok" : "no"}">${l.disponivel ? "Disponível" : "Emprestado"}</span></td>
      <td>
        <button class="pequeno">Editar</button>
        <button class="pequeno perigo">Excluir</button>
      </td>`;
    const [bEditar, bExcluir] = tr.querySelectorAll("button");
    bEditar.onclick = () => editarLivro(l);
    bExcluir.onclick = () => excluirLivro(l.id);
    tbody.appendChild(tr);
  });
  return livros;
}

function editarLivro(l) {
  document.getElementById("livro-id").value = l.id;
  document.getElementById("livro-titulo").value = l.titulo;
  document.getElementById("livro-autor").value = l.autor;
  document.getElementById("livro-ano").value = l.ano ?? "";
  document.getElementById("livro-salvar").textContent = "Salvar";
  document.getElementById("livro-cancelar").classList.remove("oculto");
}

function limparFormLivro() {
  document.getElementById("form-livro").reset();
  document.getElementById("livro-id").value = "";
  document.getElementById("livro-salvar").textContent = "Cadastrar";
  document.getElementById("livro-cancelar").classList.add("oculto");
}

document.getElementById("livro-cancelar").onclick = limparFormLivro;

document.getElementById("form-livro").addEventListener("submit", async e => {
  e.preventDefault();
  const id = document.getElementById("livro-id").value;
  const corpo = {
    titulo: document.getElementById("livro-titulo").value,
    autor: document.getElementById("livro-autor").value,
    ano: document.getElementById("livro-ano").value,
  };
  try {
    if (id) await requisicao(`/livros/${id}`, "PUT", corpo);
    else await requisicao("/livros", "POST", corpo);
    mostrarMensagem(id ? "Livro atualizado!" : "Livro cadastrado!");
    limparFormLivro();
    carregarLivros();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
});

async function excluirLivro(id) {
  if (!confirm("Excluir este livro?")) return;
  try {
    await requisicao(`/livros/${id}`, "DELETE");
    mostrarMensagem("Livro excluído.");
    carregarLivros();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
}

// ---------- EMPRÉSTIMOS ----------
async function carregarEmprestimos() {
  const [alunos, livros, emprestimos] = await Promise.all([
    requisicao("/alunos"), requisicao("/livros"), requisicao("/emprestimos"),
  ]);

  const selAluno = document.getElementById("emp-aluno");
  selAluno.innerHTML = '<option value="">Selecione o aluno</option>' +
    alunos.map(a => `<option value="${a.id}">${escapar(a.nome)} (${escapar(a.matricula)})</option>`).join("");

  const selLivro = document.getElementById("emp-livro");
  const disponiveis = livros.filter(l => l.disponivel);
  selLivro.innerHTML = '<option value="">Selecione o livro</option>' +
    disponiveis.map(l => `<option value="${l.id}">${escapar(l.titulo)} — ${escapar(l.autor)}</option>`).join("");

  const tbody = document.getElementById("tabela-emprestimos");
  tbody.innerHTML = emprestimos.length ? "" : '<tr><td colspan="5" class="vazio">Nenhum empréstimo registrado.</td></tr>';
  emprestimos.forEach(e => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapar(e.aluno_nome)}</td><td>${escapar(e.livro_titulo)}</td>
      <td>${formatarData(e.data_emprestimo)}</td><td>${formatarData(e.data_devolucao)}</td>
      <td>${e.data_devolucao ? "—" : '<button class="pequeno">Devolver</button>'}</td>`;
    const btn = tr.querySelector("button");
    if (btn) btn.onclick = () => devolver(e.id);
    tbody.appendChild(tr);
  });
}

document.getElementById("form-emprestimo").addEventListener("submit", async e => {
  e.preventDefault();
  try {
    await requisicao("/emprestimos", "POST", {
      aluno_id: document.getElementById("emp-aluno").value,
      livro_id: document.getElementById("emp-livro").value,
    });
    mostrarMensagem("Empréstimo registrado!");
    carregarEmprestimos();
    carregarLivros();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
});

async function devolver(id) {
  try {
    await requisicao(`/emprestimos/${id}/devolver`, "PUT");
    mostrarMensagem("Livro devolvido!");
    carregarEmprestimos();
    carregarLivros();
  } catch (err) { mostrarMensagem(err.message, "erro"); }
}

// ---------- início ----------
carregarAlunos();
carregarLivros();
