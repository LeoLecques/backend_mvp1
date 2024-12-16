from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from model import Base
import requests

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("ok_cliente", Integer, primary_key=True)
    cpf = Column("cpf", String(11), unique=True)
    nome = Column(String(140))
    celular = Column(String(11), unique=True)
    email = Column(String(50))
    margem = Column(Float, nullable=True)
    data_nascimento = Column(DateTime)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, cpf: str, nome: str, data_nascimento: str, celular: str, email: str, margem: float = None):
        """Construtor da classe Cliente com validações"""
        self.valida_cpf(self.formata_cpf(cpf))
        self.validate_celular(self.formata_celular(celular))
        self.valida_email(email)
        self.cpf = self.formata_cpf(cpf)
        self.nome = nome
        self.data_nascimento = self.formata_data(data_nascimento)
        self.celular = self.formata_celular(celular)
        self.email = email
        self.margem = margem
        self.data_insercao = datetime.now()

    @staticmethod
    def formata_cpf(cpf: str) -> str:
        """Remove caracteres especiais do CPF"""
        return cpf.replace(".", "").replace("-", "")

    @staticmethod
    def valida_cpf(cpf: str):
        """Valida o CPF utilizando uma API externa"""
        api_valida_cpf = requests.get(f"https://api-cpf.vercel.app/cpf/valid/{cpf}").json()
        if not api_valida_cpf["Valid"]:
            raise ValueError("CPF inválido")

    @staticmethod
    def formata_celular(celular: str) -> str:
        """Remove caracteres especiais do número de celular"""
        return celular.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

    @staticmethod
    def validate_celular(celular: str):
        """Valida se o número do celular possui 11 dígitos"""
        if len(celular) != 11 or not celular.isdigit():
            raise ValueError("O número do celular deve conter exatamente 11 dígitos numéricos (ddd+numero)")

    @staticmethod
    def valida_email(email: str):
        """Valida o e-mail utilizando a biblioteca email-validator"""
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as e:
            raise ValueError(str(e))

    @staticmethod
    def formata_data(data_nascimento):
        """Formata data"""
        if isinstance(data_nascimento, datetime):
            return data_nascimento
        return datetime.strptime(data_nascimento, "%d/%m/%Y")


