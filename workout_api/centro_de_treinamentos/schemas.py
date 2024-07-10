from typing import Annotated
from uuid import UUID4

from pydantic import Field
from workout_api.contrib.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[str, Field(description="Nome da Centro de Treinamento", example="CT King", max_length=20)]
    endereco: Annotated[str, Field(description="Nome do Endereço", example="Av. Dom Almeida Lustosa", max_length=60)]
    proprietario: Annotated[str, Field(description="Nome do Proprietario", example="Antonio", max_length=30)]
    
class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de Treinamento", examples="CT King", max_length=20)]

class CentroTreinamentoOut():
    id: Annotated[UUID4, Field(description="Identificador do centro de treinamentos")]

    

