from Tkinter import *
from tkFileDialog import askopenfilename
import socket
import os

size = 4096
print 'Iniciando conexão...'
class client(object):
        def __init__(self,host,port):
           sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           host = host
           port = port
           sock_.connect((host,port))
           server = sock_.getpeername()
           print 'Iniciando Negociação'
           self.opt(sock_)

        def conn(sef,host,porta):
           print 'Este modo ainda não foi implementado'
           return

        def upload(self,sock_):

           ##Nome do arquivo
           Tk().withdraw()
           filename = askopenfilename()
           pasta = os.path.dirname(filename)
           nome = os.path.basename(filename)
           ext1,ext2 = os.path.splitext(filename)

           ##Preparando arquivo para envio
           f = open(filename,'rb')
           b = int(os.path.getsize(filename))

           dados = nome+','+str(b)
           print dados
           sock_.send(dados)

           resposta = 0
           while (resposta == 0):
               resposta = sock_.recv(size)
               if(resposta == '1'):                   
                 print 'O servidor está pronto para receber o arquivo'
                 break;
           print 'Começando enviar arquivo...'
           resposta = 0
           enviado = 0
           l = f.read(size)
           while l:
              sock_.send(l)
              enviado = enviado + len(l)
              l = f.read(size)
              print 'Enviado:{0:.2f} '.format(enviado/float(b)*100)+'%'
           while(resposta == 0):
               resposta = sock_.recv(size)
               if(resposta == '1'):
                   print 'Arquivo recebido com sucesso no servidor'
                   break
           self.opt(sock_)

        def download(self,sock_):
           #variáveis
           tamanho = 0
           resposta = 0

           print 'preparando para receber arquivos...'
           print 'recebendo lista dos arquivos no servidor...'

           while True:
              resposta = sock_.recv(size)
              if(int(len(resposta)) > 0):
                break;

           if(resposta.strip() == '1'):
              sock_.send('1')
              resposta = 0
              while True:
                resposta = sock_.recv(size)
                if(int(len(resposta)) > 0):
                   break;

              resposta = resposta.split(',')
              for x in resposta:
                 print x

              t = raw_input('Que arquivo deseja baixar ?')
              sock_.send(t);
              t = int(float(t)) - 1
              print 'Preparando arquivo no servidor'
              f = open('c_recv/'+resposta[(t)],'wb')

              print 'Recebendo tamanho do arquivo'
              while True:
                 tamanho = sock_.recv(size)
                 if(int(len(tamanho))> 0):
                    break;

              print 'Pronto !'
              print 'Recebendo arquivo ',resposta[(t)]

              l = sock_.recv(size)
              f.write(l)
              total = len(l)
              while int(total) < int(tamanho) + 1:
                 l = sock_.recv(size)
                 total = total + len(l)
                 f.write(l)
                 if(int(tamanho) == int(total)):
                    f.close()
                    break;
              print 'arquivo recebido'
              self.opt(sock_)
           else:
              print 'Não há arquivos disponíveis no servidor'
              self.opt(sock_)

        def server(self,sock_):
             sock_ = sock_
             answ = 0

             host = socket.gethostname()
             socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             socket_.bind((host,23462))
             socket_.listen(1)
             clt,addr = socket_.accept()
             print 'Servidor Ativo...'

             while True:
               answ = clt.recv(size)
               if(int(len(answ)) >0):
                  break;

             answ = answ.split(',')
             print 'Nome:',answ[0]
             print 'tamanho',answ[1]

             f = open('s_recv/'+answ[0].strip(),'wb')

             l = clt.recv(size)
             f.write(l)
             total = len(l)
             while int(total) < int(answ[1]) + 1:
                     l = clt.recv(size)
                     total = total + len(l)
                     f.write(l)
                     if(int(answ[1]) == int(total)):
                        f.close()
                        break;
                     print 'arquivo recebido'

        def opt(self,sock_):
              print 'Escolha uma opção:'
              choice = raw_input('Enviar - 1 | Receber Arquivo - 2 | Enviar para outro cliente - 3 |\n4 - Receber arquivo de outro cliente |\nPara encerrar - Qualquer tecla: ')
              ##Enviando Mensagem

              if (choice == '1'):
                 sock_.send(choice)
                 self.upload(sock_)
              if (choice == '2'):
                 sock_.send(choice)
                 self.download(sock_)
              if (choice == '3'):
                 sock_.send(choice)
                # print 'Você será desconectado do servidor atual'
                #sock_.shutdown(SHUT_WR)
                #sock_.close()
                 rsp = 0
                 sock_.send('1')
                 answ = sock_.recv(size)
                 print(answ)
                 i = 0
                 rsp = sock_.recv(size)
                 print(rsp)
                 self.opt(sock_)
                 #t = raw_input('Qual cliente deseja se conectar ?')       
                 #conn(t,23462)
              if(choice == '4'):
                 self.server(sock_)
              else:
                 self.sock_.close()


#
client(socket.gethostname(),23461)






