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

def storeMessage(msg, type):
    global ContactList, ChatBlockList, buttonGroups
    if type == "received":
        if msg.destino == "Todos":
            ContactList["Todos"].append(msg)
        elif msg.origem in ContactList:
            ContactList[msg.origem].append(msg)
        else:
            ContactList[msg.origem] = [msg]
            ChatBlockList[msg.origem] = Button(buttonGroups, x=194/2, y=32+58/2+58*len(ChatBlockList), ctt=msg.origem[:9])
    elif type == "send":
        if msg.destino in ContactList:
            ContactList[msg.destino].append(msg)
        else:
            ContactList[msg.destino] = [msg]
            ChatBlockList[msg.destino] = Button(buttonGroups, x=194/2, y=32+58/2+58*len(ChatBlockList), ctt=msg.destino[:9])

def login(win):
    win.fill(ColorSet["white"])
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

        win.fill(ColorSet["white"])
        win.blit(text, textrect)
        login_input_box.draw(win)

        pygame.display.update()
    
    win.fill(ColorSet["white"])
    # print("nome: ", login_input_box.input)
    return login_input_box.input

def CreateChatBlock(win, contact):
    global ContactList
    left = 200
    right = 1080
    n_messages = 0

    texts = []
    textsRect = []
    for msg in ContactList[contact][::-1]:

        if msg.origem == nome_origem:
            content = "{}: {}".format("Você", msg.conteudo)
            x = 1078
            adjus = -2
        else:
            content = "{}: {}".format(msg.origem, msg.conteudo)
            x = 202
            adjus = 2

        text = FONT_ASSIST_2.render(content, True, ColorSet["black"])
        textRect = text.get_rect()
        textRect.center = (int(x+text.get_width()/adjus), int(660 - 45*n_messages))

        texts.append(text)
        textsRect.append(textRect)
        n_messages += 1
    
    return texts, textsRect

HOST = 'localhost'
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 50000

pygame.init()
fps = pygame.time.Clock()
win = CreateWindow(nameWindow="Chat")

buttonGroups = pygame.sprite.Group()
ContactList = {"Todos" : []}
ChatBlockList = {"Todos" : Button(buttonGroups, x=194/2, y=32+58/2, ctt="Todos")}
CurrentChat = "Todos"
texts = []
textsRect = []

nome_origem = login(win)
pygame.display.set_caption("Chat - {}".format(nome_origem))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = Mensagem(origem=nome_origem, apresentacao=True)
s.sendall(msg.encode(tipo=APRESENTACAO))
sleep(0.5)

th_escutando_servidor = Thread(target=escuta_servidor, args=(s,), daemon=True)
th_escutando_servidor.start()

win.fill(ColorSet["white"])
input_message = InputBox(200, 720-32, 1080-200, 32, default_text="Digite uma Mensagem")
input_destino = InputBox(0, 0, 180, 32, default_text="Digite um contato", color_active=ColorSet["white"], color_inactive=ColorSet["silver"])
nome_destino = "Todos"

MainLoop = True
while th_escutando_servidor.is_alive() and MainLoop:
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False
            break

        if input_message.handle_event(event) == True and nome_destino != None and type(nome_destino) == str:
            
            msg = Mensagem(nome_origem, nome_destino, input_message.input)
            storeMessage(msg, type="send")
            s.sendall(msg.encode())
            # sleep(0.5)

        if input_destino.handle_event(event):
            nome_destino = input_destino.input

    for contact in ContactList.keys():
        button = ChatBlockList[contact]
        if button.touch:
            nome_destino = contact
            CurrentChat = contact
    if CurrentChat in ContactList.keys():
        texts, textsRect = CreateChatBlock(win, CurrentChat)

# updates na janela
    win.fill(ColorSet["white"])
    pygame.draw.rect(win, ColorSet["blue"], (0, 0, 196, 720))
    pygame.draw.rect(win, ColorSet["black"], (196, 0, 4, 720))

    buttonGroups.update()
    buttonGroups.draw(win)

    for contact in ContactList.keys():
        button = ChatBlockList[contact]
        win.blit(button.text, button.textRect)

    for text, textRect in zip(texts, textsRect):
        win.blit(text, textRect)

    input_message.update()
    input_message.draw(win)

    input_destino.update()
    input_destino.draw(win)

    pygame.display.update()

pygame.quit()
sys.exit()