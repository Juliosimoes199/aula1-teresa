import requests


url = "https://teresa-cdc74-default-rtdb.firebaseio.com/.json"

def inserir(nome: str, email: str, idade: str) -> dict:
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
    
print(inserir("Jonas", "jonas", 12))

#rl_delet = "https://teresa-cdc74-default-rtdb.firebaseio.com/-P3VlEETpojedOotar3I/.json"

#eletar = requests.delete(url_delet)

url_edit = "https://teresa-cdc74-default-rtdb.firebaseio.com/-P3VxAE8UcuQpcWlxeaA/.json"

dados_edit = {"nome": "Ana-Júlia", "email" : "anajulia@gmail.com", "idade" : 79 }

dados_new = requests.patch(url_edit, json = dados_edit)

print(dados_new.json())