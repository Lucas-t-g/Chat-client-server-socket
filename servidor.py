import socket, sys
from time import sleep
from threading import Thread

from biblioteca import Mensagem, Cliente, APRESENTACAO, MENSAGEM

# Esta função é utlizada para rodar na thread que fica checando se
#   há novas solicitações de conexão, e aceitando-as.
def recebe_clientes():
    global s, clientes
    while True:
        conexao, endereco = s.accept()
        clientes.append(Cliente(conexao, endereco))
        print('conectado em:', endereco)

# Esta função é utilizada para chegar se cada cliente conecatado fez um novo envio de mensagem, a função acaba na primeira 
def checa_cliente(i):                   # entrada que o cliente enviar
    global clientes, grupos
    try:
        data = clientes[i].conexao.recv(1024)
    except:
        return
    # print('data' ,data)
    if data == b'':
        try:
            clientes[i].conexao.close()
            print(clientes[i].nome, "se desconectou")
            clientes.pop(i)
        except:
            return
    else:
        msg.decode(data)
        if msg.tipo == MENSAGEM:
            msg.show(detalhes=True)
            if msg.destino == '/all' or msg.destino == 'Todos': # envia a mensagem para todos os 
                for destino in clientes:                        # clientes conectados ao servidor
                    if destino.nome != msg.origem:
                        destino.conexao.sendall(msg.encode())
                sleep(0.5)
            else:
                for destino in clientes:                        # procura o destino da mensagem na lista
                    if destino.nome == msg.destino:             # de clientes conectados
                        destino.conexao.sendall(msg.encode())
                        sleep(0.5)
                        return
        elif msg.tipo == APRESENTACAO:                          # a mensagem de apresentação é enviada pelo
            clientes[i].nome = msg.origem                       # cliente apos o usuário informar seu nome
            clientes[i].show()
            print("se apresentou")

HOST = 'localhost'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
clientes = []
grupos = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('aguardando conexão com um cliente na porta:', PORT)

msg = Mensagem()
th_recebe_clientes = Thread(target=recebe_clientes)                         # cria a thread que vai ficar recepcionando
th_recebe_clientes.start()                                                  # os clientes que forem solicitando conexão

while True:
    for i, cliente in enumerate(clientes):
        if not cliente.th_escutando_servidor.is_alive():                    # caso a thread que recebe entrada do cliente acabou
            cliente.th_escutando_servidor = Thread(target=checa_cliente, args=(i,)) # cria uma nova thread para receber uma nova
            cliente.th_escutando_servidor.start()                                   # mensagem do cliente