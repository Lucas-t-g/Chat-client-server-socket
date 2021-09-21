import socket, sys
from threading import Thread
from time import sleep

from biblioteca import Mensagem, APRESENTACAO, MENSAGEM
from pygame_assist import *
from InputBox import *

# Esta função é utilizada para criar a thread que vai ficar verificando se o servidor enviou alguma mensagem.
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

# Esta função armazena as mensagens recebidas e enviadas, separando por conversas, é utilizado para criar avisualação dos chats.
def storeMessage(msg, type):
    global ContactList, ChatBlockList, buttonGroups
    if type == "received":                  # para salvar as mensagens recebidas.
        if msg.destino == "Todos":
            ContactList["Todos"].append(msg)
        elif msg.origem in ContactList:
            ContactList[msg.origem].append(msg)
        else:
            ContactList[msg.origem] = [msg]
            ChatBlockList[msg.origem] = Button(buttonGroups, x=194/2, y=32+58/2+58*len(ChatBlockList),      # cria o botção que abre o chat
                                                               ctt=msg.origem[:9])                          #  de determinada conversa.
        
    elif type == "send":                    # para salvar as mensagens enviadas.
        if msg.destino in ContactList:
            ContactList[msg.destino].append(msg)
        else:
            ContactList[msg.destino] = [msg]
            ChatBlockList[msg.destino] = Button(buttonGroups, x=194/2, y=32+58/2+58*len(ChatBlockList),     # cria o botção que abre o chat
                                                              ctt=msg.destino[:9])                          #  de determinada conversa.

# Essa função executa a tela de 'login'.
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

# Esta função lista todas as mensagens trocadas entre dois contatos, ou no chat de Todos, e cria um objeto na superficie 
# pygame para ser mostrada a mensagem na tela, e então retorna os objetos da superficie para serem desenhados na janela no loop principal.
def CreateChatBlock(win, contact):
    global ContactList
    left = 200
    right = 1080
    n_messages = 0

    texts = []
    textsRect = []
    for msg in ContactList[contact][::-1]:      # percorre a lista de mensagens com determinado contato de trás pra frente.

        if msg.origem == nome_origem:           # verifica se a mensagem foi enviada pelo usuário.
            content = "{}: {}".format("Você", msg.conteudo)
            x = 1078
            adjus = -2
        else:                                   # caso a mensagem tenha sido enviada por outo usuário.
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
ContactList = {"Todos" : []}     # uma lista para armazenar todos os contatos do usuário.
ChatBlockList = {"Todos" : Button(buttonGroups, x=194/2, y=32+58/2, ctt="Todos")} # uma lista para armazenar os botões 
                                                                                    # de chat para cada contato do usuário.
CurrentChat = "Todos"            # define qual chat está aberto atualmente.
texts = []
textsRect = []

nome_origem = login(win)    # chama a função que apresenta a tela de login.
pygame.display.set_caption("Chat - {}".format(nome_origem))     # renomeia a janela com o nome do usuário.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg = Mensagem(origem=nome_origem, apresentacao=True)
s.sendall(msg.encode(tipo=APRESENTACAO))    # após se conectar com o servidor, envia a mensagem de apresentação 
                                            # informando o nome do usuário.
sleep(0.5)

th_escutando_servidor = Thread(target=escuta_servidor, args=(s,), daemon=True)  # cria a thread que vai ficar chegando
th_escutando_servidor.start()                                                   # se há novas mensagens do servidor.

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

        if input_message.handle_event(event):    # checa se ouve um evento de 
            msg = Mensagem(nome_origem, nome_destino, input_message.input)          # entrada na InputBox de mensagem.
            storeMessage(msg, type="send")
            s.sendall(msg.encode())                                           # envia a mensagem.
            # sleep(0.5)

        if input_destino.handle_event(event):       # checa se houve uma entrada na InputBox de destinos de mensagem.
            nome_destino = input_destino.input
            if nome_destino not in ContactList.keys():
                ContactList[nome_destino] = []
                ChatBlockList[nome_destino] = Button(buttonGroups, x=194/2, y=32+58/2+58*len(ChatBlockList),     # cria o botção que abre o chat
                                                              ctt=nome_destino[:9])                          #  de determinada conversa.
            CurrentChat = nome_destino

    for contact in ContactList.keys():              # checa se clicou em outro chat de conversa para carregar as mensagens.
        button = ChatBlockList[contact]
        if button.touch:
            nome_destino = contact
            CurrentChat = contact
    if CurrentChat in ContactList.keys():           # atualiza as mensagens no chat atual.
        texts, textsRect = CreateChatBlock(win, CurrentChat)

# updates na janela, realiza todos os updates graficos necessarios para avisualização(funções: blit, draw e update).
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