"""create initial tables

Revision ID: 202610071200
Revises: 
Create Date: 2026-10-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "202610071200"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=True),
        sa.Column("criado_em", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)
    op.create_index(op.f("ix_usuarios_id"), "usuarios", ["id"], unique=False)

    op.create_table(
        "livros",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(length=200), nullable=False),
        sa.Column("autor", sa.String(length=200), nullable=False),
        sa.Column("isbn", sa.String(length=30), nullable=False),
        sa.Column("ano_publicacao", sa.Integer(), nullable=False),
        sa.Column("disponivel", sa.Boolean(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_livros_id"), "livros", ["id"], unique=False)
    op.create_index(op.f("ix_livros_isbn"), "livros", ["isbn"], unique=True)

    op.create_table(
        "emprestimos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("livro_id", sa.Integer(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("data_emprestimo", sa.Date(), nullable=False),
        sa.Column("data_devolucao", sa.Date(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["livro_id"], ["livros.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_emprestimos_id"), "emprestimos", ["id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_emprestimos_id"), table_name="emprestimos")
    op.drop_table("emprestimos")
    op.drop_index(op.f("ix_livros_isbn"), table_name="livros")
    op.drop_index(op.f("ix_livros_id"), table_name="livros")
    op.drop_table("livros")
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_index(op.f("ix_usuarios_id"), table_name="usuarios")
    op.drop_table("usuarios")
