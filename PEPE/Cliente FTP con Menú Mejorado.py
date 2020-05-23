import socket
import os
HOST = 'localhost'
PORT = 1025
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
def consultar():
    s.send(bytes("consultar", "utf-8"))
    y = 1
    existencia = s.recv(1024)
    if existencia.decode("utf-8") == "ERROR":
        print("No hay ficheros disponible.")
    else:
        print("LOS FICHEROS (.txt) QUE DISPONES SON: ")
        print(existencia.decode("utf-8"))
        while y == 1:
            existencia = s.recv(1024)
            if existencia.decode("utf-8") == "Fin":
                y = 0
            else:
                print(existencia.decode("utf-8"))
    return 0

def subir():
    s.send(bytes("subir", "utf-8"))
    ficherointroducido = input("Introduzca el fichero que deseas subir: ")
    s.send(bytes(ficherointroducido, "utf-8"))
    condicion = s.recv(1024)
    if (condicion.decode("utf-8") == 'Vacio'):
        print("El archivo está vacío. No se ha podido subir.")
    elif (condicion.decode("utf-8") == 'Correcto'):
        with open(ficherointroducido, "rb") as Fichero:
            for contenido in Fichero:
                s.send(contenido)
            print("La subida se ha realizado correctamente.")
    else:
        print("ERROR. No se pudo subir el fichero.")

def eliminar():
    consultar()
    s.send(bytes("eliminar", "utf-8"))
    fichero_eliminar = input("Introduce fichero a eliminar: ")
    s.send(bytes(fichero_eliminar, "utf-8"))
    final = s.recv(1024)
    print(final.decode("utf-8"))

def descargar():
    x=1
    s.send(bytes("descargar", "utf-8"))
    nombre_fich = input("Introduzca el nombre del fichero: ")
    s.send(bytes(nombre_fich, "utf-8"))
    condicion = s.recv(1024)
    if condicion.decode("utf-8") == "ERROR":
        print("El archivo no existe.")
    elif condicion.decode("utf-8") == "VACIO":
        print("El archivo está vacio y no se va a descargar.")
        x=2
    else:
        print("\nDESCARGANDO EL FICHERO....")
        nombre_fichero = input("Introduzca el nombre con el que deseas guardar el fichero: ")
        with open(nombre_fichero, "wb") as new_fichero:
            while x == 1:
                fichero = s.recv(1024)
                if len(fichero.decode("utf-8")) < 1024:
                    new_fichero.write(fichero)
                    x = 2
                elif len(fichero.decode("utf-8")) == 1024:
                    new_fichero.write(fichero)
                else:
                    x = 2

print("BIENVENIDO AL MENU")
print("Seleccione que deseas hacer: ")
k = 1
while k==1:
    x = int (input("1- Consultar archivos que dispone el servidor. \n2- Subir archivo al servidor. \n3- Eliminar archivos del servidor. \n4- Descargar archivos del servidor. \n5- Salir del menu.\n"))
    if(x==1):
        consultar()
    elif(x==2):
        subir()
    elif(x==3):
        eliminar()
    elif(x==4):
        descargar()
    elif(x==5):
        s.send(bytes("salir", "utf-8"))
        print("Cerrando la sesion...")
        k=2
    else:
        print("ERROR -> EL NUMERO INTRODUCIDO ES INCORRECTO")
        k=2
s.close()