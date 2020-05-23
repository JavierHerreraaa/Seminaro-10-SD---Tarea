import socket, threading

def aceptar():
    while True:
        s_cliente, address_cliente = servidor.accept()
        usuario = s_cliente.recv(1024)
        LISTA_SOCKETS.append((usuario, s_cliente))
        print(usuario.decode("utf-8") + " se ha conectado")
        thread_cliente = threading.Thread(target=mostrar_server, args=[usuario, s_cliente])
        thread_cliente.start()

def mostrar_server(usuario, s_cliente):
    while True:
        try:
            data = s_cliente.recv(1024)
            if data:
                print (usuario.decode("utf-8") +": "+ data.decode("utf-8"))
                enviar_usuarios(s_cliente, usuario, data)
        except Exception as x:
            print(x)
            break

def enviar_usuarios(s_cliente, usuario, msg):
    for cliente in LISTA_SOCKETS:
        if cliente[1] != s_cliente:
            auxiliar = ": "
            mensaje = usuario.decode("utf-8") + auxiliar + msg.decode("utf-8")
            cliente[1].send(bytes(mensaje,"utf-8"))

if __name__ == "__main__":
    LISTA_SOCKETS = []
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = '196.168.0.1'
    PORT = 8080

    servidor.bind((HOST, PORT))

    servidor.listen(1)
    print('Servidor con puerto: ' + str(PORT))

    thread_1 = threading.Thread(target = aceptar)
    thread_1.start()
