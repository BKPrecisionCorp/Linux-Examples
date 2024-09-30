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
#        try: 
#           if(int(choice) > len(li) - 1 or int(choice) < 0):
#                choice = ''
#               print("Invalid Input\n")
#      except:
#         print("Invalid Input\n")
#        choice = ''

except:
    # could not connect
    print('Could not establish communication with resource. Exiting')
    inst.exit()
    inst.close()

#inst = rm.open_resource(li[int(choice)]) 
inst = rm.open_resource(choice) 
print('Instrument Connected: ' + choice + "\n")

def instrumentInit():
    # initialize instrument parameters and query ID
    inst.timeout = 5000 # 5s
    inst.chunk_size = 10400
    inst.read_termination = '\n'
    inst.write_termination = '\n'

    inst.write("*RST")
    time.sleep(.25)
    inst.write("*CLS")
    time.sleep(.25)
    inst.write("SYST:REM")
    ID = inst.query("*IDN?")
    print("Instrument ID = " + ID + "\n")
    errorquery()
    return;

def errorquery():
    #Query error bus
    time.sleep(.05)
    err = inst.query("SYST:ERR?")
    print("reported error = " + err + "\n")
    time.sleep(.05) 
    return;
    
def configVOLT():
    voltage = input("Enter set voltage value: ")
    time.sleep(.05)
    inst.write("VOLT "+ voltage)
    errorquery()
    inst.write("OUTP 1")
    return;
    
def readVOLT():
    try: 
        while True:
            print(inst.query("MEAS:VOLT:AC?"))
            errorquery()
            time.sleep(.05)
    except KeyboardInterrupt:
        inst.write("OUTP 0")
        print("Data Acquired")
    return;
    

def main():

    instrumentInit()
    configVOLT()
    readVOLT()
    inst.close()
    

if __name__ == '__main__': 
    proc = main()
