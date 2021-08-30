import socket
from threading import Thread

# IP endereço do servidor 
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port a ser usada 
separador_MSG = "<SEP>" #vamos usar isso para separar o nome do cliente e a mensagem

# inicializar a lista / conjunto de todos os soquetes do cliente conectado
cliente_socket_S = set()
#Criando um TCP sokect 
s = socket.socket()
#tornar a porta uma porta reutilizável
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# ligando o soquete ao endereço que especificamos
s.bind((SERVER_HOST, SERVER_PORT))
# escute as próximas conexões
s.listen(5)
print(f"[*] Ouviando como  {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Esta função continua ouvindo uma mensagem do soquete `cs`
    Sempre que uma mensagem for recebida, transmita-a para todos os outros clientes conectados
    """
    while True:
        try:
            # continue ouvindo por uma mensagem do soquete `cs`
            msg = cs.recv(1024).decode()
        except Exception as e:
            # cliente não está mais conectado
            #remova-o do conjunto
            print(f"[!] Error: {e}")
            cliente_socket_S.remove(cs)
        else:
            # se recebemos uma mensagem, substitua o <SEP>
            # token com ":" para uma boa impressão 
            msg = msg.replace(separador_MSG, ": ")
        #iterar em todos os soquetes conectados
        for client_socket in cliente_socket_S:
            #e envie a mensagem
            client_socket.send(msg.encode())

while True:
    #
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} conectado.")
    #Continuamos atentos a novas conexões o tempo todo
    cliente_socket_S.add(client_socket)
    #inicie um novo tópico que ouça as mensagens de cada cliente
    t = Thread(target=listen_for_client, args=(client_socket,))
    #faça o daemon do thread para que ele termine sempre que o thread principal terminar
    t.daemon = True
    #iniciar o tópico
    t.start()


#fechando os soquetes do cliente
for cs in cliente_socket_S:
    cs.close()
#fechando o soquete do servidor
s.close()