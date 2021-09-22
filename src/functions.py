import os
import time

def clear():
    os.system('cls||clear')

def CreateAcc(): #cria uma conta 
    clear()
    while True:
        print("CRIAR CONTA:")
        login = input("Login(esse será seu nick no chat): ")
        senha = input("Senha: ")
        confirmSenha = input("Confirme a Senha: ")
        if senha == confirmSenha:
            clear()
            print("CONTA CRIADA!")
            time.sleep(1)
            clear()
            print("Login e senha registrados com sucesso!")
            time.sleep(2)
            return login,senha
        else:
            print("Senhas diferentes, tente novamente!")
            time.sleep(1)
            clear()