# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:51:24 2021

@author: Carlos
"""

# import necessary packages for hand gesture recognition project using Python OpenCV
import cv2
import numpy as np
import mediapipe as mp
import threading
import socket
import time
from utils_detectores import *
from utils_controladores import *
from utils_programa import *




# =============================================================================
# Poner WIFI a True si se desea conectar con la interfaz gráfica por WIFI.
# Poner RASP a True si se tiene conectada la Raspberry por Ethernet.
# En caso de no tener conectada la RASP, poner RASP y los mensajes que deberían
# enviarse se escribirán por pantalla.
# =============================================================================

WIFI = False
RASP = False

# =============================================================================
# Inicio de Conexiones
# =============================================================================

#Direccion IP, cambiar a la del ordenador que se esté usando.

# host = '169.254.94.140' #Carlos
#host = '169.254.82.168' #curro

print('IP:' + host)


#Puerto, mantener en 8886 si no se cambia en el programa de Raspberry o Java.
port = 8886

 
#Creación de un objeto socket (lado servidor)
obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
#Conexión con el cliente. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.bind((host, port))
obj.listen(2)


if WIFI:
    host_wifi = 'IP CURRO WIFI'
    #Usar el mismo puerto, si se cambia, cambiar en programa interfaz
    #Creación de un objeto socket (lado servidor)
    objWifi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    #Conexión con el cliente. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
    objWifi.bind((host_wifi, port))
    objWifi.listen(1)
    print("Esperando conexión con interfaz gráfica...\n")
    #Primero se debe conectar con el programa de Java.
    socket_con, (client_ip, client_port) = objWifi.accept()
    print("Cliente 1 conectado \n")
    
else :
    print("Esperando conexión con interfaz gráfica...\n")
    #Primero se debe conectar con el programa de Java.
    socket_con, (client_ip, client_port) = obj.accept()
    print("Cliente 1 conectado \n")


if RASP:
    #Luego conectar el programa de la Raspberry.
    print("Esperando conexión con Raspberry Pi...\n")
    socket_conRasp, (client_ip, client_port) = obj.accept()
    print("Raspberry conectada \n")


# =============================================================================
# Fin de conexiones
# =============================================================================



print("Conectando cámara...")
#Sleep para asegurar la conexión de los sockets.
time.sleep(1)


# =============================================================================
# Inicio Variables globales con valores por defecto
# =============================================================================
color_g = "red"
control_g=0
cara_g=False
mano_g=True
colores_g = False
pos_g="11" #posicion encuadre
controlador_g="PD"
Kinc_g = 0.01
Kp_g = 0.015
Kd_g = 0.001
Ki_g = 0.001
# =============================================================================
# Fin de variables globales
# =============================================================================

#Creacion del mutex para acceder a las variables globales.
mutex = threading.Lock()


# =============================================================================
# Se define la función aquí y no en utils_programa porque 
# es más fácil modificar las variables globales.
# 
# =============================================================================


def procesa_datos(mensaje):

    
    if mensaje.startswith("Pos:"):
        global pos_g
        pos_g = mensaje[-2:]
    
    global colores_g 
    global cara_g
    global mano_g
    
    if mensaje.startswith("Color:"):
        colores_g = True
        mano_g = False
        cara_g = False
        global color_g
        if mensaje.endswith("Rojo"):
            color_g = "red"
        if mensaje.endswith("Verde"):
            color_g = "green"
        if mensaje.endswith("Azul"):
            color_g = "blue"
            
    if mensaje.startswith("Cara"):
        colores_g = False
        mano_g = False
        cara_g = True
        
     
    if mensaje.startswith("Mano"):
        colores_g = False
        mano_g = True
        cara_g = False
    
    controladores = ["incremental", "proporcional", "PD", "PID"]
    if mensaje == "Control":
        global control_g
        control_g = not control_g    
    elif mensaje.startswith("Controlador"):
        global controlador_g
        controlador_g = controladores[int(mensaje[-1])-1]
    
    if mensaje.startswith("Constantes:"):
        i = 0
        index = 0
        while (mensaje[i] != ":"):
            i+=1
        index = i+1
        i += 1
        while (mensaje[i] !=":"):
            i+=1
        global Kinc_g
        Kinc_g = float(mensaje[index:(i)])
        index = i+1
        i += 1
        while (mensaje[i] !=":"):
            i+=1
        global Kp_g
        Kp_g = float(mensaje[index:(i)])
        index = i+1
        i += 1
        while (mensaje[i] !=":"):
            i+=1
        global Kd_g
        Kd_g = float(mensaje[index:(i)])
        index = i+1
        i += 1
        global Ki_g
        Ki_g = float(mensaje[index:])
            
        
# =============================================================================
# Fin de función de procesar mensajes  
# =============================================================================
        



#Hilo que esperará el envío de mensajes por parte de la interfaz gráfica.
def hiloJava():
    while(True):
        recibido = socket_con.recv(40).decode("utf-8")
        if len(recibido) < 2:
            break
        print(recibido)
        mutex.acquire()
        try: 
            procesa_datos(recibido)  #Aquí dentro se hace la copia a las variables globales.
        except: 
            print("Error al procesar. \n")
        mutex.release()
        #Para ver si funciona:
        print("color_g:"+ color_g)
        print("control_g:"+ str(bool(control_g)))
        print("cara_g: "+ str(bool(cara_g)))
        print("mano_g: "+ str(bool(mano_g)))
        print("colores_g: "+ str(bool(colores_g)))
        print("pos_g: "+ str(pos_g))
        print("controlador_g: "+ str(controlador_g))
        print("Kinc: "+str(Kinc_g))
        print("kp_g: "+str(Kp_g))
        print("kd_g: "+ str(Kd_g))
        print("ki_g: "+ str(Ki_g))
        
        
#Arranque del hilo
t = threading.Thread(target=hiloJava)
t.start()




# =============================================================================
# #Definicion y valores iniciales de variables necesarias para el control
# =============================================================================
accionX = 0
errorAntX = 0
integralX = 0

accionY = 0
errorAntY = 0
integralY = 0

# =============================================================================
# Fin definicion de variables para control
# =============================================================================





# Inicialización de la cámara
cap = cv2.VideoCapture(1)
while True:
    
# =============================================================================
#   # Copiar variables globales en variables locales
# =============================================================================
  mutex.acquire()
  colores = colores_g
  color = color_g
  control= control_g
  cara= cara_g
  mano= mano_g
  pos=pos_g #posicion encuadre
  controlador=controlador_g
  Kinc = Kinc_g
  Kp = Kp_g
  Kd = Kd_g
  Ki = Ki_g
  mutex.release()
# =============================================================================
#   Fin copia variables
# =============================================================================
  


    
  # Leer frame de la cámara
  _, frame = cap.read()
  y , x, c = frame.shape
  # Rota el frame en el eje vertical (modo espejo)
  frame = cv2.flip(frame, 1) 
  #Convierte los colores a RGB
  framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
  if control: #Si la variable control no está activada, simplemente muestra la imagen
      
        #Switch según detector elegido          
        if mano: 
            posX,posY=get_mano(framergb, frame, x, y)
        elif cara:
            posX,posy=get_cara(framergb, frame, x, y) #Falta funcion
            # print('0')
        elif colores:
            posX,posY = get_color(frame, color) #color valdrá Red|Blue|Green
            # print('0')
        #fin switch
        
        #Para comprobar funcionamiento:
        #print("PosX: ", posX)
        #print("PosY: ", posY)
        
        if (posX != 'NaN' and posY != 'NaN'): # Si se reconoce un objeto/mano/cara
        
            offsetX,offsetY = get_offset(pos,frame) # Se obtienen los offset según la posición de encuadre activada (pos)
            #Cálculo del error para la accion de control
            errorX = (frame.shape[1]/2 - posX + offsetX) #usar x,y,c en vez de frame.shape?
            errorY = (frame.shape[0]/2 - posY + offsetY)
            
            
            #Switch según controlador elegido
            if controlador == "incremental":
                accionX, accionY = get_accion_inc(Kinc, errorX, errorY, accionX, accionY)
            elif controlador == "proporcional" :
                accionX, accionY = get_accion_proporcional(Kp, errorX, errorY, accionX, accionY)
            elif controlador == "PD":
                accionX, accionY = get_accion_PD(Kp, Kd, Ki, errorX, errorY, accionX, accionY, errorAntX, errorAntY)
            elif controlador == "PID" :
                accionX, accionY, integralX, integralY = get_accion_PID(Kp, Kd, Ki, errorX, errorY, integralX, integralY, accionX, accionY, errorAntX, errorAntY)
            #fin switch
            
            
            #Se guardan los valores de los errores para la proxima iteración
            errorAntX = errorX  
            errorAntY = errorY 
     
            #Saturación de la accion de control y Antqqi-Windup
            if abs(accionX)>=90:
                integralX = integralX - errorX
                accionX = 90*accionX/abs(accionX)
                
            if abs(accionY)>=90:
                integralY = integralY - errorY
                accionY = 90*accionY/abs(accionY)
            
            #Envia los ángulos resultantes a la raspberry
            if RASP:
                envia_accion(accionX, accionY, socket_conRasp)
            else :
                print(str(accionX) + ":" + str(accionY))
        
  time.sleep(0.1)
  # Show the final output
  cv2.imshow("Output", frame)
  if cv2.waitKey(1) == ord('q'):
        break



    
