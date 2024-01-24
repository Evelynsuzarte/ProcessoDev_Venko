import socket
from threading import Thread
import os
import shutil
import time
import pickle


HOST = "localhost"
PORT = 8000
clientes = []
caminho_projeto = os.path.dirname(os.path.abspath("__file__"))


"""
Função main que inicializa o cliente, conectando ao cliente, e a thread
"""
def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    while True:
        #inicialização de servidor
        try:
            servidor.bind((HOST,PORT))
            servidor.listen()
            print ("Servidor inicializado.")
            break
        except:
            print ("Não possível inicializar o servidor.")
            time.sleep(5)
            main()
            #return
    
    while True:
        cliente, addr = servidor.accept()
        print("Cliente conectado: ", addr)
        clientes.append(cliente)

        thread = Thread(target=processar_msgs, args=[cliente])
        thread.start()
            



"""
Função para a Thread, recebe as mensagens que o cliente envia
    
    :param parametro1: cliente.
    :tipo parametro1: socket.

"""
def processar_msgs(cliente):
    while True:
        try:
            objeto_msg = cliente.recv(2048)
            objeto = deserializar(objeto_msg)
            msg = objeto["comando"]
            msg_nome_arquivo = objeto["dados"]
            
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
                msg_retorno = copiar_arquivo("SERVIDOR","CLIENTE",msg_nome_arquivo)
                if msg_retorno == True:
                    enviar_estrutura_msg("retorno", "Download realizado com êxito!", cliente)
                else:
                    enviar_estrutura_msg("retorno", msg_retorno, cliente)
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
                msg_retorno = copiar_arquivo("CLIENTE","SERVIDOR",msg_nome_arquivo)
                if msg_retorno == True:
                    enviar_estrutura_msg("retorno", "Upload do arquivo realizado com êxito!", cliente)
                else:
                    enviar_estrutura_msg("retorno", msg_retorno, cliente)
                time.sleep(2)
                          

        except:
            print("Cliente se desconectou.")
            delete_cliente(cliente)
            cliente.close()
            time.sleep(2)
            break
            
       

"""
Deleta os clientes inativos
    
    :param parametro1: cliente.
    :tipo parametro1: socket.

"""
def delete_cliente(cliente):
    if cliente in clientes:
        clientes.remove(cliente)


#funções de manipulação de arquivos --------------------------------
        
"""
Procura os arquivos e organiza em uma string para serem listados

    :param parametro1: pasta
    :tipo parametro1: string.
    :return: Mensagem com o nome dos arquivos.
    :rtipo: string.
"""
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


"""
Procura os arquivos e organiza em uma string para serem listados

    :param parametro1: origem
    :tipo parametro1: string.
    :param parametro2: destino
    :tipo parametro2: string.
    :param parametro3: nome_arquivo
    :tipo parametro3: string.
    :return: Mensagem  de erro ou "True" para indicar sucesso.
    :rtipo: string e booleano.
"""
def copiar_arquivo(origem, destino, nome_arquivo):
    caminho_origem = os.path.join(caminho_projeto, origem, nome_arquivo)
    caminho_destino = os.path.join(caminho_projeto, destino)
    if os.path.exists(caminho_origem):
        shutil.copy2(caminho_origem, caminho_destino)
        return True
    else:
        return "Não foi possível realizar a ação, verifique o nome do arquivo."
    

"""
Procura os arquivos e organiza em uma string para serem listados

    :param parametro1: nome_arquivo
    :tipo parametro1: string.
    :return: Mensagem .
    :rtipo: string.
"""
def deletar_arquivo(nome_arquivo):
    caminho_origem = os.path.join(caminho_projeto, 'SERVIDOR')
    caminho_excluir = os.path.join(caminho_projeto, caminho_origem, nome_arquivo)
    if os.path.exists(caminho_excluir):
        os.remove(caminho_excluir)
        return "Remoção do arquivo realizado com êxito!"
    else:
        return "O arquivo não existe. Digite o nome do arquivo corretamente."


#-----------------------------------------------------------------
"""
Trata o vetor de arquivos recebido, transformando em uma string
    
    :param parametro1: msg.
    :tipo parametro1: string.
    :return: mensagem tratada .
    :rtipo: string.

"""
def tratar_vetor(vetor):
    tratado = ",".join(vetor)
    return tratado 


"""
Função que deserializa uma mensagem depois de ser recebida via socket
    :param parametro1: objeto.
    :tipo parametro1: string.
    :return: Objeto deserializado.
    :rtipo: dicionario.
"""
def deserializar(objeto_recebido):
    objeto = pickle.loads(objeto_recebido)
    return objeto


"""
Função que serializa uma mensagem que não seja uma string simples para ser enviada via socket
    :param parametro1: objeto.
    :tipo parametro1: dicionário.
    :return: Objeto serializado.
    :rtipo: obj.
"""
def serializar (objeto):
    objeto_serializado = pickle.dumps(objeto)
    return objeto_serializado


"""
Envia a mensagem desejada no formato de dicionário, mas para isso é necessário os dados de comando e as informações
    :param parametro1: comando.
    :tipo parametro1: string.
    :param parametro2: dados.
    :tipo parametro2: string.
    :param parametro3: cliente.
    :tipo parametro3: socket.
"""
def enviar_estrutura_msg(comando, dados, cliente):
    try:
        msg = {"comando":comando,"dados":dados}
        obj_serial = serializar(msg)
        cliente.send(obj_serial)
    except:
        print('Não foi possível enviar msg')

#-------------------------------------------------------------------
        
main()