import socket
import threading

HOST1='localhost'
PORT1=1025
HOST2='localhost'
PORT2=1025
s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tcp.bind((HOST2, PORT2))
s_tcp.listen(3)

def clientenuevo(cliente, direccion):
    print("El cliente con IP y puerto: " +str(direccion))
    while True:
        mensaje = cliente.recv(1024)
        if mensaje.decode() == 'adios':
            break
        print("El cliente: "+mensaje.decode())
        reply = mensaje.decode()
        cliente.sendall(reply.encode('utf-8'))
    print(f"El cliente con IP y puerto: " +str(direccion)+" se desconectó")
    cliente.close()

while True:
    try:
        cliente, direccion = s_tcp.accept()
        threading._start_new_thread(clientenuevo,(cliente, direccion))
    except Exception:
        print("El cliente no es un participante")

s_tcp.close()