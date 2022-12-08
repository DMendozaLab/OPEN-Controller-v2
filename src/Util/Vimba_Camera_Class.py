# Class wrapper for Vimba Camera to facilate easier use
import logging
import os.path

import cv2
from vimba import *
from datetime import datetime
from time import sleep

log = logging.getLogger('open_controller_log.log')

'''Using with statement throughout this class to grab and autodelete vimba camera.
    The instance still persist.'''

class Vimba_Camera(object):

    #vimba_ins = Vimba.get_instance()
    settings_file = 'src/Setting_Files/OPEN_Root_Settings_V2.xml' #TODO set this constant

    def __init__(self):
        log.debug('Vimba Camera Class initiated')
        self.save_location = None
        self.LoadSettings()
        #self.vimba = Vimba.get_instance()

    def LoadSettings(self):
        try: 
            with Vimba.get_instance() as vimba: 
                cams = vimba.get_all_cameras()
                with cams[0] as cam:
                    cam.load_settings(self.settings_file, PersistType.All)
                    log.info("Camera Settings File Loaded")
                    cam.GVSPAdjustPacketSize.run()
                    while not cam.GVSPAdjustPacketSize.is_done():
                        pass
        except IndexError as e:
            log.error("Index Error: {}".format(e))
        except Exception as e:
            log.error('Failure to load Camera Settings because {}'.format(e))

    def CaptureImage(self, filepath):
        frame = self.CaptureFrame()
        self.SaveImage(frame, filepath)

    #gets and return Frame already converted
    def CaptureFrame(self):
        try:
            self.LoadSettings()
            with Vimba.get_instance() as vimba: 
                cams = vimba.get_all_cameras()
                with cams[0] as cam:
                    # converting to Bayer Format
                    cam.set_pixel_format(PixelFormat.BayerGR8)
                    #Capturing frame
                    sleep(2)
                    frame = cam.get_frame()
                    sleep(2)
                    log.info('Image Captured with vimba camera')
                    return frame  # may not return
        except IndexError as e:
            log.error("Index Error: {}".format(e))
        except:
            log.error('Failure to load Camera Settings')

    def SaveImage(self, frame, filename):
        try:
            #get the raw image as numpy array from frame
            image = frame.as_numpy_ndarray()
            #use opencv to convert from raw Bayer to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BAYER_GR2RGB)
            #write image to disk
            log.debug("filename for SaveImage is {}".format(filename))
            cv2.imwrite(filename, rgb_image)
            log.info('Image writen to disk at {}'.format(filename))
        except:
            log.info("failure to save {} at this time".format(filename))

    #def __del__(self):
        #log.debug('Vimba Camera class deleted')
        
