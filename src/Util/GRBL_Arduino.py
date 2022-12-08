# GRBL Subclass of Arduino class
import logging

from Util.Arduino_Class import Arduino
from Util.File_Class import File
from time import sleep


class GRBL_Arduino(Arduino):

    GRBL_Settings = File('src/Setting_Files/GRBL_settings.txt')
    
    def __init__(self, portname):
        super(GRBL_Arduino, self).__init__(portname)
        self.ser_port.Write_Data("\r\n\r\n") # wake up grbl
        sleep(2)
        self.ser_port.ser.flushInput()        # flush input messages
        self.SetGRBLSettings()
        self.HomeCommand()

    # homing commands wait until we have ok signal, other manual commands go to ok right away
    def SendCommand(self, command):
        try:
            self.Send_Serial(command + '\n')
            sleep(1)
            is_ok = self.ser_port.Read_Data()
            while is_ok != 'ok':
                is_ok = self.ser_port.Read_Data()
                #logging.debug('is_ ok is {}'.format(is_ok))
            sleep(0.5)
            self.ser_port.ser.flushInput()
        except:
            return False

    # set GRBL Settings to serial port
    def SetGRBLSettings(self):
        logging.info('Loading GRBL settings')
        for line in self.GRBL_Settings.ReturnFileAsList():
            self.Send_Serial(line)

    def HomeCommand(self): 
        self.SendCommand('$H\n')
        
    def SleepCommand(self):
        self.Send_Serial('$SLP\n')
        
    def GRBLSoftReset(self):      
        self.Send_Serial(chr(0x18)) # ctrl-x in ascii