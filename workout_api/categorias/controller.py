from http.client import HTTPException
from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4

from workout_api.atleta.schemas import CategoriaIn
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaOut
from workout_api.centro_de_treinamentos.schemas import Categoria
from workout_api.contrib.dependecies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()
@router.post(path='/', 
    summary="Criar novo atetla",
    status_code=status.HTTP_201_CREATED
    )
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
               )-> CategoriaOut:
    
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = categoria_model(**categoria_out.model_dump())
    breakpoint()
    
    db_session.add(categoria_model)
    await db_session.commmit()

    return categoria_out
    
@router.get(path='/', 
    summary="Consulta todas as categorias",
    status_code=status.HTTP_200_OK
    )
async def query(db_session: DatabaseDependency)-> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    
    return categorias 

@router.get(path='/', 
    summary="Consulta uma categoria pelo id",
    status_code=status.HTTP_200_OK
    )
if not Categoria:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Categoria não Encontradan no id:{id}")
        
return Categoria
