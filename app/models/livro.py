from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(200), nullable=False)
    isbn = Column(String(30), unique=True, nullable=False, index=True)
    ano_publicacao = Column(Integer, nullable=False)
    disponivel = Column(Boolean, default=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    usuario = relationship("Usuario", back_populates="livros")
    emprestimos = relationship("Emprestimo", back_populates="livro")
