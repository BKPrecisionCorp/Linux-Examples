import serial
import time
serialPort = serial.Serial(
	port = "/dev/ttyACM0", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
	
serialstring = ""
time.sleep(.5)
serialPort.write(b'*IDN?\n')
time.sleep(.5)
print(serialPort.read(40))

