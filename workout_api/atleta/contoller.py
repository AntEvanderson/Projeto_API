import datetime
from http.client import HTTPException
from uuid import uuid4
from fastapi import APIRouter, Body, status
from pydantic import UUID4

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_de_treinamentos.models import CentroTreinamentoModel
from workout_api.contrib.dependecies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()
@router.post(path='/', 
    summary="Criar um novo atetla",
    status_code=status.HTTP_201_CREATED
    )
async def post(db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
    ):
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
        ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_name} não foi encontrada"
        )
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
        ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento} não foi encontrada")

    try:
        atleta_out = AtletaOut(id = uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria, centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
    except Exception:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados no banco")

    return atleta_out

    @router.get(path='/', 
    summary="Consultar todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model= list[AtletaOut],
    )

    async def query(db_session: DatabaseDependency)-> list[AtletaOut]:
        atletas: AtletaOut = (await db_session.execute(select(AtletaModel))).scalars().all()
    
    return[AtletaOut.model_validate(atleta) for atleta in atletas]              

@router.get(
'/{id}',
summary= "Consulta um atleta pelo id",
status_code=status.HTTP_200_OK,
response_model=AtletaOut,
)

async def query(db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut =(
        await db_session.execute(select(AtletaModel)).filter_by(id=id)
    ).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado pelo id:{id}"
        )
    
    return atleta

@router.patch(
'/{id}',
summary= "Consulta um atleta pelo id",
status_code=status.HTTP_200_OK,
response_model=AtletaOut,
)

async def get(id:UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut =(
        await db_session.execute(select(AtletaModel)).filter_by(id=id)
    ).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado pelo id:{id}"
        )
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.itens():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(
'/{id}',
summary= "Deletar um atleta pelo id",
status_code=status.HTTP_204_NO_CONTENT,
)

async def get(db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut =(
        await db_session.execute(select(AtletaModel)).filter_by(id=id)
    ).scalars().first()
    if not atleta:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado pelo id:{id}"
        )
    await db_session.delete(atleta)
    await db_session.commit()
    return atleta