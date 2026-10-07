from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.models.usuario import Usuario
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoUpdate


def get_emprestimos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Emprestimo).offset(skip).limit(limit).all()


def get_emprestimo_by_id(db: Session, emprestimo_id: int):
    return db.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()


def create_emprestimo(db: Session, emprestimo: EmprestimoCreate):
    livro = db.query(Livro).filter(Livro.id == emprestimo.livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    usuario = db.query(Usuario).filter(Usuario.id == emprestimo.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if not livro.disponivel:
        raise HTTPException(status_code=400, detail="Livro indisponível para empréstimo.")

    if emprestimo.status not in ["emprestado", "devolvido"]:
        raise HTTPException(status_code=422, detail="Status inválido.")

    db_emprestimo = Emprestimo(
        livro_id=emprestimo.livro_id,
        usuario_id=emprestimo.usuario_id,
        data_emprestimo=emprestimo.data_emprestimo,
        data_devolucao=emprestimo.data_devolucao,
        status=emprestimo.status,
    )

    livro.disponivel = False
    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo


def update_emprestimo(db: Session, emprestimo_id: int, emprestimo: EmprestimoUpdate):
    db_emprestimo = get_emprestimo_by_id(db, emprestimo_id)

    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    if emprestimo.livro_id is not None:
        livro = db.query(Livro).filter(Livro.id == emprestimo.livro_id).first()
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")
        db_emprestimo.livro_id = emprestimo.livro_id

    if emprestimo.usuario_id is not None:
        usuario = db.query(Usuario).filter(Usuario.id == emprestimo.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        db_emprestimo.usuario_id = emprestimo.usuario_id

    if emprestimo.data_emprestimo is not None:
        db_emprestimo.data_emprestimo = emprestimo.data_emprestimo

    if emprestimo.data_devolucao is not None:
        db_emprestimo.data_devolucao = emprestimo.data_devolucao

    if emprestimo.status is not None:
        if emprestimo.status not in ["emprestado", "devolvido"]:
            raise HTTPException(status_code=422, detail="Status inválido.")
        db_emprestimo.status = emprestimo.status

    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo


def delete_emprestimo(db: Session, emprestimo_id: int):
    db_emprestimo = get_emprestimo_by_id(db, emprestimo_id)

    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    db.delete(db_emprestimo)
    db.commit()
    return {"message": "Empréstimo removido com sucesso."}


def registrar_devolucao(db: Session, emprestimo_id: int):
    db_emprestimo = get_emprestimo_by_id(db, emprestimo_id)

    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")

    db_emprestimo.status = "devolvido"
    db_emprestimo.data_devolucao = db_emprestimo.data_devolucao or date.today()

    livro = db.query(Livro).filter(Livro.id == db_emprestimo.livro_id).first()
    if livro:
        livro.disponivel = True

    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo
