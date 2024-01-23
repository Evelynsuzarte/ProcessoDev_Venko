import socket
from threading import Thread
import os
import shutil
from datetime import datetime
import time
import pickle


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
        print ("Não possível inicializar o servidor.")
        time.sleep(5)
        main()
        #return
    
    #adiciona cliente na lista de clientes e cria uma thread para ele
    while True:
        cliente, addr = servidor.accept()
        clientes.append(cliente)
        print("Cliente conectado: ", addr)

        thread = Thread(target=processar_msgs, args=[cliente])
        thread.start()

#processa as msgs enviadas pelo cliente
def processar_msgs(cliente):
    while True:
        try:
            objeto_msg = cliente.recv(2048)
            objeto = deserializar(objeto_msg)
            msg = objeto["comando"]
            msg_nome_arquivo = objeto["dados"]
            
            a, b = cliente.getsockname()
            print (a)
            print (b)
            print(clientes)

            if msg == "listagem_servidor":
                arquivos = listar_arquivos("SERVIDOR")
                enviar_estrutura_msg("listagem_servidor", arquivos, cliente)
                time.sleep(2)

            elif msg == "listagem_cliente":
                arquivos = listar_arquivos("CLIENTE")
                enviar_estrutura_msg("listagem_cliente", arquivos, cliente)
                time.sleep(2)

            elif msg == 'download':
                arquivos = listar_arquivos("SERVIDOR")
                enviar_estrutura_msg("solicitar_download", arquivos, cliente)
                time.sleep(2)
            
            elif msg == 'solicitar_download':
                copiar_arquivo("SERVIDOR","CLIENTE",msg_nome_arquivo)
                enviar_estrutura_msg("retorno", "Download realizado com êxito!", cliente)
                time.sleep(2)

            elif msg == 'delecao':
                arquivos = listar_arquivos("SERVIDOR")
                enviar_estrutura_msg("solicitar_delecao", arquivos, cliente)
                time.sleep(2)
            
            elif msg == 'solicitar_delecao':
                msg_retorno = deletar_arquivo(msg_nome_arquivo)
                enviar_estrutura_msg("retorno", msg_retorno, cliente)
                time.sleep(2)

            elif msg == 'upload':
                arquivos = listar_arquivos("CLIENTE")
                enviar_estrutura_msg("solicitar_upload", arquivos, cliente)
                time.sleep(2)
            
            elif msg == 'solicitar_upload':
                copiar_arquivo("CLIENTE","SERVIDOR",msg_nome_arquivo)
                enviar_estrutura_msg("retorno", "Upload do arquivo realizado com êxito!", cliente)
                time.sleep(2)
                          

        except:
            delete_cliente(cliente)
            time.sleep(5)
            main()
       

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
    lista.append("---------- Listagem de arquivos do "+pasta+" ----------")
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
        return "Remoção do arquivo realizado com êxito!"
    else:
        return "O arquivo não existe. Digite o nome do arquivo corretamente."

def escrever_log(mensagem):
    data_public = datetime.now()
    data = data_public.strftime("%d/%m/%Y %H:%M")
    arquivo = open ("logs.txt",'a')
    arquivo.write(data + " : " + mensagem+"\n")
    arquivo.close()

def tratar_vetor(vetor):
    tratado = ",".join(vetor)
    return tratado 

def deserializar(objeto_recebido):
    objeto = pickle.loads(objeto_recebido)
    return objeto

def serializar (objeto):
    objeto_serializado = pickle.dumps(objeto)
    return objeto_serializado

def enviar_estrutura_msg(comando, dados, cliente):
    try:
        msg = {"comando":comando,"dados":dados}
        obj_serial = serializar(msg)
        cliente.send(obj_serial)
    except:
        print('Não foi possível enviar msg')
        delete_cliente(cliente)

#-------------------------------------------------------------------
        
main()