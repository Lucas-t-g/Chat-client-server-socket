import socket, sys
from threading import Thread
from time import sleep

from biblioteca import Mensagem, APRESENTACAO, MENSAGEM

def escuta_servidor(servidor):
    while True:
        msg = Mensagem()
        data = servidor.recv(1024)
        if data == b'':
            try:
                servidor.close()
            except:
                return
        else:
            # print('data', data)
            msg.decode(data)
            msg.show()


print('''
->  para enviar mensagens para um grupo de outros clientes informe seus nomes separados por ';'(ponto e virgula)
        -exemplo: lucas;murilo;gabriel
->  para criar um grupo de clientes especifique o nome do grupo seguido por um '>' (maior que) e o nome dos membros separados por ';'(ponto e virgula). Obs.:após criado basta utilizar o nome do grupo como destinatario
        -exemplo: grupo1>lucas;murilo;gabriel
->  para enviar mensagem para todos os clientes coloque apenas: '/all'
''')

HOST = 'localhost'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 50000

nome_origem = str(input("qual seu nome: "))
# nome_origem = 'lucas'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = Mensagem(origem=nome_origem, apresentacao=True)
s.sendall(msg.encode(tipo=APRESENTACAO))
sleep(0.5)

th_escutando_servidor = Thread(target=escuta_servidor, args=(s,))
th_escutando_servidor.start()
while th_escutando_servidor.is_alive():

    nome_destino = str(input("para quem é a mensagem:\n"))
    msg = str(input("digite sua mensagem:\n"))
    msg = Mensagem(nome_origem, nome_destino, msg)
    s.sendall(msg.encode())
    sleep(0.5)