from http.client import responses
from typing import List

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, subqueryload
from models import Empresa, ObrigacaoAcessoria
from schema import EmpresaCreate, EmpresaResponse, ObrigacaoAcessoriaResponse, ObrigacaoAcessoriaCreate, ObrigacaoAcessoriaUpdate
from database import generate_db

app = FastAPI(
    title="API de Empresas",
    description="API de gerenciamento de empresas",
    version="0.0.1"
)

@app.get("/empresas/{empresa_id}",
         response_model=EmpresaResponse,
         status_code=status.HTTP_200_OK,
         summary="Obter detalhes de uma empresa",
         description="Retorna os detalhes de uma empresa específica com suas obrigações acessórias.",
         responses={
             200: {"description": "Empresa encontrada e retornada com sucesso"},
             404: {"description": "Empresa não encontrada"}
         }
         )
async def get_empresa(empresa_id: int, db: Session = Depends(generate_db)):
    empresa = (
        db.query(Empresa)
        .options(subqueryload(Empresa.obrigacoes_acessorias))
        .filter(Empresa.id == empresa_id)
        .first()
    )
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")
    return empresa

@app.get("/empresas",
         response_model=List[EmpresaResponse],
         summary="Obter todas as empresas",
         description="Retorna todas as empresas no banco de dados junto com suas obrigações")
async def get_empresas(db: Session = Depends(generate_db)):
    empresas = (
        db.query(Empresa)
        .options(subqueryload(Empresa.obrigacoes_acessorias))
        .all()
    )
    if not empresas:
        raise HTTPException(status_code=404, detail="Nenhuma empresa cadastrada")
    return empresas

@app.post('/empresas/',
          response_model=EmpresaResponse,
          status_code=status.HTTP_201_CREATED,
          description="Cadastra uma empresa e retorna a empresa cadastrada",
          )
async def create_empresa(empresa: EmpresaCreate, db: Session = Depends(generate_db)):
    db_empresa = Empresa(**empresa.model_dump())
    try:
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa

    except IntegrityError as e:
        db.rollback()

        error_message = str(e.orig).lower()

        campos_duplicados = []
        if "cnpj" in error_message:
            campos_duplicados.append("CNPJ")
        if "nome" in error_message:
            campos_duplicados.append("Nome")
        if "email" in error_message:
            campos_duplicados.append("E-mail")
        if "telefone" in error_message:
            campos_duplicados.append("Telefone")
        if campos_duplicados:
            raise HTTPException(
                status_code=400,
                detail=f"Os seguintes campos já existem: {', '.join(campos_duplicados)}"
            )

        raise HTTPException(status_code=400, detail="Erro ao cadastrar empresa: Dados duplicados")

@app.post('/obrigacoes/',
          response_model=ObrigacaoAcessoriaResponse,
          status_code=status.HTTP_201_CREATED,
          description="Cadastra uma obrigação para a empresa e retorna a obrigação como resposta")
async def create_obrigacao(obrigacao: ObrigacaoAcessoriaCreate, db: Session = Depends(generate_db)):
    db_obrigacao = ObrigacaoAcessoria(**obrigacao.model_dump())
    try:
        db.add(db_obrigacao)
        db.commit()
        db.refresh(db_obrigacao)
        return db_obrigacao
    except IntegrityError as e:
        db.rollback()

        error_message = str(e.orig).lower()

        campos_duplicados = []

        if "nome" in error_message:
            campos_duplicados.append("Nome")
        if "foreign key" in error_message:
            raise HTTPException(status_code=400, detail=f"Empresa com o ID {obrigacao.empresa_id} não encontrada")

        raise HTTPException(status_code=400, detail="Erro ao cadastrar obrigação")


@app.put(path="/empresas/{empresa_id}",
        response_model=EmpresaResponse,
        status_code=status.HTTP_202_ACCEPTED,
        summary="Altera dados de uma empresa",
        description="Altera dados de uma empresa e retorna os dados modificados"
        )
async def update_empresa(empresa_id: int,empresa_update:EmpresaCreate, db : Session = Depends(generate_db)):
    empresa = (
        db.query(Empresa)
        .options(subqueryload(Empresa.obrigacoes_acessorias))
        .filter(Empresa.id == empresa_id)
        .first()
    )
    if not empresa:
        raise HTTPException(status_code=404, detail="Nenhuma empresa encontrada com o ID fornecido")

    empresa.nome = empresa_update.nome
    empresa.email = empresa_update.email
    empresa.endereco = empresa_update.endereco
    empresa.cnpj = empresa_update.cnpj

    db.commit()
    db.refresh(empresa)

    return empresa

@app.put(path="/obrigacoes/{obrigacao_id}",
        response_model=ObrigacaoAcessoriaResponse,
        status_code=status.HTTP_202_ACCEPTED,
        summary="Altera as obrigações da empresa",
        description="Altera dados de obrigação da empresa e retorna os dados modificados"
        )
async def update_obrigacoes(obrigacao_id: int, obrigacao_update: ObrigacaoAcessoriaUpdate, db: Session = Depends(generate_db)):
    obrigacao = (
        db.query(ObrigacaoAcessoria)
        .filter(ObrigacaoAcessoria.id == obrigacao_id)
        .first())

    if not obrigacao:
        raise HTTPException(status_code=404, detail="Nenhuma obrigação encontrada com o id fornecido")

    obrigacao.nome = obrigacao_update.nome
    obrigacao.periodicidade = obrigacao_update.periodicidade

    db.commit()
    db.refresh(obrigacao)

    return obrigacao

@app.delete("/empresa/{empresa_id}",
            status_code=status.HTTP_200_OK,
            summary="Deleta uma empresa",
            description="Deleta uma empresa e retorna um texto caso tenha sido deletada com sucesso"
            )
async def delete_empresa(empresa_id: int, db: Session = Depends(generate_db)):
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    db.delete(empresa)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Deletado com sucesso"})