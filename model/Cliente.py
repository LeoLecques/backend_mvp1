from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
import requests
from email_validator import validate_email, EmailNotValidError
from datetime import datetime



from  model import Base


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("ok_cliente",Integer, primary_key=True)
    cpf = Column("cpf", String(11), unique=True)
    nome = Column(String(140))
    celular = Column(String(11), unique=True)
    email = Column (String(50))
    margem = Column (Float, nullable=True)
    data_nascimento = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())

def __init__(self, cpf:str, nome:str, data_nascimento:str, celular:str, email:str, margem:Union[Float,None] = None,
             data_insercao:Union[DateTime, None] = None):
    """
    Cria um Cliente
    """
    self.valida_cpf(Cliente.formata_cpf(cpf))
    self.validate_celular(Cliente.formata_celular(celular))
    self.valida_email(email)
    self.cpf = Cliente.formata_cpf(cpf)
    self.nome = nome
    self.data_nascimento = Cliente.formata_data(data_nascimento)
    self.celular = Cliente.formata_celular(celular)
    self.email = email
    self.margem = margem
    self.data_insercao = data_insercao

    # Se não for informada, será o data exata da inserção no banco
    if data_insercao:
        self.data_insercao = data_insercao
            
    @staticmethod
    def formata_celular(celular: str):
        ''' Retira "(", ")", " " e "-" de um Celular, caso tenha
        '''
        return celular.replace("(","").replace(")","").replace(" ","").replace("-","")
    
    @staticmethod
    def validate_celular(celular: str):
        """
        Valida o número do celular.

        Levanta um ValueError se o celular não tiver 11 dígitos.
        """
        if len(celular) != 11 or not celular.isdigit():
            raise ValueError("O número do celular deve conter exatamente 11 dígitos numéricos (ddd+numero)")
        
    @staticmethod
    def formata_cpf(cpf: str):
        ''' Retira "." e "-" de um CPF, caso tenha
        '''
        return cpf.replace("-","").replace(".","")

    @staticmethod
    def valida_cpf(cpf: str):
        ''' Chama api externa para verificar se um CPF é válido
        '''
        api_valida_cpf = requests.get("https://api-cpf.vercel.app/cpf/valid/{}".format(cpf)).json()
        if api_valida_cpf["Valid"] == False:
            raise ValueError ("CPF inválido")
        
    @staticmethod
    def valida_email(email: str):
        try:
            # Check that the email address is valid. Turn on check_deliverability
            # for first-time validations like on account creation pages (but not
            # login pages).
            emailinfo = validate_email(email, check_deliverability=False)

            # After this point, use only the normalized form of the email address,
            # especially before going to a database query.
            email = emailinfo.normalized

        except EmailNotValidError as e:

        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.
            raise ValueError(str(e))
        
    @staticmethod
    def formata_data(data_nascimento: str):
        data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        return data_nascimento
