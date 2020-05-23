import socket
import os.path as path
import os
HOST ='localhost'
PORT= 1025
socketServidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketServidor.bind((HOST,PORT))
socketServidor.listen(1)
print("Nos quedamos a la espera de la opción elegida por el usuario...")
s_cliente, addr = socketServidor.accept()
ruta = "C:\\Users\\Usuario\\Desktop\\sd"
os.chdir(ruta)
dirs = os.listdir(ruta)
def consultar():
    y = 0
    for file in dirs:
        if file.endswith(".txt"):
            s_cliente.send(bytes(file, "utf-8"))
            print(file)
            y = y + 1
    if y == 0:
        s_cliente.send(bytes("ERROR", "utf-8"))
    else:
        s_cliente.send(bytes("Fin", "utf-8"))

def subir():
    x=1
    print("\nDESCARGANDO EL FICHERO....")
    nombre_fichero = s_cliente.recv(1024)
    condition = s_cliente.recv(1024)
    if condition.decode("utf-8") != "ERROR":
        with open(nombre_fichero, "wb") as new_fichero:
            while x == 1:
                fichero = s_cliente.recv(1024)
                if len(fichero) < 1024:
                    x=2
                    new_fichero.write(fichero)
                else:
                    new_fichero.write(fichero)
        print("La subida se ha realizado correctamente.")
    else:
        print("No se ha podido subir el fichero")

def eliminar():
    fichero_eliminar = s_cliente.recv(1024)
    try:
        os.remove(fichero_eliminar)
    except:
        s_cliente.send(bytes("ERROR fichero no existe", "utf-8"))
    else:
        s_cliente.send(bytes("Fichero eliminado correctamente", "utf-8"))
def descargar():
    ficherointroducido = s_cliente.recv(1024)
    if os.stat(ficherointroducido.decode("utf-8")).st_size == 0:
        s_cliente.send(bytes("VACIO", "utf-8"))
    elif path.exists(ficherointroducido.decode("utf-8")):
        s_cliente.send(bytes("CORRECTO", "utf-8"))
        with open(ficherointroducido.decode("utf-8"), "rb") as Fichero:
            for contenido in Fichero:
                s_cliente.send(contenido)
    else:
        s_cliente.send(bytes("ERROR", "utf-8"))

z = 1
while z == 1:
    opcion = s_cliente.recv(1024)
    if (opcion.decode("utf-8") == 'consultar'):
        consultar()
    elif (opcion.decode("utf-8") == 'subir'):
        subir()
    elif (opcion.decode("utf-8") == 'eliminar'):
        eliminar()
    elif (opcion.decode("utf-8") == 'descargar'):
        descargar()
    elif (opcion.decode("utf-8") == 'salir'):
        print("El cliente se ha desconectado. Desconectando...")
        z=2
    else:
        print("El Cliente ha introducido una tecla incorrecta. Incorrecta...")
        z=2
s_cliente.close()
socketServidor.close()