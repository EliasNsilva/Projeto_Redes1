import socket
import threading
import database

address = ("localhost", 20000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen()
dados = database.abrir() #pegando dados do da base de dados
print("Servidor Iniciado.")

clientes = []

def send_messages(issuer, message): #função para enviar as mensagem a todos do chat menos ao remetente
    for i in range(len(clientes)):
        if (clientes[i] != issuer):
            clientes[i].send(message)

def process(server_input,address):
    while True: 
        response = server_input.recv(1024).decode('UTF-8')
        if (response == "CC"):
            login = server_input.recv(1024).decode('UTF-8')
            server_input.send("L_OK".encode('UTF-8'))
            senha = server_input.recv(1024).decode('UTF-8')
            server_input.send("S_OK".encode('UTF-8'))

            dados[login] = senha
            database.atualizar(dados) #adiciona o usuario da base de dados

        elif(response == "CHAT"):
            login = server_input.recv(1024).decode('UTF-8')
            senha = server_input.recv(1024).decode('UTF-8')

            if login in dados: #verifica ser o usuario é valido
                if dados[login] == senha:
                    server_input.send("!OK".encode('UTF-8')) #envia um codigo de validação de usuario ao cliente

                    mess = "**{} {}**".format(login,"Entrou no chat! =)")
                    send_messages(server_input, mess.encode('UTF-8'))

                    clientes.append(server_input) #adiciona o cliente a lista de usuarios conectados

                    while True:
                        try:
                            response = server_input.recv(1024).decode('UTF-8')
                            if response == "/SAIR":
                                server_input.send("/SAIR".encode('UTF-8'))

                                mess = "**{} {}**".format(login,"Saiu do chat! ;-;")
                                send_messages(server_input, mess.encode('UTF-8'))

                                print("Conexão de {} encerrada ".format(address))

                                clientes.remove(server_input) #remove da lista de usuarios conectados 
                                break
                            else:
                                response = "{}: {}".format(login,response)
                                send_messages(server_input, response.encode('UTF-8'))
                        except:
                            server_input.close()
                            break
                else:
                    server_input.send("!LOG_ERR".encode('UTF-8')) #envia um codigo de erro ao cliente
            else:
                server_input.send("!LOG_ERR".encode('UTF-8')) #envia um codigo de erro ao cliente
            
        elif(response == "DSC"):
            print ("Conexão de {} encerrada ".format(address))


while True:
    server_input, address = server_socket.accept()

    print ("Nova conexao recebida de ", address)

    thread = threading.Thread(target=process, args=(server_input,address)) 
    thread.start()
