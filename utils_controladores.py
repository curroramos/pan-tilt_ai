#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 17:54:59 2021

@author: curro
"""

def get_accion_PID(Kp, Kd, Ki, errorX, errorY, integralX, integralY, accionX, accionY, errorAntX, errorAntY):
    
    ## EJE X
    integralX = integralX + errorX
    
    #Restablece el valor de la integral al aproximarse a la posicion deseada
    if abs(errorX)<20: #aumentar rango ?? Probado con 10
        integralX = 0
    # Control PID
    accionX = accionX + Kp*(errorX + Kd*(errorX - errorAntX) + Ki*integralX)
    
    
    ##EJE Y
    integralY = integralY + errorY
    
    #Restablece el valor de la integral al aproximarse a la posicion deseada
    if abs(errorY)<20: 
        integralY = 0
    # Control PID
    accionY = accionY + Kp*(errorY + Kd*(errorY - errorAntY) + Ki*integralY)
    
    return accionX, accionY, integralX, integralY



def get_accion_PD(Kp, Kd, Ki, errorX, errorY, accionX, accionY, errorAntX, errorAntY):
    
    ## EJE X
    # Control PD
    accionX = accionX + Kp*(errorX + Kd*(errorX - errorAntX))

    ##EJE Y
    # Control PD
    accionY = accionY + Kp*(errorY + Kd*(errorY - errorAntY))
    
    return accionX, accionY


def get_accion_proporcional(Kp, errorX, errorY, accionX, accionY):
    
    ## EJE X
    # Control Proporcional
    accionX = accionX + Kp*errorX

    ##EJE Y
    # Control PD
    accionY = accionY + Kp*errorY
    
    return accionX, accionY

def get_accion_inc(Kinc, errorX, errorY, accionX, accionY):
    if(errorX>10):
        accionX += Kinc
    elif (errorX<-10) :
        accionX -= Kinc

    if(errorY>10):
        accionY += Kinc
    elif(errorY<-10) :
        accionY -= Kinc

