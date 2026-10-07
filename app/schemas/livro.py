from typing import Optional

from pydantic import BaseModel, ConfigDict


class LivroBase(BaseModel):
    titulo: str
    autor: str
    isbn: str
    ano_publicacao: int
    disponivel: bool = True
    usuario_id: Optional[int] = None


class LivroCreate(LivroBase):
    pass


class LivroUpdate(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    isbn: Optional[str] = None
    ano_publicacao: Optional[int] = None
    disponivel: Optional[bool] = None
    usuario_id: Optional[int] = None


class LivroResponse(LivroBase):
    id: int
    modelo_config = ConfigDict(from_attributes=True)
