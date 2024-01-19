import socket
from threading import Thread
import os
import shutil


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
    except:
        return print ("Não possível inicializar o servidor.")
    
    #adiciona cliente na lista de clientes e cria uma thread para ele
    while True:
        cliente, addr = servidor.accept()
        clientes.append(cliente)
        print("Cliente conectado:",addr)
        thread = Thread(target=processar_msgs, args=[cliente])
        thread.start()

#processa as msgs enviadas pelo cliente
def processar_msgs(cliente):
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if msg == '1':
                print("\n---------- Listagem de arquivos do servidor----------\n")
                listar_arquivos("SERVIDOR")
                
            elif msg == '2':
                print("\n---------- Listagem de arquivos do cliente----------\n")
                listar_arquivos("CLIENTE")
                
            elif msg == '3':
                print("\n---------- Download de arquivos do servidor----------\n")
                listar_arquivos("SERVIDOR")
                nome_arquivo = input("Digite o nome do arquivo para fazer download: \n")
                copiar_arquivo("SERVIDOR","CLIENTE",nome_arquivo)
                print("Download realizado com êxito!")
                print("\n---------- Arquivos cliente ----------")
                listar_arquivos("CLIENTE")     
                          
            elif msg == '4':
                print("\n---------- Deleção de arquivos no servidor ---------- \n")
                listar_arquivos("SERVIDOR")
                nome_arquivo = input("Digite o nome do arquivo para deletar: \n")
                deletar_arquivo(nome_arquivo)
                print("\n---------- Arquivos servidor ----------")
                listar_arquivos("SERVIDOR")
                  
            elif msg == '5':
                print("\n----------Upload de arquivos para o servidor ----------\n")
                listar_arquivos("CLIENTE")
                nome_arquivo = input("Digite o nome do arquivo para fazer upload: \n")
                copiar_arquivo("CLIENTE","SERVIDOR",nome_arquivo)
                print("Upload realizado com êxito!")
                print("\n---------- Arquivos servidor ----------")
                listar_arquivos("SERVIDOR") 
                
            else:
                print ("Opção desejada não existente!!")
                msg = "-1"
                enviar_msgs(cliente,msg.encode('utf-8'))

        except:
            delete_cliente(cliente)
            break

def delete_cliente(cliente):
    clientes.remove(cliente)

def enviar_msgs(cliente, msg):
    try:
        cliente.send(msg.encode('utf-8'))
    except:
        delete_cliente(cliente)


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

main()