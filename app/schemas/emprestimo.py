from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EmprestimoBase(BaseModel):
    livro_id: int
    usuario_id: int
    data_emprestimo: date
    data_devolucao: Optional[date] = None
    status: str = "emprestado"


class EmprestimoCreate(EmprestimoBase):
    pass


class EmprestimoUpdate(BaseModel):
    livro_id: Optional[int] = None
    usuario_id: Optional[int] = None
    data_emprestimo: Optional[date] = None
    data_devolucao: Optional[date] = None
    status: Optional[str] = None


class EmprestimoResponse(EmprestimoBase):
    id: int
    modelo_config = ConfigDict(from_attributes=True)
