from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()


def get_usuario_by_id(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def get_usuario_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()


def create_usuario(db: Session, usuario: UsuarioCreate):
    if get_usuario_by_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = get_usuario_by_id(db, usuario_id)

    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if usuario.nome is not None:
        db_usuario.nome = usuario.nome

    if usuario.email is not None:
        existing = get_usuario_by_email(db, usuario.email)
        if existing and existing.id != usuario_id:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
        db_usuario.email = usuario.email

    if usuario.telefone is not None:
        db_usuario.telefone = usuario.telefone

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)

    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuário removido com sucesso."}
