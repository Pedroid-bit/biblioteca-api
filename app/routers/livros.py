from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import livro as crud_livro
from app.db.session import SessionLocal
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[LivroResponse])
def listar_livros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_livro.get_livros(db, skip=skip, limit=limit)


@router.get("/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = crud_livro.get_livro_by_id(db, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: LivroCreate, db: Session = Depends(get_db)):
    return crud_livro.create_livro(db, livro)


@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, livro: LivroUpdate, db: Session = Depends(get_db)):
    return crud_livro.update_livro(db, livro_id, livro)


@router.delete("/{livro_id}")
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    return crud_livro.delete_livro(db, livro_id)
