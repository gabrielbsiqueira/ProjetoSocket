import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back

# iniciando cores 
init()

# definindo cores disponiveis 
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

#gerando uma cor aleatoria para o cliente 
client_color = random.choice(colors)

# Ip servidor 

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 #Port do servidor 
separator_token = "<SEP>" #separando o nome do cliente e a mensagem 

#iniciando TCP socket 
s = socket.socket()
print(f"[*] Conectando á  {SERVER_HOST}:{SERVER_PORT}...")
# conectando ao servidor 
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Conectado.")

# entrando com o nome do cliente 
name = input("Digite o nome : ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

#gravando a mensagem do cliente e dar um print 
t = Thread(target=listen_for_messages)
# daemon do thread para que ele termine sempre que o thread principal terminar 
t.daemon = True
#inoiciando a thread 
t.start()

while True:
    #msg que queremos enviar para o servidor 
    to_send =  input()
    #Saindo do programa 
    if to_send.lower() == 'q':
        break
    #adicionando dados de tempo e cor do remetente 
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # enciando mgs 
    s.send(to_send.encode())

# close the socket
s.close()
