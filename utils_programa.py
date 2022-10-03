#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 11:21:35 2021

@author: curro
"""




def get_offset(pos,frame):
    offsetX = 0
    offsetY = 0
    #Switch según posición de encuadre (offsetX)
    if pos[1] == "0":
        offsetX = - frame.shape[1]/4 #bajar estos valores si no se quiere referencias tan alejadas
    elif pos[1] == "1":
        offsetX = 0
    elif pos[1] == "2":
        offsetX = frame.shape[1]/4
    #fin switch
    
    #Switch según posición de encuadre (offsetY)
    if pos[0] == "0":
        offsetY = - frame.shape[0]/4
    elif pos[0] == "1":
        offsetY = 0
    elif pos[0] == "2":
        offsetY = frame.shape[0]/4
    #fin switch
    
    return offsetX, offsetY



def envia_accion(accionX, accionY, socket_conRasp):
    #El menos es porque la imagen está girada.
    accionXString = str(int(-accionX))
    
    #Hace que el mensaje X tenga 3 caracteres.
    for i in range(len(accionXString),3) :
        accionXString = "0" + accionXString
        
    #El menos es por el sentido de giro del 2 servomotor.
    accionYString = str(int(-accionY))
    
    #Hace que el mensaje Y tenga 3 caracteres.
    for i in range(len(accionYString),3) :
        accionYString = "0" + accionYString
        
    #Junta los 2 mensajes, 6 caracteres en total.
    mens = accionXString + accionYString
    #Muestra por consola el mensaje enviado.
    print(mens)
    #Envía el mensaje a la Raspberry
    socket_conRasp.send(mens.encode())
    return 0
