#practice machine class for communicating with GUI
import logging
import os
from time import sleep
from Util.Event import Event_Obj
from Util.GRBL_Arduino import GRBL_Arduino
from Util.Vimba_Camera_Class import Vimba_Camera
from Util.Lights_Arduino import Lights_Arduino
from Util.File_Class import File
import time
import schedule
from datetime import datetime, date
import threading #for threading things

log = logging.getLogger('open_controller_log.log')


class Machine:

    # Class Variables - constants
    
    # command list
    grbl_commands = File(os.path.join(os.getcwd(), 'src/Setting_Files/grbl_commands.txt'))
    start_of_night = 22
    end_of_night = 7

    #Events for communicating with GUI
    OnGRBLConnected = Event_Obj()
    OffGRBLConnected = Event_Obj()
    OnLightConnected = Event_Obj()
    OffLightConnected = Event_Obj()
    OnCameraSettingsLoaded = Event_Obj()
    OffCameraSettingsLoaded = Event_Obj()

    '''def __init__(self):
        self.stop_event = None
        log.info('Machine class is initiated')

        #initating arduinos and camera
        self.grbl_ar = GRBL_Arduino('/dev/ttyACM0') #GRBL arduino, plugged in first
        self.lights_ar = Lights_Arduino('/dev/ttyACM1') #plugged in second
        self.camera = Vimba_Camera()

        self.saveFolderPath = os.getcwd() # just to have something set on the program just in case
        self.cameraSettingsPath = None
        self.timelapse_interval = 2
        self.timelapse_end_date = datetime.combine(datetime.now(), datetime.max.time())
        self.current_Position = None
        self.timelapse_start_of_night = datetime.strptime("21", "%H")
        self.timelapse_end_of_night = datetime.strptime("7", "%H")
        self.stop_run_continuously = None
        self.timelapse_running = False
        self.num_of_pos = 7 #default number of positions
        
        #setting night schedules
        self.SetTimelapseStartOfNight(self.timelapse_start_of_night.strftime('%H'))
        self.SetTimelapseEndOfNight(self.timelapse_end_of_night.strftime('%H'))'''
    
    #init with declared serial ports
    def __init__(self, grbl_port, lights_port):
        self.stop_event = None
        log.info('Machine class is initiated')

        #initating arduinos and camera
        if grbl_port is None:
            self.grbl_ar = GRBL_Arduino('/dev/ttyACM0') #GRBL arduino, plugged in first
        else:
            self.grbl_ar = GRBL_Arduino(grbl_port) #GRBL arduino, plugged in first
        if lights_port is None:
            self.lights_ar = Lights_Arduino('/dev/ttyACM1') #plugged in second
        else:
            self.lights_ar = Lights_Arduino(lights_port) #plugged in second
        self.camera = Vimba_Camera()

        self.saveFolderPath = os.getcwd() # just to have something set on the program just in case
        self.cameraSettingsPath = None
        self.timelapse_interval = 2
        self.timelapse_end_date = datetime.combine(datetime.now(), datetime.max.time())
        self.current_Position = None
        self.timelapse_start_of_night = datetime.strptime("21", "%H")
        self.timelapse_end_of_night = datetime.strptime("7", "%H")
        self.stop_run_continuously = None
        self.timelapse_running = False
        self.num_of_pos = 7 #default number of positions
        
        #setting night schedules
        self.SetTimelapseStartOfNight(self.timelapse_start_of_night.strftime('%H'))
        self.SetTimelapseEndOfNight(self.timelapse_end_of_night.strftime('%H'))

    def SetSaveFolderPath(self, path):
        # setting path
        self.saveFolderPath = path
        log.debug('save folder setting path is {}'.format(self.saveFolderPath))
        '''commands = self.grbl_commands.ReturnFileAsList()
        #removing homing signals
        commands = commands[1:-1]
        
        #make folders in save folder path
        if path:    # if real path
            for position in commands:
                folder_name = "Position_" + str(commands.index(position) + 1) #this should return the number, may need to add 1 as well
                folder_path = os.path.join(self.saveFolderPath, folder_name)
                try:
                    if not os.path.isdir(folder_path): # if folder not made then make it
                        os.makedirs(folder_path)
                        logger.debug('Folder made at {}'.format(folder_path))
                except OSError:
                    logger.error('Fialure to make folder {}'.format(folder_path))
                    pass # pass if already exist'''
                
        return
    
    # makes number of position folders as needed
    def PositionFolders(self):
        commands = self.grbl_commands.ReturnFileAsList()
        #removing homing signals
        #commands = commands[1:-1]
        commands = commands[1:-(8-int(self.num_of_pos))]
        #make folders in save folder path
        if self.saveFolderPath:    # if real path
            for position in commands:
                folder_name = "Position_" + str(commands.index(position) + 1) #this should return the number, may need to add 1 as well
                folder_path = os.path.join(self.saveFolderPath, folder_name)
                try:
                    if not os.path.isdir(folder_path): # if folder not made then make it
                        os.makedirs(folder_path)
                        log.debug('Folder made at {}'.format(folder_path))
                except OSError:
                    log.error('Failure to make folder {}'.format(folder_path))
                    pass # pass if already exist
                
    def SetNumOfPos(self, num):
        self.num_of_pos = num
        log.debug('Machine Num of Pos is: {}'.format(self.num_of_pos))

    def SetCameraSettingsPath(self, path):
        self.cameraSettingsPath = path

    def SetTimelapseInterval(self, interval):
        log.debug("Timelapse interval is set to: {}".format(interval))
        self.timelapse_interval = int(interval)
        
    def SetTimelapseEndDate(self, end_date):
        end_date_datetime = datetime.combine(end_date, datetime.max.time())
        log.debug("Timelapse end date is set to: {}".format(end_date_datetime))
        self.timelapse_end_date = end_date_datetime
        
    def SetTimelapseStartOfNight(self, start_of_night):
        # state flag for if schedule running
        self.start_of_night_schedule_flag = 0;
        
        log.debug("Timelapse start of night is set to: {}".format(start_of_night))
        start_of_night_dt = datetime.strptime(start_of_night, "%H")
        log.debug("start of night_dt value is {}".format(start_of_night_dt))
        self.timelapse_start_of_night = start_of_night_dt
        
        # schedule it to turn off growlights
        '''if self.start_of_night_schedule_flag == 0:
            schedule.every().day.at(start_of_night_dt.strftime('%H:%M')).do(self.GrowLights_Off)
            #self.stop_run_continously_start_night = self.run_continuously()
            self.start_of_night_schedule_flag = 1
        else: # stop current run and start new one with new parameters
            #self.stop_run_continously_start_night.set()
            schedule.every().day.at(start_of_night_dt.strftime('%H:%M')).do(self.GrowLights_Off)
            #self.stop_run_continously_start_night = self.run_continuously()
            self.start_of_night_schedule_flag = 1 # redundant but just in case'''
            
    def TimelapseStartOfNightThread(self):
        job_thread = threading.Thread(target=self.GrowLights_Off())
        job_thread.start()
        
    def SetTimelapseEndOfNight(self, end_of_night):
        #end of night schedule flag for if schedule set yet
        self.end_of_night_schedule_flag = 0;
        
        log.debug("Timelapse end of night is set to: {}".format(end_of_night))
        end_of_night_dt = datetime.strptime(end_of_night, "%H")
        log.debug("end of night_dt value is {}".format(end_of_night_dt))
        self.timelapse_end_of_night = end_of_night_dt
                      
        # schedule it to turn on growlights
        '''if self.end_of_night_schedule_flag == 0:
            schedule.every().day.at(end_of_night_dt.strftime('%H:%M')).do(self.GrowLights_On)
            #self.stop_run_continously_end_night = self.run_continuously(interval=1)
            self.end_of_night_schedule_flag = 1
        else: # stop current run and start new one with new parameters
            #self.stop_run_continously_end_night.set()
            schedule.every().day.at(end_of_night_dt.strftime('%H:%M')).do(self.GrowLights_On)
            #self.stop_run_continously_end_night = self.run_continuously(interval=1)
            self.end_of_night_schedule_flag = 1 # redundant but just in case'''

    # Function that moves to specific location
    def MoveTo(self, posNum):
        commands = self.grbl_commands.ReturnFileAsList()
        log.info('Moving to position {}'.format(posNum))
        # sending command
        if posNum == '$H':
            self.grbl_ar.HomeCommand()
        else: # regular position
            self.grbl_ar.Send_Serial(commands[int(posNum)])

    def CaptureImage(self, filepath):
        log.info('Capturing image on vimba camera')
        self.camera.CaptureImage(filepath)
        
    '''Manually capture images from GUI based on position of machine'''
    def CaptureImageManual(self, posNum_str):
        if posNum_str == '$H':
            log.error('Trying to capture image on homing command in manual section')
            pass
        else:
            #trying lights on for image capture
            self.lights_ar.GrowlightsOff()
            self.lights_ar.BackLightsOn()
            sleep(0.5)
            
            #setting filepath for manual image
            posNum_int = int(posNum_str)
            posNum_int = posNum_int - 1
            log.info('Capturing image manually from tkinter on vimba camera')
            filepath = self.Filepath_Set(posNum_int) #minus one becuase filepath_set adds one during execution
            self.camera.CaptureImage(filepath)
            
            #resetting lights to normal states
            sleep(0.5)
            self.lights_ar.GrowlightsOn()
            self.lights_ar.BackLightsOff()

    def Filepath_Set(self, position_number):
        current_time = datetime.now().strftime('%d-%m-%Y--%H-%M-%S')
        filename = current_time + '_P' + str(position_number + 1) + '.png'
        folder_name = "Position_" + str(position_number + 1)
        folder_path = os.path.join(self.saveFolderPath, folder_name)
        filepath = os.path.join(folder_path, filename)
        return filepath

    # Single Cycle Function, may throw into thread
    def SingleCycle(self):
        self.cycle_running = True
        
        # creating folders
        self.PositionFolders()

        # check if night time and pass if it is
        if self.in_between(datetime.now().time(),
                           self.timelapse_start_of_night.time(),
                           self.timelapse_end_of_night.time()):
            log.debug('It is nighttime, not running cycle')
        else: # it is not nighttime
            #cycle_thread = threading.Thread(target=self.SingleCycleThread)
            self.run_threaded(self.SingleCycleThread)
            '''try:
                if self.cycle_running is True:
                    cycle_thread.start()
                    cycle_thread.join() #wait until done, may not need
                    self.cycle_running = False
            except:
                logger.debug("Single cycle thread failed")
                cycle_thread = None'''
            
    # Thread for single cycle
    def SingleCycleThread(self):
        log.debug('single cycle thread is running')
        commands = self.grbl_commands.ReturnFileAsList()
        self.lights_ar.GrowlightsOff()
        self.lights_ar.BackLightsOn()
        
        first_command = commands[0] # slicing first command off (ususally homing)
        commands = commands[1:-(8-int(self.num_of_pos))]
        self.grbl_ar.ser_port.ser.flushInput()        # flush input messages
        sleep(0.1)
        self.grbl_ar.Send_Serial(first_command)
        sleep(3)

        #iterate through each position
        for position in commands:
        #move to position
            if self.cycle_running is True:
                self.grbl_ar.Send_Serial(position)
                if not 'H' in position: #if not homing command
                    #wait until at position
                    sleep(5)
                    filepath = self.Filepath_Set(commands.index(position)) #check that this creates right things #TODO MAKE SURE WORK
                    self.camera.CaptureImage(filepath)
                    sleep(1)
            else:
                #self.grbl_ar.Home_Command()
                pass
        
        #if cancelled during cycle, send reset and home command
        if self.cycle_running is False:
                self.grbl_ar.GRBLSoftReset() # reset GRBL
                self.grbl_ar.HomeCommand()
            
        self.grbl_ar.HomeCommand()
        self.lights_ar.GrowlightsOn()
        self.lights_ar.BackLightsOff()

    # Sees if time is between two ppints, useful for determining nighttime
    def in_between(self, now, start, end):
        #logger.debug("start is {}".format(start))
        #logger.debug("end is {}".format(end))
        #logger.debug("now is {}".format(now))
        if start <= end:
            return start <= now < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= now or now < end

    #Stops Single Cycle Function
    def StopCycle(self):
        logging.info('stopping single cycle thread')
        self.cycle_running = False # finish last move then joining thread

    #Starts Timelapse
    def StartTimelapse(self):
        logging.info('Starting timelapse')
        self.timelapse_running = True
        
        # creating folders
        self.PositionFolders()

        if self.timelapse_running is True:
                    #starting cycle
            self.SingleCycle()
        
            current_date = datetime.now()

            schedule.every(self.timelapse_interval).hours.until(self.timelapse_end_date).do(self.run_threaded, self.SingleCycle) #can change and set schedule with this using GUI!
            schedule.every().day.at(self.timelapse_start_of_night.strftime('%H:%M')).do(self.run_threaded, self.GrowLights_Off)
            schedule.every().day.at(self.timelapse_end_of_night.strftime('%H:%M')).do(self.run_threaded, self.GrowLights_On)
            
            self.stop_run_continously = self.run_continuously()
            log.info("All jobs on schedule is {}".format(schedule.get_jobs()))
            
    # example from schedule library website
    # link: https://schedule.readthedocs.io/en/stable/background-execution.html
    def run_continuously(self, interval=1): 
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(interval)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run
    
    #from scheduler documentation of parallel execution
    # https://schedule.readthedocs.io/en/stable/parallel-execution.html
    def run_threaded(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()

    #Stops Timelapse
    def StopTimelapse(self):
        logging.info('Stopping timelapse')
        self.stop_run_continously.set() #stopping continous run thread
        self.timelapse_running = False
    
    def BackLights_On(self):
        logging.debug('Turning backlights on from machine class')
        self.lights_ar.BackLightsOn()
    
    def BackLights_Off(self):
        logging.debug('Turning backlights off from machine class')
        self.lights_ar.BackLightsOff()
        
    def GrowLights_On(self):
        logging.debug('Turning growlights on from machine class')
        self.lights_ar.GrowlightsOn()
        
    def GrowLights_Off(self):
        logging.debug('Turning growlights off from machine class')
        self.lights_ar.GrowlightsOff()

    #event handling
    def AddSubscribersForOnConnectedGRBLEvent(self, objMethod):
        self.OnGRBLConnected += objMethod

    def AddSubscrubersForOffConnectedGRBLEvent(self, objMethod):
        self.OffGRBLConnected += objMethod

    def AddSubscribersForOnLightConnectedEvent(self, objMethod):
        self.OnLightConnected += objMethod

    def AddSubscriberForOffLightConnectedEvent(self, objMethod):
        self.OffLightConnected += objMethod

    def AddSubscribersForOnLoadCameraSettingsEvent(self, objMethod):
        self.OnCameraSettingsLoaded += objMethod

    def AddSubscriberForOffLoadCameraSettingsEvent(self, objMethod):
        self.OffCameraSettingsLoaded += objMethod

    def __del__(self):
        # stopping schedule jobs
        if self.timelapse_running is True: #if set
            log.debug("stopping timelapse with setting")
            self.stop_run_continously.set() #stopping continous run thread
        
        #deleting other objects
        self.grbl_ar.__del__()
        self.lights_ar.__del__()
        #self.camera.__del__() #may not need to delete

