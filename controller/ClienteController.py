from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
import requests

from model import Session
from model.Cliente import *
from schemas.ClienteSchemas import *
from schemas.erroSchemas import ErrorSchema
from flask_cors import CORS

info = Info(title="CRM CORBAN INSS", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#Definir tags para Swagger
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="")

@app.get("/", tags = [home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema,"401": ErrorSchema})
def cadastra_cliente(body: ClienteSchema):
    """Realizar Cadastro de Cliente no Banco de Dados"""
    try:
        # Depurar o JSON recebido
        form_data = request.json  # Acessa o corpo da requisição diretamente
        print("Dados recebidos: ", form_data)

        # Converte o JSON para o schema Pydantic
        form = ClienteSchema(**form_data)

        cliente = Cliente(
            cpf=form.cpf,
            nome=form.nome,
            data_nascimento=form.data_nascimento,
            celular=form.celular,
            email=form.email,
            margem=form.margem
        )
        session = Session()
        session.add(cliente)
        session.commit()
        return apresenta_cliente_cadastrado(cliente), 200
    except Exception as e:
        return {"error": str(e)}, 500
    
@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema})
def consultar_todos_clientes():
    """Faz a busca por todos os clientes cadastrados
    Retorna uma representação da listagem de clientes.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    clientes = session.query(Cliente).all()

    if not clientes:
        # se não há produtos cadastrados
        return {"cliente": []}, 200
    else:
        # retorna a representação de cliente
        print(clientes)
        return consulta_todos_clientes(clientes), 200

@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema})
@app.get('/cliente', tags=[cliente_tag], responses={"200": ClienteViewSchema})
def consulta_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um cliente a partir do cpf, email ou celular"""
    session = Session()

    # Obtém os parâmetros da query
    email = request.args.get("email")
    cpf = request.args.get("cpf")
    celular = request.args.get("celular")

    cliente = None
    if cpf:
        cliente = session.query(Cliente).filter(Cliente.cpf == cpf).first()
    elif email:
        cliente = session.query(Cliente).filter(Cliente.email == email).first()
    elif celular:
        cliente = session.query(Cliente).filter(Cliente.celular == celular).first()

    if not cliente:
        return {"message": "Cliente não encontrado na base."}, 404
    return apresenta_cliente(cliente), 200

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        return {"mesage": "error_msg"}, 404
    else:
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200
 
@app.delete('/cliente', 
            tags=[cliente_tag],responses={"200": ClienteDelSchema})
def del_produto(query: ClienteBuscaSchema):
    """Deleta um Cliente a partir do CPF de cliente informado
    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_cpf = query.cpf
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Cliente removido", "id": cliente_cpf}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": "error_msg"}, 404
    
@app.put('/cliente', tags=[cliente_tag], 
         responses={"200": ClienteViewSchema})
def atualizar_cliente(body: ClienteAtualizaSchema):
    """Atualiza as informações de um cliente a partir do CPF.

    Os campos que podem ser atualizados incluem celular, email, data de nascimento e margem.
    """
    try:
        # Converte o JSON para o schema Pydantic
        dados_atualizacao = ClienteAtualizaSchema(**request.json)

        # Cria a sessão
        session = Session()

        # Busca o cliente pelo CPF
        cliente = session.query(Cliente).filter(Cliente.cpf == dados_atualizacao.cpf).first()

        if not cliente:
            # Se o cliente não foi encontrado
            return {"message": "Cliente não encontrado na base."}, 404

        # Atualiza os campos fornecidos no body
        if dados_atualizacao.celular:
            cliente.celular = dados_atualizacao.celular
        if dados_atualizacao.email:
            cliente.email = dados_atualizacao.email
        if dados_atualizacao.data_nascimento:
            cliente.data_nascimento = dados_atualizacao.data_nascimento
        if dados_atualizacao.margem:
            cliente.margem = dados_atualizacao.margem

        # Salva as alterações
        session.commit()

        # Retorna o cliente atualizado
        return apresenta_cliente(cliente), 200
    except Exception as e:
        return {"error": str(e)}, 500

#inicia um servidor web Flask que permite a aplicação responder a requisições HTTP na rede
def cliente_view():
    app.run(host="0.0.0.0", port=5000, debug = True)