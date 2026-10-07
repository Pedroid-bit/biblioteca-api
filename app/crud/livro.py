from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.livro import Livro
from app.models.usuario import Usuario
from app.schemas.livro import LivroCreate, LivroUpdate


def get_livros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Livro).offset(skip).limit(limit).all()


def get_livro_by_id(db: Session, livro_id: int):
    return db.query(Livro).filter(Livro.id == livro_id).first()


def get_livro_by_isbn(db: Session, isbn: str):
    return db.query(Livro).filter(Livro.isbn == isbn).first()


def create_livro(db: Session, livro: LivroCreate):
    if get_livro_by_isbn(db, livro.isbn):
        raise HTTPException(status_code=400, detail="ISBN já cadastrado.")

    if livro.usuario_id is not None:
        usuario = db.query(Usuario).filter(Usuario.id == livro.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db_livro = Livro(
        titulo=livro.titulo,
        autor=livro.autor,
        isbn=livro.isbn,
        ano_publicacao=livro.ano_publicacao,
        disponivel=livro.disponivel,
        usuario_id=livro.usuario_id,
    )
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro


def update_livro(db: Session, livro_id: int, livro: LivroUpdate):
    db_livro = get_livro_by_id(db, livro_id)

    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    if livro.titulo is not None:
        db_livro.titulo = livro.titulo

    if livro.autor is not None:
        db_livro.autor = livro.autor

    if livro.isbn is not None:
        existing = get_livro_by_isbn(db, livro.isbn)
        if existing and existing.id != livro_id:
            raise HTTPException(status_code=400, detail="ISBN já cadastrado.")
        db_livro.isbn = livro.isbn

    if livro.ano_publicacao is not None:
        db_livro.ano_publicacao = livro.ano_publicacao

    if livro.disponivel is not None:
        db_livro.disponivel = livro.disponivel

    if livro.usuario_id is not None:
        usuario = db.query(Usuario).filter(Usuario.id == livro.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        db_livro.usuario_id = livro.usuario_id

    db.commit()
    db.refresh(db_livro)
    return db_livro


def delete_livro(db: Session, livro_id: int):
    db_livro = get_livro_by_id(db, livro_id)

    if not db_livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    db.delete(db_livro)
    db.commit()
    return {"message": "Livro removido com sucesso."}
