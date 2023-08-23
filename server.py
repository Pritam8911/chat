import threading
import socket
host='127.0.0.1'
port=59000
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
nickNames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_clients(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickName=nickNames[index]
            broadcast(f'{nickName} has left'.encode('utf-8'))
            nickNames.remove(nickName)
            break

def receive():
    while True:
        print('Server is ready to receive connection from clients')
        client, address = server.accept()
        print(f'Successfully connected with {str(address)}')
        client.send('nickName?'.encode('utf-8'))
        nickName = client.recv(1024)
        nickNames.append(nickName)
        clients.append(client)
        print(f'The nickname of this client is {nickName}'.encode('utf-8'))
        broadcast(f'{nickName} just connected for gossiping '.encode('utf-8'))
        client.send('You are now connected'.encode('utf-8'))
        thread = threading.Thread(target=handle_clients, args =(client,))
        thread.start()

receive()