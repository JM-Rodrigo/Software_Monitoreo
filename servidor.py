from socket import *
import os
import socket
from tkinter import *
import tkinter
from tkinter import filedialog
from tkinter import scrolledtext


ventana = Tk()
opcion=IntVar()
txtResultado = scrolledtext.ScrolledText(ventana,width=40,height=5)
txtResultado.grid(column=0,row=0)
fondo = "#78909C"
colorFont = "#000000"

ventana.configure(bg=fondo)
ventana.title("Servidor")
ventana.geometry("750x750")
txtTitulo=Label(ventana,text="SOFTWARE DE MONITOREO",bg=fondo, fg=colorFont,font=("System", 18)).place(x=175,y=20)


mi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mi_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

ip = "192.168.43.215"   #aqui va tu ip entre las comillas
puerto = 8000    #puerto, se puede cambiar si quieres
mi_socket.bind((ip, puerto))
mi_socket.listen(5) #Cantidad de peticiones que puede tener en cola el socket
printStr = "El servidor se inició correctamente\n"#, si la conexión es exitosa
txtResultado.insert(tkinter.INSERT, printStr)# Mostrado en la ventana de información
conexion, addr = mi_socket.accept()

def servidor():
        try:
            #Bloquear
            if opcion.get() == 1:
                try:
                    conexion.send("1".encode()) #se envia un aviso de que vamos a enviar un comando
                    comando="rundll32.exe user32.dll,LockWorkStation" # se inserta el comando que queremos mandar y ejecutar
                    conexion.send(comando.encode()) #se envia
                    h=""
                    while True:  #en este buble
                        g=conexion.recv(1024).decode()
                        if g=="\a":
                            break
                        h=h+g
                    print (h)
                except:
                   txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Enviar archivos
            elif opcion.get() == 2:
                try:
                    conexion.send("2".encode())
                    #Se crea la variable para generar la pantalla para seleccionar el archivo
                    archivo = filedialog.askopenfile(title="Abrir", initialdir= "C:/", filetypes=(("Todos los archivos", "*.*"),("Archivos de texto", "*.txt"),("Archivos pdf", "*.pdf") ))
                    #Se obiene le nombre del archivo y se envia 
                    nameFile = os.path.basename(archivo.name)
                    conexion.send(nameFile.encode())
                    while True:
                        f = open(archivo.name, "rb")
                        content = f.read(1024)
                        while content:
                            # Enviar contenido.
                            conexion.send(content)
                            content = f.read(1024)   
                        break
                    # Se utiliza el caracter de código 1 para indicar al cliente que ya se ha enviado todo el contenido.
                    try:
                        conexion.send(chr(1))
                    except TypeError:
                        # Compatibilidad con Python 3.
                        conexion.send(bytes(chr(1), "utf-8"))
                    
                    # Cerrar conexión y archivo.
                   
                    txtResultado.insert(INSERT,"El archivo se envio correctamente\n")
                   
                    nameFile = conexion.recv(1024)
                    f = open(nameFile, "wb")
                    while True:
                        try:
                            # Recibir datos del cliente.
                            input_data = conexion.recv(1024)
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
                    txtResultado.insert(INSERT,"El archivo se recibio correctamente\n")
                    f.close()          
                except:
                   txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Chat       
            elif opcion.get() == 3:
                try:
                    conexion.send("3".encode()) #se envia un aviso de que vamos a enviar un comando
                    print("------------ CHAT ------------")
                    while True:
                        #Recibimos el mensaje del cliente
                        mensajeRecibido = conexion.recv(1024).decode()
                        print("Cliente: ",mensajeRecibido)

                        #Si la cadena enviada es adios se termina el chat
                        if(mensajeRecibido == "adios"):
                            break
                        #Se manda mensaje al cliente
                        conexion.send(input("Escribe tu mensaje: ",).encode())
                except:
                   txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Apagar
            elif opcion.get() == 4:
                try:
                    conexion.send("1".encode()) #se envia un aviso de que vamos a enviar un comando
                    comando="shutdown -s -t 30" # se inserta el comando que queremos mandar y ejecutar
                    conexion.send(comando.encode()) #se envia
                    h=""
                    while True:  #en este buble
                        g=conexion.recv(1024).decode()
                        if g=="\a":
                            break
                        h=h+g
                    print (h)
                except:
                    txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Cerrar sesion
            elif opcion.get() == 5:
                try:
                    conexion.send("1".encode()) #se envia un aviso de que vamos a enviar un comando
                    comando="shutdown /l" # se inserta el comando que queremos mandar y ejecutar
                    conexion.send(comando.encode()) #se envia
                    h=""
                    txtResultado.insert(INSERT,"Se cancelo la acción\n")
                    while True:  #en este buble
                        g=conexion.recv(1024).decode()
                        if g=="\a":
                            break
                        h=h+g
                    print (h)
                except:
                    txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Reiniciar
            elif opcion.get() == 6:
                try:
                    conexion.send("1".encode()) #se envia un aviso de que vamos a enviar un comando
                    comando="shutdown /r /t 30" # se inserta el comando que queremos mandar y ejecutar
                    conexion.send(comando.encode()) #se envia
                    h=""
                    txtResultado.insert(INSERT,"Se cancelo la acción\n")
                    while True:  #en este buble
                        g=conexion.recv(1024).decode()
                        if g=="\a":
                            break
                        h=h+g
                    print (h)
                except:
                    txtResultado.insert(INSERT,"Servidor se desconecto\n")

            #Cancelar Apagado-Reinicio
            elif opcion.get() == 7:
                try:
                    conexion.send("1".encode()) #se envia un aviso de que vamos a enviar un comando
                    comando="shutdown /a" # se inserta el comando que queremos mandar y ejecutar
                    conexion.send(comando.encode()) #se envia
                    h=""
                    txtResultado.insert(INSERT,"Se cancelo la acción\n")
                    while True:  #en este buble
                        g=conexion.recv(1024).decode()
                        if g=="\a":
                            break
                        h=h+g
                    print (h)
                except:
                    txtResultado.insert(INSERT,"Servidor se desconecto\n")
        except:
            txtResultado.insert(INSERT,"Servidor se desconecto\n")
#Metodo para limpiar
def limpiar():
    opcion.set(None)
    txtResultado.delete(1.0,END)

#Metodo para salir
def salir(): 
    ventana.destroy()

#RadioButtons
lblAlg=Label(ventana,text="Selecciona una opcion:",bg = fondo, font=("Arial", 13)).place(x=70, y=80)
rBOptions=Radiobutton(ventana,text="Bloquear equipo",bg = fondo, variable=opcion, value=1,font=("Arial", 13)).place(x=140, y=110)
rBOptions=Radiobutton(ventana,text="Transferir archivos",bg = fondo, variable=opcion, value=2,font=("Arial", 13)).place(x=140, y=140)
rBOptions=Radiobutton(ventana,text="Chatear",bg = fondo, variable=opcion, value=3,font=("Arial", 13)).place(x=140, y=170)
rBOptions=Radiobutton(ventana,text="Apagar equipo",bg = fondo, variable=opcion, value=4,font=("Arial", 13)).place(x=140, y=200)
rBOptions=Radiobutton(ventana,text="Cerrar Sesion",bg = fondo, variable=opcion, value=5,font=("Arial", 13)).place(x=140, y=230)
rBOptions=Radiobutton(ventana,text="Reiniciar",bg = fondo, variable=opcion, value=6,font=("Arial", 13)).place(x=140, y=260)
rBOptions=Radiobutton(ventana,text="Cancelar apagado/reinicio",bg = fondo, variable=opcion, value=7,font=("Arial", 13)).place(x=140, y=290)
lblAlg=Label(ventana,text="Estatus:",bg = fondo, font=("Arial", 13)).place(x=380, y=80)
txtResultado.place(x=380, y=110)

boton=Button(ventana, text="Ejecutar", command=servidor, fg="navy",font=("Arial", 13)).place(x=380, y=210)
boton=Button(ventana, text="Nueva acción", command=limpiar,fg="navy",font=("Arial", 13)).place(x=380, y=260)
boton=Button(ventana, text="Salir", command=salir,fg="navy",font=("Arial", 13)).place(x=380, y=310)
ventana.mainloop()



