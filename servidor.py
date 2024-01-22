import socket
from threading import Thread, Semaphore
import os
import shutil
from datetime import datetime
import time

sem_thread1 = Semaphore(1)
sem_thread2 = Semaphore(0)


HOST = "localhost"
PORT = 8000
clientes = []
caminho_projeto = os.path.dirname(os.path.abspath("__file__"))


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    #inicialização de servidor
    try:
        servidor.bind((HOST,PORT))
        servidor.listen()
        print ("Servidor inicializado.")
        escrever_log('Servidor iniciado')
    except:
        escrever_log('Não possível inicializar o servidor.')
        print ("Não possível inicializar o servidor.")
        return
    
    #adiciona cliente na lista de clientes e cria uma thread para ele
    while True:
        cliente, addr = servidor.accept()
        clientes.append(cliente)
        print("Cliente conectado:",addr)
        escrever_log('Cliente conectado '+str(addr[1]))

        thread = Thread(target=processar_msgs, args=[cliente])
        thread.start()

#processa as msgs enviadas pelo cliente
def processar_msgs(cliente):
    while True:
        #retorno = []
        try:
            msg = cliente.recv(1024).decode('utf-8')
            #sem_thread1.release()

            if msg[-8:] == "download":
                nome_arquivo = msg.split()[0]
                copiar_arquivo("SERVIDOR","CLIENTE",nome_arquivo)
                print("Download realizado com êxito!")
                enviar_msgs(cliente,"---------- Arquivos cliente ----------")
                arquivos = listar_arquivos("CLIENTE")     
                enviar_msgs(cliente, arquivos)
                escrever_log('Solicitação de download de arquivos do servidor')
                #time.sleep(5)
            
            elif msg[-7:] == "delecao":
                nome_arquivo = msg.split()[0]
                deletar_arquivo(nome_arquivo)
                enviar_msgs(cliente,"---------- Arquivos servidor ----------")
                arquivos = listar_arquivos("SERVIDOR")
                enviar_msgs(cliente, arquivos)
                escrever_log('Solicitação de deleção de arquivos do servidor')
                time.sleep(2)
            
            elif msg[-6:] == "upload":
                nome_arquivo = msg.split()[0]
                copiar_arquivo("CLIENTE","SERVIDOR",nome_arquivo)
                print("Upload realizado com êxito!")
                enviar_msgs(cliente,"---------- Arquivos servidor ----------")
                arquivos = listar_arquivos("SERVIDOR") 
                enviar_msgs(cliente, arquivos)
                escrever_log('Solicitação de upload de arquivos para o servidor')
                time.sleep(2)

            elif msg == '1':
                enviar_msgs(cliente,"---------- Listagem de arquivos do servidor----------")
                arquivos = listar_arquivos("SERVIDOR")
                enviar_msgs(cliente, arquivos)
                escrever_log('Solicitação de listagem de arquivos do servidor ')
                time.sleep(2)

            elif msg == '2':
                enviar_msgs(cliente,"---------- Listagem de arquivos do cliente----------")
                arquivos = listar_arquivos("CLIENTE")
                enviar_msgs(cliente,arquivos)
                escrever_log('Solicitação de listagem de arquivos do cliente')
                time.sleep(2)

            elif msg == '3':
                enviar_msgs(cliente,"---------- Download de arquivos do servidor----------")
                arquivos = listar_arquivos("SERVIDOR")
                enviar_msgs (cliente,arquivos)
                enviar_msgs (cliente,"solicitar download")
                time.sleep(2)
                          
            elif msg == '4':
                enviar_msgs(cliente,"---------- Deleção de arquivos no servidor ----------")
                arquivos = listar_arquivos("SERVIDOR")
                enviar_msgs (cliente,arquivos)
                enviar_msgs (cliente,"solicitar delecao")

                #time.sleep(1)
                  
            elif msg == '5':
                enviar_msgs(cliente,"----------Upload de arquivos para o servidor ----------")
                arquivos = listar_arquivos("CLIENTE")
                enviar_msgs (cliente,arquivos)
                enviar_msgs (cliente,"solicitar upload")

                #time.sleep(1)
                
            else:
                print ("Opção desejada não existente!!")
                msg = "-1"
                enviar_msgs(cliente,msg.encode('utf-8'))

        except:
            delete_cliente(cliente)
            time.sleep(5)
            #escrever_log('Cliente removido: '+cliente)
            #break
        #sem_thread1.release()
       

#deletar clientes que não estão mais conectados
def delete_cliente(cliente):
    clientes.remove(cliente)


#enviar msg para cliente
def enviar_msgs(cliente, msg):
    try:
        cliente.send(msg.encode('utf-8'))
    except:
        delete_cliente(cliente)

#funções de manipulação de arquivos --------------------------------
def listar_arquivos(pasta):
    lista = []
    caminho_pasta = os.path.join(caminho_projeto,pasta)
    arquivos_na_pasta = os.listdir(caminho_pasta)
    for arquivo in arquivos_na_pasta:
        nome = os.path.basename(arquivo)
        lista.append(nome)
    msg = tratar_vetor(lista)
    return msg

def copiar_arquivo(origem, destino, nome_arquivo):
    caminho_origem = os.path.join(caminho_projeto, origem, nome_arquivo)
    caminho_destino = os.path.join(caminho_projeto, destino)
    shutil.copy2(caminho_origem, caminho_destino)

def deletar_arquivo(nome_arquivo):
    caminho_origem = os.path.join(caminho_projeto, 'SERVIDOR')
    caminho_excluir = os.path.join(caminho_projeto, caminho_origem, nome_arquivo)
    if os.path.exists(caminho_excluir):
        os.remove(caminho_excluir)
        print("\nArquivo excluído com sucesso.")
    else:
        print("\nO arquivo não existe.")

def escrever_log(mensagem):
    data_public = datetime.now()
    data = data_public.strftime("%d/%m/%Y %H:%M")
    arquivo = open ("logs.txt",'a')
    arquivo.write(data + " : " + mensagem+"\n")
    arquivo.close()

def tratar_vetor(vetor):
    tratado = ",".join(vetor)
    return tratado 
#-------------------------------------------------------------------
        
main()