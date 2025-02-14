from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "Empresa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    cnpj: Mapped[str] = mapped_column(unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(nullable=False)

    obrigacoes_acessorias: Mapped[List["ObrigacaoAcessoria"]] = (
        relationship("ObrigacaoAcessoria", back_populates="empresa", lazy="joined", cascade="all, delete-orphan"))

class ObrigacaoAcessoria(Base):
    __tablename__ = "ObrigacaoAcessoria"

    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str] = mapped_column(nullable=False)
    periodicidade:Mapped[str] = mapped_column(nullable=False)
    empresa_id:Mapped[int] = mapped_column(ForeignKey("Empresa.id", ondelete="CASCADE"))

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="obrigacoes_acessorias")
