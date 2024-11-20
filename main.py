from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from models.livro import Livro
from services.livro_service import carregar_livros, salvar_livros, reescreve_livros

app = FastAPI()

livros: list[Livro] = carregar_livros()

@app.get("/")
def home():
    return {"msg": "Bem vindo à API de Biblioteca"}


@app.get("/livros/quantidade")
def contar_livros():
    return {"quantidade": len(livros)}


@app.get("/livros/{livro_id}")
def ler_livro(livro_id: int) -> Livro:
    for livro in livros:
        if livro.id == livro_id:
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.get("/livros/")
def listar_livros() -> list[Livro]:
    return livros


@app.post("/livros/", status_code=HTTPStatus.CREATED)
def adicionar_livro(livro: Livro) -> Livro:
    if any(livro_atual.id == livro.id for livro_atual in livros):
        raise HTTPException(status_code=400, detail="ID já existe.")
    livros.append(livro)
    salvar_livros(livro)
    return livro


@app.put("/livro/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro) -> Livro:
    for indice, livro_atual in enumerate(livros):
        if livro_atual.id == livro_id:
            if livro_atualizado.id != livro_id:
                livro_atualizado.id = livro_id
            livros[indice] = livro_atualizado
            reescreve_livros(livros)
            return livro_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.delete("/livro/{livro_id}")
def remover_livro(livro_id: int):
    for livro in livros:
        if livro.id == livro_id:
            livros.remove(livro)
            reescreve_livros(livros)
            return {"msg": "Livro removido com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")
