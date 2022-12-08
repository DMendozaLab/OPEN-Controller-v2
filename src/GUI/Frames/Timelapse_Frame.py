#Timelapse frame for UI
import logging
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkcalendar

#for event handling
from Util.Event import Event_Obj

log = logging.getLogger('open_controller_log.log')

#TODO
#-implement the events for this frame


class TimelapseFrame(tk.Frame):

    #Will need to set default values for machine because only updates when changed

    OnIntervalChanged = Event_Obj()
    OnIntervalUnitsChanged = Event_Obj()
    OnEndDateChanged = Event_Obj()
    OnStartNightChanged = Event_Obj()
    OnEndNightChanged = Event_Obj()
    OnStartButtonPressed = Event_Obj()
    OnStopButtonPressed = Event_Obj()

    #init
    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        #self['bg']='red'      #finding messed up grid things
        #self.grid(sticky='ew')
        self.machine = Machine

        time_units = ('hours', 'days', 'weeks')
        decimal_units = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
        clock_units = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')

        #timelapse title
        Timelapse_title = tk.Label(self, text='Timelapse').grid(row=0, column=0, columnspan=6, sticky='EW')

        #interval
        Interval_title = tk.Label(self, text='Interval:').grid(row=1, column=0)

        self.Interval_combobox = ttk.Combobox(self, width=3, textvariable=tk.StringVar())
        self.Interval_combobox['values'] = decimal_units
        self.Interval_combobox['state'] = 'readonly'
        self.Interval_combobox.current(1)
        self.Interval_combobox.bind('<<ComboboxSelected>>', func=self.Interval_dec_set)
        self.Interval_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.Interval_combobox_time_unit = ttk.Combobox(self, width=5, textvariable=tk.StringVar())
        self.Interval_combobox_time_unit['values'] = time_units
        self.Interval_combobox_time_unit['state'] = 'readonly'
        self.Interval_combobox_time_unit.current(0)
        self.Interval_combobox_time_unit.bind('<<ComboboxSelected>>', func=self.Interval_time_unit_set)
        self.Interval_combobox_time_unit.grid(row=1, column=2, padx=5, pady=5)

        #end date
        End_date = tk.Label(self, text="End Date:").grid(row=1, column=3)

        self.end_date_cal = tkcalendar.DateEntry(self, borderwidth=2)
        self.end_date_cal.configure(justify='center')
        self.end_date_cal.grid(row=1, column=4, padx=5, pady=5, columnspan=2, sticky='ew')
        self.end_date_cal.bind('<<DateEntrySelected>>', self.EndDateEntrySelected)

        #label = tk.Label(self, text='test').grid(row=1, column=5)

        #Night time selection
        night_time_label = tk.Label(self, text='Night Time Selection').grid(row=3, column=0, columnspan=6, sticky='ew')

        #Start of Night
        start_night_label = tk.Label(self, text='Start of Night:').grid(row=4, column=0, padx=5, pady=5)

        self.start_night_time = ttk.Combobox(self, width=3, textvariable=tk.StringVar())
        self.start_night_time['values'] = clock_units
        self.start_night_time['state'] = 'readonly'
        self.start_night_time.current(8)
        self.start_night_time.bind('<<ComboboxSelected>>', func=self.StartNightComboChanged)
        self.start_night_time.grid(row=4, column=1, padx=5, pady=5)

        pm_label = tk.Label(self, text="PM").grid(row=4, column=2, padx=5, pady=5)

        #end of night
        end_night_label = tk.Label(self, text='End of Night').grid(row=4, column=3, padx=5, pady=5)

        self.end_night_time = ttk.Combobox(self, width =3, textvariable=tk.StringVar())
        self.end_night_time['values'] = clock_units
        self.end_night_time['state'] = 'readonly'
        self.end_night_time.current(6)
        self.end_night_time.bind('<<ComboboxSelected>>', func=self.EndNightComboChanged)
        self.end_night_time.grid(row=4, column=4, padx=5, pady=5)

        am_label = tk.Label(self, text='AM').grid(row=4, column=5, padx=5, pady=5)

        #Start and Stop Button
        self.Start_Button = tk.Button(self, text='Start', command=self.Start_Button)
        self.Start_Button.grid(row=5, column=0, columnspan=3,
                               padx=5, ipadx=20, pady=5, ipady=5,
                               sticky='ew')

        self.Stop_Button = tk.Button(self, text='Stop', command=self.Stop_Button)
        self.Stop_Button.grid(row=5, column=3, columnspan=3,
                              padx=5, ipadx=30, pady=5, ipady=5,
                              sticky='ew')

    def EndNightComboChanged(self, event):
        log.info("End of night is {} AM".format(self.end_night_time.get()))
        self.OnEndNightChanged(self.end_night_time.get())

    def StartNightComboChanged(self, event ):
        log.info("Start of Night is {} PM".format(self.start_night_time.get()))
        start_of_night_pm = int(self.start_night_time.get()) + 12
        log.info("Start of Night is {} PM".format(start_of_night_pm))
        self.OnStartNightChanged(str(start_of_night_pm))

    def EndDateEntrySelected(self, event):
        log.info("Selected end date is {}".format(self.end_date_cal.get_date()))
        self.OnEndDateChanged(self.end_date_cal.get_date())

    def Interval_dec_set(self, event):
        #set value of machine timelapse interval here
        log.info('The value of timelapse interval is: ' + self.Interval_combobox.get())
        self.OnIntervalChanged(self.Interval_combobox.get())

    def Interval_time_unit_set(self, event):
        #set time unit for timelapse
        log.info('Timelapse interval time unit is ' + self.Interval_combobox_time_unit.get())
        self.OnIntervalUnitsChanged(self.Interval_combobox_time_unit.get())

    def End_date_interval_set(self, event):
        #set end date interval
        log.info('End Date interval is: ' + self.End_date_dec.get())

    def End_date_time_set(self, event):
        #setting time unit for end date
        log.info('End date time unit is: ' + self.End_date_time.get())

    def Start_Button(self):
        #starting timelapse
        log.info("Starting Cycle...")
        self.OnStartButtonPressed()

    def Stop_Button(self):
        #stopping timelapse
        log.info("Stopping Cycle...")
        self.OnStopButtonPressed()

    #Event Subscribing Functions
    def AddSubscriberOnIntervalChanged(self, objMethod):
        self.OnIntervalChanged += objMethod

    def AddSubscriberOnIntervalUnitChanged(self, objMethod):
        self.OnIntervalUnitsChanged += objMethod

    def AddSubscriberOnEndDateChanged(self, objMethod):
        self.OnEndDateChanged += objMethod

    def AddSubscriberOnStartNightChanged(self, objMethod):
        self.OnStartNightChanged += objMethod

    def AddSubscriberOnEndNightChanged(self, objMethod):
        self.OnEndNightChanged += objMethod

    def AddSubscriberOnStartButtonPressed(self, objMethod):
        self.OnStartButtonPressed += objMethod

    def AddSubscriberOnStopButtonPressed(self, objMethod):
        self.OnStopButtonPressed += objMethod
