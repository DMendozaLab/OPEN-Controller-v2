#Lights Arduino Subclass

from Util.Arduino_Class import Arduino

class Lights_Arduino(Arduino):

    backlight_state: bool = False
    growlight_state: bool = False
    
    def __init__(self, portname):
        super(Lights_Arduino, self).__init__(portname)

        # clearing on startup the lights
        #self.AllOff()
        self.BackLightsOff()
        self.GrowlightsOn()

    ### Combined Functions ###

    # Turns on all of lights
    def AllOn(self):
        self.BackLightsOn()
        self.GrowlightsOn()

    # Turns off all lights
    def AllOff(self):
        self.BackLightsOff()
        self.GrowlightsOff()

    ### Manually Functions ###

    # turning on Backlights when called with command
    def BackLightsOn(self):
        #try: 
        self.ser_port.Write_Data('S2V1\n') #or whatever command is
        self.backlight_state = True
        #except serial.SerialTimeException as e:
        #    log.error("Serial Time Exception for BacklightsOn()")

    # Turns off Backlights when called
    def BackLightsOff(self):
        #try: 
        self.ser_port.Write_Data('S2V0\n')
        self.backlight_state = False
        #except serial.SerialTimeException as e:
            #log.error("Serial Time Exception for BacklightsOff()")
        

    # Turns on Growlight Relay signal on arduino
    def GrowlightsOn(self):
        #try: 
        self.ser_port.Write_Data('S1V1\n')
        self.growlight_state = True
        #except serial.SerialTimeException as e:
        #    log.error("Serial Time Exception for GrowlightsOn()")

    #Turns off Growlight Relay Signal on arduino
    def GrowlightsOff(self):
        #try:
        self.ser_port.Write_Data('S1V0\n')
        self.growlight_state = False
        #except serial.SerialTimeException as e:
            #log.error("Serial Time Exception for GrowlightsOff()")
        
        
    ### Getter and Setter Functions ###

    #Encapsulation Functions
    def GetBackLightStatus(self):
        return self.backlight_state

    def SetBackLightStatus(self, state: bool):
        self.backlight_state = state

    def GetGrowlightStatus(self):
        return self.growlight_state

    def SetGrowlightStatus(self, state: bool):
        self.growlight_state = state
        
        
    ###  Delete Function ### 

    # deleting method that turns off lights on way out
    def __del__(self):
        #self.AllOff()
        self.BackLightsOff()
        # Growlights are normally closed relay so leaving on to not hurt relay when shutting down
        # can be manually turned off with switch on cord
        self.GrowlightsOn() 

