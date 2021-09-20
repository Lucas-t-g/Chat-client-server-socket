import socket, sys
from threading import Thread
from time import sleep

from biblioteca import Mensagem, APRESENTACAO, MENSAGEM
from pygame_assist import *
from InputBox import *

def escuta_servidor(servidor):
    global ContactList
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
            storeMessage(msg, type="received")

def ex(s):
    while True:
        nome_destino = str(input("para quem é a mensagem:\n"))
        msg = str(input("digite sua mensagem:\n"))
        msg = Mensagem(nome_origem, nome_destino, msg)

        storeMessage(msg, type="send")
        s.sendall(msg.encode())
        sleep(0.5)

def storeMessage(msg, type):
    global ContactList, ChatBlockList, buttonGroups
    if type == "received":
        if msg.origem in ContactList:
            ContactList[msg.origem].append(msg)
        else:
            ContactList[msg.origem] = [msg]
            ChatBlockList[msg.origem] = Button(buttonGroups, x=194/2, y=58/2+58*len(ChatBlockList), ctt=msg.origem[:9])
    elif type == "send":
        if msg.destino in ContactList:
            ContactList[msg.destino].append(msg)
        else:
            ContactList[msg.destino] = [msg]
            ChatBlockList[msg.destino] = Button(buttonGroups, x=194/2, y=58/2+58*len(ChatBlockList), ctt=msg.destino[:9])

def login(win):
    win.fill(ColorSet["green"])
    x = 540
    y = 360
    w = 140
    h = 32
    text = FONT_ASSIST.render("LOGIN", True, ColorSet["blue"])
    textrect = text.get_rect(center=(x, y-2*h))
    
    login_input_box = InputBox(x-w/2, y-h/2, w, h, default_text="Informe seu nome")
    done = False

    while not done:
        fps.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                continue
            if login_input_box.handle_event(event) == True:
                done = True
        login_input_box.update()

        win.fill(ColorSet["green"])
        win.blit(text, textrect)
        login_input_box.draw(win)

        pygame.display.update()
    
    win.fill(ColorSet["white"])
    # print("nome: ", login_input_box.text)
    return login_input_box.text

# def CreateChatBlock(win):
#     global ContactList


# print('''
# ->  para enviar mensagens para um grupo de outros clientes informe seus nomes separados por ';'(ponto e virgula)
#         -exemplo: lucas;murilo;gabriel
# ->  para criar um grupo de clientes especifique o nome do grupo seguido por um '>' (maior que) e o nome dos membros separados por ';'(ponto e virgula). Obs.:após criado basta utilizar o nome do grupo como destinatario
#         -exemplo: grupo1>lucas;murilo;gabriel
# ->  para enviar mensagem para todos os clientes coloque apenas: '/all'
# ''')

HOST = 'localhost'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 50000

pygame.init()
fps = pygame.time.Clock()
win = CreateWindow(nameWindow="Chat")
pygame.draw.rect(win, ColorSet["blue"], (0, 0, 196, 720))
pygame.draw.rect(win, ColorSet["black"], (196, 0, 4, 720))

buttonGroups = pygame.sprite.Group()
ContactList = {}
ChatBlockList = {}

# nome_origem = str(input("qual seu nome: "))
nome_origem = login(win)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = Mensagem(origem=nome_origem, apresentacao=True)
s.sendall(msg.encode(tipo=APRESENTACAO))
sleep(0.5)

th_escutando_servidor = Thread(target=escuta_servidor, args=(s,))
th_escutando_servidor.start()

th_ex = Thread(target=ex, args=(s,))
th_ex.start()

MainLoop = True
while th_escutando_servidor.is_alive() and MainLoop:
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False
            break

        buttonGroups.update()
        buttonGroups.draw(win)
        pygame.display.update()

    # print("fffffffff")
    # print(ContactList.keys())
    # print("fffffffff")
    if len(ContactList) > 0:
        for contact in ContactList.keys():
            # print(contact)
            button = ChatBlockList[contact]
            win.blit(button.text, button.textRect)

    pygame.display.update()

pygame.quit()