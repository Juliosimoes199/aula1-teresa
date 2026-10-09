from google.adk.agents import Agent
from dotenv import load_dotenv
import requests

url = "https://teresa-cdc74-default-rtdb.firebaseio.com/.json"

def inserir(nome: str, email: str, idade: int) -> dict:
    """Essa função insere dados na ase de dados
    Arg: 
        nome "str" - essa variável recebe um nome
        email "str" - essa variável recebe um email
        idade "str" - essa variável recebe uma idade   
    """
    dados = {"nome": nome, "email" : email, "idade" : idade}
    recebe = requests.post(url, json = dados)
    
    return {"status" : f"{recebe}", "response": f"{recebe.json()}"}

def pegar_dados():
    """Esta função pega os dados de uma base de dados"""

    recebe = requests.get(url)
    return {"status" : f"{recebe}", "response": f"{recebe.json()}"}
    
def deletar(id_cliente: str) -> dict:
    """Essa é uma função que deleta os dados de uma tabela
    
    arg:
    id_cliente (str) : esta variável recebe o id do cliente
    """
    url_delet = f"https://teresa-cdc74-default-rtdb.firebaseio.com/{id_cliente}.json"
    deletar = requests.delete(url_delet)
    return deletar.json()

load_dotenv(override=True)

root_agent = Agent(
    name = "Agentezinho",
    model = "gemini-2.5-flash",
    instruction = """Você é um agente que capta dados de um cliente e insere na base de dados e 
    você é capaz de pesquisar os dados desse cliente no banco de dados. *inserir* use essa função para inserir dados
    *pegar_dados* use esta função para pegar os dados da base de dados. 
    *deletar*primeiro use a função *pegar_dados* para capturar o id do cliente e depois use 
    esta função para deletar os dados do cliente na tabela""",
    tools = [pegar_dados,inserir, deletar]
)