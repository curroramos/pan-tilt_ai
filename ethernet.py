import socket
import time
import sys
import RPi.GPIO as GPIO



print("Creando socket TCP... \n")

socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#socket_tcp.connect(("169.254.94.140",8886))
socket_tcp.connect(("169.254.147.238",8886))
#socket_tcp.bind(("169.254.94.140",8050))
#socket_tcp.listen(1)

#socket_con, (client_ip, client_port) = socket_tcp.accept()
print("conexion aceptada")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

pwm=GPIO.PWM(11,50)
pwm.start(0)

pwmY=GPIO.PWM(13,50)
pwmY.start(0)

duty = 5;
dutyY = 5;

numactX=0
numactY=0


while True:
    data = socket_tcp.recv(1024).decode()
    print("Recibido:%s\n"%data)
    mens=data
    mensX=mens[0:3]
    mensY=mens[3:6]
    
    while (mensX[0]  == "0") & (len(mensX)>2):
        mensX=mensX[1:]
    
    while (mensY[0] == "0") & (len(mensY)>2) :
        mensY=mensY[1:]
        
    numX=int(mensX)+90
    numY=int(mensY)+90
    
    #num = int(data) + 90
    #print("numX: \n" + numX)
    #print("numY: \n" + numY)
    
    if (numX>numactX+3):
        numactX=numX
        duty = 1/18*(numX)
        if (duty>10):
            duty = 10
        if (duty<0):
            duty = 0
        pwm.ChangeDutyCycle(duty)                            
        
    if (numX<numactX-3):
        numactX=numX
        duty = 1/18*(numX)
        if (duty<0):
            duty = 0
        if (duty>10):
            duty = 10
        pwm.ChangeDutyCycle(duty)
            
#     if (num>80):
#         duty = duty+0.2;
#         if (duty>10):
#             duty = 10
#         pwm.ChangeDutyCycle(duty)
#         
#     if (num<-80):
#         duty = duty-0.2;
#         if (duty<0):
#             duty = 0
#         pwm.ChangeDutyCycle(duty)
    if (numY>numactY+3):
        numactY=numY
        dutyY = 1/18*(numY)
        if (dutyY>10):
            dutyY = 10
        if (dutyY<0):
            dutyY = 0
        pwmY.ChangeDutyCycle(dutyY)                            
        
    if (numY<numactY-3):
        numactY=numY
        dutyY = 1/18*(numY)
        if (dutyY<0):
            dutyY = 0
        if (dutyY>10):
            dutyY = 10
        pwmY.ChangeDutyCycle(dutyY)
        
            
    time.sleep(0.05)
    
    
socket_tcp.close()
GPIO.cleanup

