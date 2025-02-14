from typing import Literal, List
from pydantic import BaseModel, constr, field_validator, EmailStr
import re

class ObrigacaoAcessoriaCreate(BaseModel):
    nome: constr(min_length=2)
    periodicidade: Literal["mensal", "trimestral", "anual"]
    empresa_id: int

    @field_validator("nome", "periodicidade", mode="before")
    @classmethod
    def transformar_lower(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value

class ObrigacaoAcessoriaUpdate(BaseModel):
    nome: constr(min_length=2)
    periodicidade: Literal["mensal", "trimestral", "anual"]

    @field_validator("nome", "periodicidade", mode="before")
    @classmethod
    def transformar_lower(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value


class ObrigacaoAcessoriaResponse(ObrigacaoAcessoriaCreate):
    id: int
    class Config:
        from_attributes = True

class EmpresaCreate(BaseModel):
    nome:constr(min_length=2)
    cnpj: str
    endereco: str
    email: EmailStr
    telefone: str

    @field_validator("cnpj")
    @classmethod
    def validar_cnpj(cls, value: str) -> str:
        cnpj_limpo = re.sub(r"\D", "", value)
        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ deve ter 14 digitos!")
        return cnpj_limpo

    @field_validator("nome", "email", mode="before")
    @classmethod
    def transformar_lower(cls, value: str) -> str:
        return value.lower() if isinstance(value, str) else value

class EmpresaResponse(EmpresaCreate):
    id: int
    obrigacoes_acessorias: List[ObrigacaoAcessoriaResponse]
    class Config:
        from_attributes = True

