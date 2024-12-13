 # Corban Manager

A motivação para o desenvolvimento deste projeto foi atender à necessidade de pequenas instituições financeiras, que enfrentam dificuldades em oferecer uma camada eficiente de operações e gestão para seus correspondentes bancários.

O projeto foi implementado utilizando tecnologias robustas e acessíveis. No backend, foram empregadas Python e SQLite, garantindo confiabilidade e eficiência no processamento de dados. Para o frontend, foram utilizadas HTML, CSS, Bootstrap e JavaScript, proporcionando uma interface intuitiva e responsiva para os usuários.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Criação Ambiente Virtual
```
python -m venv .venv
```
Ativação Ambiente Virtual (Windows)
```
.\.venv\Scripts\activate
```
Instalação bibliotecas do arquivo `requirements.txt`.
```
(env)$ pip install -r requirements.txt
```

Para executar a API  basta executar:

```
(env)$ python app.py
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.