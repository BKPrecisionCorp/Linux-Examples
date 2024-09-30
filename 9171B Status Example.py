import pyvisa
import time 

try:
    #List all available VISA resources
    rm = pyvisa.ResourceManager()
    li = rm.list_resources()
    choice = ''
    while(choice == ''):
        for index in range(len(li)):
            print(str(index)+" - "+li[index])
        choice = input("Select DUT: ")
        try: 
            if(int(choice) > len(li) - 1 or int(choice) < 0):
                choice = ''
                print("Invalid Input\n")
        except:
            print("Invalid Input\n")
            choice = ''

except:
    # could not connect
    print('Could not establish communication with resource. Exiting')
    inst.exit()
    inst.close()

inst = rm.open_resource(li[int(choice)]) 

print('Instrument Connected: ' + li[int(choice)] + "\n")

def instrumentInit():
    # initialize instrument parameters and query ID
    inst.baud_rate = 57600
    inst.timeout = 5000 # 5s
    inst.chunk_size = 10400
    inst.read_termination = '\n'
    inst.write_termination = '\n'

    inst.write("*RST")
    time.sleep(.5)
    inst.write("*CLS")
    time.sleep(.5)
    ID = inst.query("*IDN?")
    print("Instrument ID = " + ID + "\n")
    errorquery()
    return;

def errorquery():
    #Query error bus
    time.sleep(.5)
    err = inst.query("SYST:ERR?")
    print("reported error = " + err + "\n")
    time.sleep(.5) 
    return;

def Status():
    #Read the registers status and convert hex string to binary
    status = inst.query("STATUS?")
    print(status)
    binary = bin(int(status[0:6], 16))
    print(binary)
    return;

def ConfigStatus():

    #Configures each bit of byte 0 enabling each bit one at a time starting with bit 1

    #Enable bit 1 LCD backlight ON
    inst.write("SYS:LCD:BL 1")
    errorquery()
    Status()
    
    #Enable bit 3 CH1 Output Enable
    inst.write("OUT1 ON")
    errorquery()
    Status()

    #Enable bit 5 CH1 OCP Enable
    inst.write("OCP ON")
    errorquery()
    Status()
    time.sleep(.750)

    #Enable bit 7 CH1 OVP Enable
    inst.write("OVP ON")
    errorquery()
    Status()

def main():
    instrumentInit()
    Status()
    ConfigStatus()
    inst.close()
    

if __name__ == '__main__': 
    proc = main()

