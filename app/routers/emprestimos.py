from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import emprestimo as crud_emprestimo
from app.db.session import SessionLocal
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoResponse, EmprestimoUpdate

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[EmprestimoResponse])
def listar_emprestimos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_emprestimo.get_emprestimos(db, skip=skip, limit=limit)


@router.get("/{emprestimo_id}", response_model=EmprestimoResponse)
def obter_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    emprestimo = crud_emprestimo.get_emprestimo_by_id(db, emprestimo_id)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")
    return emprestimo


@router.post("/", response_model=EmprestimoResponse, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(emprestimo: EmprestimoCreate, db: Session = Depends(get_db)):
    return crud_emprestimo.create_emprestimo(db, emprestimo)


@router.put("/{emprestimo_id}", response_model=EmprestimoResponse)
def atualizar_emprestimo(emprestimo_id: int, emprestimo: EmprestimoUpdate, db: Session = Depends(get_db)):
    return crud_emprestimo.update_emprestimo(db, emprestimo_id, emprestimo)


@router.patch("/{emprestimo_id}/devolucao", response_model=EmprestimoResponse)
def registrar_devolucao(emprestimo_id: int, db: Session = Depends(get_db)):
    return crud_emprestimo.registrar_devolucao(db, emprestimo_id)


@router.delete("/{emprestimo_id}")
def remover_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)):
    return crud_emprestimo.delete_emprestimo(db, emprestimo_id)
