#frame for manual control of GUI
import logging
import tkinter as tk
from tkinter import ttk
from Util.Event import Event_Obj


log = logging.getLogger('open_controller_log.log')

class ManualControlFrame(tk.Frame):

    numPos = ('$H', '1', '2', '3', '4', '5', '6', '7')

    OnPositionNumChanged = Event_Obj()
    OnMoveToEvent = Event_Obj()
    OnCaptureImageEvent = Event_Obj()
    OnBacklightsOnEvent = Event_Obj()
    OnBacklightsOffEvent = Event_Obj()
    OnGrowlightsOnEvent = Event_Obj()
    OnGrowlightsOffEvent = Event_Obj()

    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        #Label of Manual Control
        tk.Label(self, text='Manual Control').grid(row=0,
                                                   column=0,
                                                   columnspan=4,
                                                   sticky='ew',
                                                   padx=5,
                                                   pady=5)

        #Position Num and manual move
        PositionNumber_title = tk.Label(self, text='Position #: ').grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.PositionNumber_combobox = ttk.Combobox(self, width=3, textvariable=tk.StringVar())
        self.PositionNumber_combobox['values'] = self.numPos
        self.PositionNumber_combobox['state'] = 'readonly'
        self.PositionNumber_combobox.current(0)
        self.PositionNumber_combobox.bind('<<ComboboxSelected>>', func=self.PositionNum_combo_changed)
        self.PositionNumber_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='e')

        self.MoveTo_Button = tk.Button(self, text='Move To', command=self.MoveTo_Button_Clicked)
        self.MoveTo_Button.grid(row=1, column=2, columnspan=2, sticky='ew', padx=5, pady=5, ipadx=30, ipady=5)

        #Capture Image Manual
        Camera_capture_manual = tk.Label(self, text='Manual Image Capture: ').grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        self.Camera_capture_image_btn = tk.Button(self, text='Capture Image', command=self.ManualImageCaputre)
        self.Camera_capture_image_btn.grid(row=2, column=2, padx=5, pady=5, ipadx=30, ipady=5, columnspan=2, sticky='ew')

        #Backlights manual on/off
        Manual_backlights_label = tk.Label(self, text='Backlight Controls: ').grid(row=3, column=0, padx=5, pady=5, columnspan=2, sticky='e')

        self.manual_backlight_on_btn = tk.Button(self, text='On', command=self.ManualBacklightOnBtn)
        self.manual_backlight_on_btn.grid(row=3, column=2, padx=5, pady=5, sticky='ew', ipady=5)

        self.manual_backlight_off_btn = tk.Button(self, text='Off', command=self.ManualBacklightOffBtn)
        self.manual_backlight_off_btn.grid(row=3, column=3, padx=5, pady=5, sticky='ew', ipady=5)

        #Growlight manual on/off
        Manual_growlight_label = tk.Label(self, text='Growlight Controls: ').grid(row=4, column=0, padx=5 , pady=5, columnspan=2, sticky='e')

        self.manual_growlight_on_btn = tk.Button(self, text='On', command=self.ManualGrowlightOnBtn)
        self.manual_growlight_on_btn.grid(row=4, column=2, padx=5, pady=5, ipady=5, sticky='ew')

        self.manual_growlight_off_btn = tk.Button(self, text='Off', command=self.ManualGrowlightOffBtn)
        self.manual_growlight_off_btn.grid(row=4, column=3, padx=5, pady=5, ipady=5, sticky='ew')

    # set current position in grbl class
    def PositionNum_combo_changed(self, event):
        log.debug('Position num combo box changed')
        #self.OnPositionNumChanged(self.PositionNumber_combobox.get())

    # move machine to position
    def MoveTo_Button_Clicked(self):
        self.OnMoveToEvent(self.PositionNumber_combobox.get()) #passing the position number selected to machine
        log.info('Move to button pressed')

    # manually capture image
    def ManualImageCaputre(self):
        self.OnCaptureImageEvent(self.PositionNumber_combobox.get())
        log.info('Manual Image Button clicked')

    #turns on backlight on manually
    def ManualBacklightOnBtn(self):
        self.OnBacklightsOnEvent()
        log.info('Manual backlight on btn pressed')

    #manually turn backlights off
    def ManualBacklightOffBtn(self):
        self.OnBacklightsOffEvent()
        log.info('Manual backlight off btn pressed')

    #manually turn growlight on
    def ManualGrowlightOnBtn(self):
        self.OnGrowlightsOnEvent()
        log.info('Manual Growlight on btn pressed')

    #manually turn growlight off
    def ManualGrowlightOffBtn(self):
        self.OnGrowlightsOffEvent()
        log.info("Manual Growlight off btn pressed")

    #Event Subscruber Functions
    def AddSubscriberForPositionNumChanged(self, objMethod):
        self.OnPositionNumChanged += objMethod

    def AddSubscriberForMoveToBtnPressed(self, objMethod):
        self.OnMoveToEvent += objMethod

    def AddSubscriberForManualImageCaptureBtnPressed(self, objMethod):
        self.OnCaptureImageEvent += objMethod

    def AddSubscriberForManualBacklightOnBtnPressed(self, objMethod):
        self.OnBacklightsOnEvent += objMethod

    def AddSubscriberForManualBacklightOffBtnPressed(self, objMethod):
        self.OnBacklightsOffEvent += objMethod

    def AddSubscriberForManualGrowlightOnBtnPressed(self, objMethod):
        self.OnGrowlightsOnEvent += objMethod

    def AddSubscriberForManualGrowlightOffBtnPressed(self, objMethod):
        self.OnGrowlightsOffEvent += objMethod