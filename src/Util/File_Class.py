# File Utility Class
import logging
import string
import os

log = logging.getLogger('open_controller_log.log')

class File(object):

    current_working_dir = os.getcwd()

    def __init__(self, filename):
        #filename_full = os.path.join(self.current_working_dir, filename)
        log.debug('Filepath for file is: {}'.format(filename))
        self.file_obj = self.OpenFileRead(filename)
        self.lines = self.file_obj.readlines()

    # Opens file with given filename
    def OpenFileRead(self, filename: string):
        try:
            return open(filename, 'r')
        except FileNotFoundError as e:
            log.error('Error msg: {}'.format(e, filename))

    def OpenFileWrite(self, filename: string):
        try:
            return open(filename, 'w')
        except FileNotFoundError as e:
            log.error('{} while opening file at {} for writing'.format(e, filename))

    def IsClosed(self):
        return self.file_obj.closed() #True if closed, false otherwise

    def ReturnMode(self):
        return self.file_obj.mode()

    def ReturnName(self):
        return self.file_obj.name()

    # Return false if space explicivityly required with print, true otherwise
    def ReturnSoftspace(self):
        return self.file_obj.softspace()

    # Return file as list for iterating
    def ReturnFileAsList(self):
        return self.lines

    def __del__(self):
        self.file_obj.close()
        #log.debug('File Closed')

