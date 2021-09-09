from threading import Thread
from sys import exit, stdout

APRESENTACAO = 'aps'
MENSAGEM = 'msg'
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
    
    def show(self, detalhes=False):
        if detalhes:
            print("{:<5}*{:>10}->{:<10}: {:<}".format(str(self.tipo), str(self.origem), str(self.destino), str(self.conteudo)))
        else:
            print("\n{}: {}".format(self.origem, self.conteudo))
            # stdout.writelines("\r{}: {}\n".format(self.origem, self.conteudo))
    
    def encode(self, tipo = MENSAGEM):
        return str.encode("{}(#*#){}(#*#){}(#*#){}".format(self.tipo, self.origem, self.destino, self.conteudo))
        
    def decode(self, msg):
        msg = msg.decode().split("(#*#)")
        self.tipo = msg[0]
        self.origem = msg[1]
        self.destino = msg[2]
        self.conteudo = msg[3]

class Cliente:
    def __init__(self, conexao, endereco):
        self.conexao = conexao
        self.endereco = endereco
        self.nome = None
        self.th_escutando_servidor = Thread(target=exit)
        self.th_escutando_servidor.start()
    
    def show(self):
        print("{}".format(self.nome))

class Grupo:
    def __init__(self, nome, membros):
        self.nome = nome
        self.membros = membros
    
    def att_membro(self, membro_0, membro_1):
        self.membros[ self.membros.index(membro_1.nome) ] = membro_1
    
    def att_membros(self, clientes):
        for cliente in clientes:
            if cliente.nome in self.membros:
                self.att_membro(cliente.nome, cliente)
        
        i = 0
        while i < len(self.membros):
            if type(self.membros[i]) != Cliente: self.membros.pop(i)
            else: i += 1
    
    def show(self):
        print("grupo - {}: {}".format(self.nome, [membro.nome for membro in self.membros if type(membro) == Cliente]))