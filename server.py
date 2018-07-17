from array import *
from string import Template
import socket
import os
import re
import threading
from os import path

lista = []
qtd_file = 0
arquivos = []
clientes = 0
size = 4096

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = socket.gethostname() #capturando nome do cliente
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #abrindo socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #configurações opcionais
        self.sock.bind((self.host, self.port))
        print 'Servidor Ativo'

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()  #aceitando conexão
            client.settimeout(360)
            threading.Thread(target = self.listenToClient,args = (client,address)).start() #thread
    
    def listenToClient(self,client,address):        
        lista.append(address)
        inicial = 0

        ##variáveis globais
        global clientes
        clientes += 1

        print 'Cliente ',address,' conectado'
        print 'Iniciando Negociação...'

        self.escuta(client,address)
        
        while (inicial == 0):
            data = client.recv(size)
            if(len(str(data)) > 0):
                inicial = data
                break
        print 'Mensagem Recebida !'
        if(inicial == '1'):
             print 'O Cliente deseja enviar arquivos..'
             print 'Preparando para receber o(s) arquivo(s)'
             self.receber(client,address)

        elif (inicial == '2'):
             print 'O cliente deseja receber arquivos..'
             print 'Preparando para enviar arquivos para o cliente ',address

             self.enviar(client,address)
        elif (inicial == '3'):
             print 'O cliente',address,'deseja se conectar com outros clientes'
             self.clientList(client,address)
        else:
             print 'Resposta inválida'
             client.close()
    
    def escuta(self,client,address):
        global size
        resp = 0
        print 'Esperando mensagem do cliente'
        while True:
           resp = client.recv(size)
           if(len(str(resp)) > 0):
               break;

        if(resp == '1'):
           self.receber(client, address)

        elif(resp == '2'):
           self.enviar(client, address) 

        elif(resp == '3'):
          print 'Lista de clientes'
          self.clientList(client,address)
  
        else:
            client.close()

    def enviar(self,client,address):
        global size

        if( len(arquivos) > 0):
           print 'Enviando lista para cliente'          
          
           client.send('1')
           resp__ = 0
           while True:
               resp__ = client.recv(size)
               if(int(len(resp__)) > 0):
                  break;
          
           if(resp__.strip() == '1'):
              array_size = int(len(arquivos))
              print 'Arquivos recebidos: ',array_size
              #Enviando nome dos arquivos
              clt_rsp = ','.join(arquivos)
              client.send(clt_rsp)

              resp__ = 0
              while (resp__ == 0):
                 resp__ = client.recv(size)
        
              resp__ = int(float(resp__)) - 1
              fl_send = arquivos[resp__]
              fl_send = str(fl_send.strip())
              print fl_send
              print 'resposta recebida'
              print 'abrindo arquivo...'
              f = open('recv/'+fl_send,'rb')
              
              filesize = str(os.path.getsize('recv/'+fl_send))
              client.send(filesize)
              
              print 'enviando...'
              l = f.read(size)
              total = len(l)
              while l:
                 client.send(l)
                 total = total + len(l)
                 l = f.read(size)                  
              self.escuta(client,address)      
        else:
            client.send('Não há arquivos para enviar')
            print 'Não há arquivos para enviar'
            #escuta(client)    
    
    def receber(self,client,address):       
        #variaveis globais
        global size
        global qtd_file
        resposta = 0
        dados = 0
        data = 0

        ##Esperando nome do arquivo
        while (dados == 0):
           resposta = client.recv(size)
           if(len(str(resposta)) > 0):
              break
    
        resposta = resposta.split(',')
        print 'Nome: ',resposta[0]
        print 'Tamanho: ',resposta[1]

        arquivos.append(resposta[0])
          
        print 'Preparando arquivo no servidor...'
        f = open('recv/'+resposta[0],'wb') ##prepara arquivo no servidor
        print 'arquivo criado!'
        #Mensagem de confirmação para envio
        client.send('1')
        print 'O Cliente',address,'está pronto para enviar o arquivo'
        data = client.recv(size)
        total = len(data)
        f.write(data)
        
        print 'Recebendo...'      
        while int(total) < int(resposta[1]) + 1:  
               data = client.recv(size)
               total = total + len(data)
               f.write(data) 
             
               if(int(total) == int(resposta[1])):
                 f.close()
                 client.send('1')
                 qtd_file = qtd_file + 1
                 break
        print 'Arquivo Recebido'
        self.escuta(client,address) 

    def clientList(self,client,address):
        print 'enviando lista de clientes ativos'
        global lista
        aws = 0
        lista_ = 0
        while True:
            aws = client.recv(size)
            if(int(len(aws))>0):
               break      
        client.send(str(len(lista)))
        i = 0
        if(len(lista)== 1):
            client.send(str(lista[0]))
            self.escuta(client,address)
        elif(len(lista)> 1):
             i = ','.join(map(str,lista))
             client.send(str(i))
             self.escuta(client,address)
        else:
          client.send('0')
          self.escuta(client,address)


if __name__ == "__main__":
    ThreadedServer('',23461).listen()
