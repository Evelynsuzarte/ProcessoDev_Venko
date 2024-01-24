import socket
from threading import Thread
import time
import pickle


HOST = "localhost"
PORT = 8000


"""
Função main que inicializa o cliente, conectando ao servidor, e a thread
"""
def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        cliente.connect((HOST,PORT))
        print ("Conectado ao servidor.\n")
        print("Cliente ip/porta: ",cliente.getsockname())
        enviar_msgs(cliente)
    except:
        print("Não foi possível conectar ao servidor.")
        cliente.close()
        time.sleep(5)
        
        
        
    thread1 = Thread(target=receber_msgs, args= [cliente])
    thread1.start()

    
"""
Função para a Thread, recebe as mensagens que o servidor envia
    
    :param parametro1: cliente.
    :tipo parametro1: socket.

"""
def receber_msgs(cliente):
    while True:
        try:
            objeto_msg = cliente.recv(2048)
            objeto = deserializar(objeto_msg)
            msg = objeto["comando"]

            if msg == "listagem_servidor":
                tratar_vetor(objeto["dados"])
                time.sleep(2)
                enviar_msgs(cliente)

            if msg == "listagem_cliente":
                tratar_vetor(objeto["dados"])
                time.sleep(2)
                enviar_msgs(cliente)

            elif msg == "solicitar_download":
                tratar_vetor(objeto["dados"])
                print("----------- ÁREA DE DOWNLOAD -----------\n")
                nome_arquivo = input("Digite o nome do arquivo para fazer download: \n")    
                enviar_estrutura_msg("solicitar_download", nome_arquivo, cliente)
            
            elif msg == "solicitar_delecao":
                tratar_vetor(objeto["dados"])
                print("----------- ÁREA DE DELEÇÃO -----------\n")
                nome_arquivo = input("Digite o nome do arquivo para fazer deleção: \n")
                enviar_estrutura_msg("solicitar_delecao", nome_arquivo, cliente)
            
            elif msg == "solicitar_upload":
                tratar_vetor(objeto["dados"])
                print("----------- ÁREA DE UPLOAD -----------\n")
                nome_arquivo = input("Digite o nome do arquivo para fazer upload: \n")
                enviar_estrutura_msg("solicitar_upload", nome_arquivo, cliente)
            
            elif msg == "retorno":
                msg_retorno = objeto["dados"]
                print (msg_retorno)
                time.sleep(2)
                enviar_msgs(cliente)
            
        except:
            print ("Não foi possível continuar conectado ao servidor")
            cliente.close()
            return
        


"""
Envia a mensagem referente as opções do menu
    
    :param parametro1: cliente
    :tipo parametro1: socket

"""
def enviar_msgs(cliente):
        time.sleep(2)
        opcao = ""
        print("------------ MEUS ARQUIVOS -------------\n")  
        print("1. Listagem de arquivos do servidor")
        print("2. Listagem de arquivos do cliente")
        print("3. Download de arquivos do servidor")
        print("4. Deleção de arquivos no servidor")
        print("5. Upload de arquivos para o servidor")

        msg = input("Digite a opção desejada:\n->")
        if msg == "1": 
            opcao = "listagem_servidor"
        elif msg == "2": 
            opcao = "listagem_cliente"
        elif msg == "3": 
            opcao = "download"
        elif msg == "4": 
            opcao = "delecao"
        elif msg == "5": 
            opcao = "upload" 
        else:
            print("Opção digitada inexistente! Selecione a opção correta.")
            enviar_msgs(cliente)

        enviar_estrutura_msg(opcao, ' ', cliente)


"""
Trata a string de lista de arquivos recebido, transformando em uma lista e exibindo
    
    :param parametro1: msg.
    :tipo parametro1: string.

"""
def tratar_vetor(msg):
    lista = []
    lista = msg.split(",")
    for item in lista:
        print (item)


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
    msg = {"comando":comando,"dados":dados}
    obj_serial = serializar(msg)
    cliente.send(obj_serial)


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
Função que deserializa uma mensagem depois de ser recebida via socket
    :param parametro1: objeto.
    :tipo parametro1: string.
    :return: Objeto deserializado.
    :rtipo: dicionario.
"""
def deserializar(objeto_recebido):
    objeto = pickle.loads(objeto_recebido)
    return objeto


#--------------------------
main()