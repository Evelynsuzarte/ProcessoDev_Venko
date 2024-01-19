import socket
from threading import Thread
import time



HOST = "localhost"
PORT = 8000


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        cliente.connect((HOST,PORT))
        print ("Conectado ao servidor.")
    except:
        return print("Não foi possível conectar ao servidor.")
    
    thread1 = Thread(target=enviar_msgs, args= [cliente])
    thread2 = Thread(target=receber_msgs, args= [cliente])

    thread1.start()
    thread2.start()


def receber_msgs(cliente):
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if msg == "-1":
                input("**** Digite a opção desejada novamente a seguir ****\n")
                #enviar_msgs(cliente)
        except:
            print ("Não foi possível continuar conectado ao servidor")
            cliente.close()
            break

def enviar_msgs(cliente):
    while True:
        try:
            #time(1)
            print("------------ MEUS ARQUIVOS -------------\n")  
            print("1. Listagem de arquivos do servidor")
            print("2. Listagem de arquivos do cliente")
            print("3. Download de arquivos do servidor")
            print("4. Deleção de arquivos no servidor")
            print("5. Upload de arquivos para o servidor")

            msg = input("Digite a opção desejada:\n->")
            cliente.send(msg.encode('utf-8'))
        except:
            return
        


main()