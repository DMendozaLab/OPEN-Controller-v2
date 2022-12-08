#Super of Arduino Class

# Standard Libaries
import logging
import random
import string
import serial

# Project Specific Modules

#from Util.Serial_Communicator_Class import Serial_Communicator
#from Util.Serial_Communicator_Class import Serial_Communicator
from Util.UART_Serial_class import UART_Serial

log = logging.getLogger('open_controller_log.log')

class Arduino:

    #Constructor with passed port name
    def __init__(self, passed_port_name):
        self.serial_port_name = passed_port_name #taking in pass port name
        self.ser_port = UART_Serial()
        self.ser_port.Open_Port(passed_port_name)

    #Send Data Over Serial Port
    def Send_Serial(self, msg):
        if '\n' in msg:
            log.debug('Sending {} through arduino serial'.format(msg.strip('\n')))
        else:
            log.debug('Sending {} through arduino serial'.format(msg.encode('utf-8').hex()))
            
        self.ser_port.Write_Data(msg)

    #Read Serial Response
    def Read_Serial(self):
        msg = self.ser_port.Read_Data()
        if msg is None: # if none then error
            return None
        log.debug('Read {} from arduino serial'.format(msg))
        return msg

    def __del__(self):
        self.ser_port.__del__()
