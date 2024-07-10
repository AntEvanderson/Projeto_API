from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api.atleta.schemas import CategoriaIn
from workout_api.centro_treinamento.models import CentroTreinamentoIn, CentroTreinamentoOut # type: ignore
from workout_api.centro_treinamento.schemas import CentroTreinamentoModel # type: ignore
from workout_api.contrib.dependecies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()
@router.post(path='/', 
    summary="Criar um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED
    )
async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)
               )-> CentroTreinamentoOut:
    
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    breakpoint()
    
    db_session.add(centro_treinamento_model)
    await db_session.commmit()

    return centro_treinamento_out
    
@router.get(path='/', 
    summary="Consulta todas os centros de treinamentos",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
    )
async def query(db_session: DatabaseDependency)-> list[CentroTreinamentoOut]:
    centros_treinamentos_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    
    return centros_treinamentos_out 

@router.get(path='/', 
    summary="Consulta um centro de treinamento pelo id",
    status_code=status.HTTP_200_OK,
    response_model= CentroTreinamentoOut,
    )
async def query(id: UUID4, db_session: DatabaseDependency)-> CentroTreinamentoOut:
    centros_treinamentos_out: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centros_treinamentos_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Centro de Treinamentos não Encontradan no id:{id}")
    
    return centros_treinamentos_out
