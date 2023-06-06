import serial
import time
import keyboard

ard = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
status = False


def write(x):
    ard.write(bytes(x, 'utf-8'))
    
while True:
    if keyboard.is_pressed('ENTER'):
        write('1')
        time.sleep(0.05)
        data = ard.readline().decode("utf-8") 
        if data == 'ON':
            print("ON")
        else:
            print("OFF")

