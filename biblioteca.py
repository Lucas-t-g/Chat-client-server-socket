from threading import Thread
from sys import exit, stdout

APRESENTACAO = 'aps'
MENSAGEM = 'msg'

# A classe mensagem implementa uma estrutura que criei para armazenar os dados da mensagem,
#   como: origem, destino e conteudo
class Mensagem:
    def __init__(self, origem=None, destino=None, conteudo=None, apresentacao=False):
        self.origem = origem
        self.destino = destino
        if apresentacao:
            self.tipo = APRESENTACAO
            self.conteudo = ''
        else:
            self.conteudo = conteudo
            self.tipo = MENSAGEM
    
    # A função show mostra em terminal o conteudo de um objeto da classe Mensagem
    def show(self, detalhes=False): 
        if detalhes:
            print("{:<5}*{:>10}->{:<10}: {:<}".format(str(self.tipo), str(self.origem), str(self.destino), str(self.conteudo)))
        else:
            print("\n{}: {}".format(self.origem, self.conteudo))
            # stdout.writelines("\r{}: {}\n".format(self.origem, self.conteudo))
    
    # __repr__ é uma nomenclatura padrão do python para representar um objeto em forma de string
    def __repr__(self):
        return "{:>10}->{:<10}: {:<}".format(str(self.origem), str(self.destino), str(self.conteudo))

    # encode codifica o objeto Mensagem para uma string para serenviado via socket
    def encode(self, tipo = MENSAGEM):
        return str.encode("{}(#*#){}(#*#){}(#*#){}".format(self.tipo, self.origem, self.destino, self.conteudo))
        
    # decodifica a string para um objeto Mensagem
    def decode(self, msg):
        msg = msg.decode().split("(#*#)")
        self.tipo = msg[0]
        self.origem = msg[1]
        self.destino = msg[2]
        self.conteudo = msg[3]

# A classe Cliente é utilizadda apenas pelo programa do servidor,
#   utiliza esta classe para armazenar os dados de conexão com cada cliente
class Cliente:
    def __init__(self, conexao, endereco):
        self.conexao = conexao
        self.endereco = endereco
        self.nome = None
        self.th_escutando_servidor = Thread(target=exit)
        self.th_escutando_servidor.start()
    
    def show(self):
        print("{}".format(self.nome))