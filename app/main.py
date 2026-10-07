from fastapi import FastAPI

from app.routers.emprestimos import router as emprestimos_router
from app.routers.livros import router as livros_router
from app.routers.usuarios import router as usuarios_router

app = FastAPI(
    title="Biblioteca Digital API",
    description="API para gerenciamento de usuários, livros e empréstimos.",
    version="1.0.0",
)

app.include_router(usuarios_router)
app.include_router(livros_router)
app.include_router(emprestimos_router)


@app.get("/")
def home():
    return {
        "message": "Bem-vindo à Biblioteca Digital API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
