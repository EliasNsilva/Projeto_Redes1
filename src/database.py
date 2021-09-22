import json

def abrir(): #retorna os dados da base de dados
    json_file = open("data.json","r", encoding="utf-8")
    dicionario = json.load(json_file)
    json_file.close()
    return dicionario


def atualizar(data): #atualisa a base de dados 
    file2= open("data.json","w", encoding="utf-8")
    json.dump(data, file2)
    file2.close()