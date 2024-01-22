import socket
from threading import Thread, Semaphore
import time


HOST = "localhost"
PORT = 8000
msg = ''

sem_thread1 = Semaphore(1)
sem_thread2 = Semaphore(0)


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        cliente.connect((HOST,PORT))
        print ("Conectado ao servidor.")
    except:
        return print("Não foi possível conectar ao servidor.")
    
    #thread1 = Thread(target=enviar_msgs, args= [cliente])
    thread1 = Thread(target=receber_msgs, args= [cliente])

    thread1.start()

#receber msgs do servidor
def receber_msgs(cliente):
    while True:
        try:
            #sem_thread1.acquire()
            msg = cliente.recv(2048).decode('utf-8')

            if msg == "-1":
                opcao = input("**** Digite a opção desejada novamente a seguir ****\n")
                cliente.send(opcao.encode('utf-8'))
            elif msg.count(',') >=1:
                tratar_vetor(msg)
            elif msg.count(',') == 0 and not msg[:9] == "solicitar":
                print(msg)    
            elif msg == "solicitar download":
                #sem_thread2.acquire()
                nome_arquivo = input("Digite o nome do arquivo para fazer download: \n")    
                cliente.send(nome_arquivo+' download'.encode('utf-8'))
                #time.sleep(20)
                #time.sleep(5)
            elif msg == "solicitar upload":
                nome_arquivo = input("Digite o nome do arquivo para fazer upload: \n")
                cliente.send(nome_arquivo+' upload'.encode('utf-8'))
            
            elif msg == "solicitar delecao":
                nome_arquivo = input("Digite o nome do arquivo para deletar: \n")
                cliente.send(nome_arquivo+' delecao'.encode('utf-8'))

        except:
            print ("Não foi possível continuar conectado ao servidor")
            cliente.close()
            
            return
        #time.sleep(8)
        
            #break
        


#menu
def menu():
    print("------------ MEUS ARQUIVOS -------------\n")  
    print("1. Listagem de arquivos do servidor")
    print("2. Listagem de arquivos do cliente")
    print("3. Download de arquivos do servidor")
    print("4. Deleção de arquivos no servidor")
    print("5. Upload de arquivos para o servidor")


#enviar msgs para o servidor
def enviar_msgs(cliente):
    while True:
        try:
            #sem_thread2.acquire()
            time.sleep(2)
            print("------------ MEUS ARQUIVOS -------------\n")  
            print("1. Listagem de arquivos do servidor")
            print("2. Listagem de arquivos do cliente")
            print("3. Download de arquivos do servidor")
            print("4. Deleção de arquivos no servidor")
            print("5. Upload de arquivos para o servidor")

            msg = input("Digite a opção desejada:\n->")
            cliente.send(msg.encode('utf-8'))

            #time.sleep(40)
           

        except:
            return
        

def tratar_vetor(msg):
    lista = []
    lista = msg.split(",")
    for item in lista:
        print (item)

 
menu()
main()