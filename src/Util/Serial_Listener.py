#Serial listener process
try:
    from UART_Serial_class import UART_Serial
except ImportError:
    print('failure to import in serial_listener.py')
    
from time import sleep
import socket
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

logging.debug('starting serial sub process')
sleep(0.1)

portname = sys.argv[1]
socket_port = sys.argv[2]
adr = ('127.0.0.1', int(socket_port))  # localhost on pi
ser = UART_Serial()
ser.Open_Port(portname)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(adr)
    s.settimeout(0.1)
    sleep(0.1)
    s.sendall(b'Hello Server! I am connected from serial client')

    try:
        #Event loop
        while True:
            #recieve data, check socket then send data from socket also
            try:
                data = s.recv(1024)
            
                if data:    #if recieved something from socket
                    data_string = str(data, 'UTF-8')
                    #buffer += data_string
                    logging.debug("client received: {}".format(data))
                    ser.Write_Data(data) #write to serial
            except socket.timeout: #instead of TimeoutError
                pass

            #sleep(0.1)

            #send data (check serial and do nothing if nothing)
            try:
                ser_data = ser.Read_Data() #check to make sure in bytes
                if ser_data:
                    s.send(ser_data) #send recievd serial data over socket
                    ser_data_string = str(ser_data, 'UTF-8')
                    logging.debug('serial sent: {}'.format(ser_data))
            except TimeoutError:
                pass

            #sleep(0.1)
    except KeyboardInterrupt:
        logging.info("keyboard interrupt and port closed")
        s.close()
        ser.Close_Port()