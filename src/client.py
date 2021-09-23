#!/usr/bin/python

import socket
import threading
import time
import functions


address = ("localhost", 20000)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

def listen(): # Função para recerber as mensagem no chat a qualquer momento
    while True:
        mes = client_socket.recv(1024).decode('UTF-8')
        if mes == "/SAIR":
            print("Até logo!")
            break
        else: 
            print(mes)

def typing():  # Função para enviar mensagens no chat a qualquer momento
    while True:
        text = input("")
        client_socket.send(text.encode('UTF-8'))
        if text == "/SAIR":
            break

def menu():
    print("Olá seja bem-vindo(a) ao Global Chat...")
    while True:
        time.sleep(2)
        functions.clear()
        print("[1] Entrar no chat \n[2] Criar conta\n[3] Sair" )
        command = input("Comando: ")

        if command == "1":
            client_socket.send("CHAT".encode('UTF-8')) #envio de codigo para o servidor
            login = input('Login:')
            senha = input('Senha:')
            if login == "" or senha == "":
                client_socket.send("!".encode('UTF-8'))
                client_socket.send("!".encode('UTF-8'))
            else:
                client_socket.send(login.encode('UTF-8'))
                client_socket.send(senha.encode('UTF-8'))

            

            code = client_socket.recv(1024).decode('UTF-8') #recebe o codigo para validar ou não o usuario

            if code == "!OK":
                functions.clear()
                print("Chat iniciado! Digite /SAIR para fechar o programa.")

                receive_thread = threading.Thread(target=typing) 
                receive_thread.start()

                write_thread = threading.Thread(target=listen)
                write_thread.start()

                break
            elif code == "!LOG_ERR":
                print("Login ou senha incorretos!")

        elif command == "2": 
            login, senha = functions.CreateAcc() #criar conta
            client_socket.send('CC'.encode('UTF-8')) #envio de codigo para o servidor receber os dados
            client_socket.send(login.encode('UTF-8'))
            client_socket.recv(1024)
            client_socket.send(senha.encode('UTF-8'))
            client_socket.recv(1024)
        elif command == "3": #fechar o programa
            print("Saindo...")
            client_socket.send("DSC".encode('UTF-8'))
            client_socket.close()
            time.sleep(2)
            break
        else:
            functions.clear()
            print("Desculpe, opção inválida.")

menu()
