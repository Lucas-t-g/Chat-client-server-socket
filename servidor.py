import socket, sys
from time import sleep
from threading import Thread

from biblioteca import Mensagem, Cliente, APRESENTACAO, MENSAGEM, Grupo


def recebe_clientes():
    global s, clientes
    while True:
        conexao, endereco = s.accept()
        clientes.append(Cliente(conexao, endereco))
        print('conectado em:', endereco)

def checa_cliente(i):
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
            if msg.destino == '/all' or msg.destino == 'Todos':
                for destino in clientes:
                    if destino.nome != msg.origem:
                        destino.conexao.sendall(msg.encode())
                sleep(0.5)
            elif ';' in msg.destino:
                cria_grupo = False
                msg.destino = msg.destino.replace(' ;', ';')
                msg.destino = msg.destino.replace('; ', ';')
                if '>' in msg.destino:
                    cria_grupo = True
                    msg.destino = msg.destino.replace(' >', '>')
                    msg.destino = msg.destino.replace('> ', '>')
                msg.destino = msg.destino.split(';')
                if cria_grupo:
                    msg.destino = [elem.split('>') for elem in msg.destino]
                    msg.destino = sum(msg.destino, [])
                    grupo_aux = Grupo(msg.destino.pop(0), msg.destino)
                    grupo_aux.att_membros(clientes)
                    grupos.append(grupo_aux)
                    grupo_aux.show()

                    for membro in grupo_aux.membros:
                        if membro.nome != msg.origem:
                            membro.conexao.sendall(msg.encode())
                    sleep(0.5)
                else:
                    for p_destino in clientes:
                        if p_destino.nome in msg.destino:
                            p_destino.conexao.sendall(msg.encode())
                    sleep(0.5)
            else:
                for destino in clientes:
                    if destino.nome == msg.destino:
                        destino.conexao.sendall(msg.encode())
                        sleep(0.5)
                        return
                for grupo in grupos:
                    if grupo.nome == msg.destino:
                        for membro in grupo.membros:
                            if membro.nome != msg.origem:
                                membro.conexao.sendall(msg.encode())
                        sleep(0.5)
                        return
        elif msg.tipo == APRESENTACAO:
            clientes[i].nome = msg.origem
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
th_recebe_clentes = Thread(target=recebe_clientes)
th_recebe_clentes.start()
while True:
    for i, cliente in enumerate(clientes):
        if not cliente.th_escutando_servidor.is_alive():
            cliente.th_escutando_servidor = Thread(target=checa_cliente, args=(i,))
            cliente.th_escutando_servidor.start()

for cliente in clientes:
    cliente.conexao.close()