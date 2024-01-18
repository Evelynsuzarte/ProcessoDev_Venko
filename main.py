import socket
from threading import Thread
import time
import os
import shutil


HOST1 = "127.0.0.1"
caminho_projeto = os.path.dirname(os.path.abspath("__file__"))

#função para receber dados ao servidor
def cliente():
    #HOST = socket.gethostbyname(socket.gethostname())               # Capta o endereco IP do Servidor
    HOST = HOST1
    PORT_SERVER = 8000                                              # Porta que o Servidor esta

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #conexão TCP
    orig = (HOST, PORT_SERVER)      
    tcp.bind(orig)
    tcp.listen(2)                                                   

    try:
        con, cliente = tcp.accept()
        while True:
            print ("Conectado ao usuário")
            msg = con.recv(1024).decode()
            if msg == "1":
                print("\n---------- Listagem de arquivos do servidor----------\n")
                listar_arquivos("SERVIDOR")
            if msg == "2":
                print("\n---------- Listagem de arquivos do cliente----------\n")
                listar_arquivos("CLIENTE")
            if msg == "3":
                print("\n---------- Download de arquivos do servidor----------\n")
                listar_arquivos("SERVIDOR")
                nome_arquivo = input("Digite o nome do arquivo para fazer download: \n")
                copiar_arquivo("SERVIDOR","CLIENTE",nome_arquivo)
                print("Download realizado com êxito!")
                print("\n---------- Arquivos cliente ----------")
                listar_arquivos("CLIENTE")               
            if msg == "4":
                print("\n---------- Deleção de arquivos no servidor ---------- \n")
                listar_arquivos("SERVIDOR")
                nome_arquivo = input("Digite o nome do arquivo para deletar: \n")
                deletar_arquivo(nome_arquivo)
                print("Arquivo deletado com êxito!")
                print("\n---------- Arquivos servidor ----------")
                listar_arquivos("SERVIDOR")  
            if msg == "5":
                print("\n----------Upload de arquivos para o servidor ----------\n")
                listar_arquivos("CLIENTE")
                nome_arquivo = input("Digite o nome do arquivo para fazer upload: \n")
                copiar_arquivo("CLIENTE","SERVIDOR",nome_arquivo)
                print("Upload realizado com êxito!")
                print("\n---------- Arquivos servidor ----------")
                listar_arquivos("SERVIDOR") 

            time.sleep(4)
            if not msg: break
    finally:
        print ('Finalizando conexão do cliente',cliente)            #finaliza a conexão com o cliente
        con.close()                                                 #finaliza conexão


#função para enviar servindo como cliente --------------------------------------------------------------------------------
def servidor():
    #HOST = socket.gethostbyname(socket.gethostname())               # Endereco IP do Servidor
    HOST = HOST1
    PORT_CLIENT = 8000                                                     # Porta que o Servidor esta
    dest = (HOST, PORT_CLIENT)                                             # destino de envio

    while True:
        try:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # configuração TCP                   
            tcp.connect(dest)                                               # conectando
            
            try:
                print("------------ MEUS ARQUIVOS -------------\n")  
                print("1. Listagem de arquivos do servidor")
                print("2. Listagem de arquivos do cliente")
                print("3. Download de arquivos do servidor")
                print("4. Deleção de arquivos no servidor")
                print("5. Upload de arquivos para o servidor")
                selecao = input("Digite a opção desejada:\n")
                
                msg = selecao
                tcp.send(msg.encode('utf-8'))
 
            finally:
                print ('Finalizando conexão ao servidor')            #finaliza a conexão com o cliente
                tcp.close()
                time.sleep(2)
        except:
            print("Conexão falhou, tentaremos conectar em 10 segundos.\nCarregando...\n")
            time.sleep(10)                                          #Tempo para uma nova tentativa

#função das threads
def inicializar():

    thread1 = Thread(target=cliente)                           #Thread para envio de dados 
    thread2 = Thread(target=servidor)                          #Thread para recebimento de dados

    thread1.start()
    thread2.start()        




def listar_arquivos(pasta):
    caminho_pasta = os.path.join(caminho_projeto,pasta)
    arquivos_na_pasta = os.listdir(caminho_pasta)
    for arquivo in arquivos_na_pasta:
        print(arquivo)

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


#------------------------------------------------
inicializar()