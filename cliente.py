import socket
from threading import Thread
import time
import mensagem
import pickle


HOST = "localhost"
PORT = 8000


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        cliente.connect((HOST,PORT))
        print ("Conectado ao servidor.\n")
        print("Cliente ip/porta: ",cliente.getsockname())
        enviar_msgs(cliente)
    except:
        print("Não foi possível conectar ao servidor.")
        time.sleep(5)
        main()
        #return 
        
  
    thread1 = Thread(target=receber_msgs, args= [cliente])
    thread1.start()

    

#receber msgs do servidor
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
        



#enviar msgs para o servidor
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
        
def tratar_vetor(msg):
    lista = []
    lista = msg.split(",")
    for item in lista:
        print (item)

def enviar_estrutura_msg(comando, dados, cliente):
    msg = {"comando":comando,"dados":dados}
    obj_serial = serializar(msg)
    cliente.send(obj_serial)
                   
def serializar (objeto):
    objeto_serializado = pickle.dumps(objeto)
    return objeto_serializado

def deserializar(objeto_recebido):
    objeto = pickle.loads(objeto_recebido)
    return objeto



main()