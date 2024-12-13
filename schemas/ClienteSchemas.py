from pydantic import BaseModel
from typing import Optional, List
from model.Cliente import Cliente
from datetime import date,datetime

class ClienteSchema(BaseModel):
    """ Cadastra um novo cliente na base de dados
    """
    cpf: str 
    nome: str 
    data_nascimento: date
    celular: str 
    email: str 
    margem: Optional[float] = None

class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado após seu cadastro
    """
    cpf: int = 14773253797
    nome: str = "Leonardo de Magalhaes Lecques"
    data_nascimento: date = date(1995, 5, 20)
    celular: int = 21986064010
    email: str = "leonardolecques@hotmail.com" 
    data_insercao: date = datetime.now()
    margem: float = 450.99
    id: int = 1

def apresenta_cliente_cadastrado(cliente):
    """ Retorna uma representação do Cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    result = {
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "data_nascimento": cliente.data_nascimento,
        "celular": cliente.celular,
        "data_insercao": cliente.data_insercao,
        "margem": cliente.margem,
        "email": cliente.email,
        "data_insercao": cliente.data_insercao,
        "id": cliente.id
    }

    return {"cliente": result}


class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes será retornada.
    """
    clientes:List[ClienteSchema]


def consulta_todos_clientes(clientes: List[Cliente]):
    """ Retorna uma representação de todos os clientes cadastrados
    no banco de dados
    """
    result = []
    for cliente in clientes:
        result.append({
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "data_nascimento": cliente.data_nascimento,
        "celular": cliente.celular,
        "data_insercao": cliente.data_insercao,
        "margem": cliente.margem,
        "email": cliente.email,
        "data_insercao": cliente.data_insercao,
        "id": cliente.id
    })
    return {"clientes": result}

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    cpf: Optional[str] = None
    email: Optional[str] = None
    celular: Optional[str] = None

def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    return {
        "cpf": cliente.cpf,
        "nome": cliente.nome,
        "data_nascimento": cliente.data_nascimento,
        "celular": cliente.celular,
        "data_insercao": cliente.data_insercao,
        "margem": cliente.margem,
        "email": cliente.email,
        "data_insercao": cliente.data_insercao,
        "id": cliente.id
    }

class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    cpf: str

class ClienteAtualizaSchema(BaseModel):
    cpf: str
    celular: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    margem: Optional[float] = None