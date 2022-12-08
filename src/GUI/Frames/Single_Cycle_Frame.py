#single cycle control frames

import tkinter as tk
from Util.Event import Event_Obj

class SingleCycle(tk.Frame):

    OnSingleCycle = Event_Obj()
    OnStopSingleCycle = Event_Obj()

    #init
    def __init__(self, parent): #no need to pass machine I think
        tk.Frame.__init__(self, width=600)

        Single_cycle_label = tk.Label(self, text='Single Cycle').grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.Start_button = tk.Button(self, text='Start', command=self.startButton)
        self.Start_button.grid(row=1, column=0, padx=5, pady=5, ipadx=60, ipady=5, sticky='ew')

        self.Stop_Button = tk.Button(self, text='Stop', command=self.stopButton)
        self.Stop_Button.grid(row=1, column=1, padx=5, pady=5, ipadx=60, ipady=5, sticky='ew')

    #Frame Functions
    def startButton(self):
        self.OnSingleCycle()
        #print('start')

    def stopButton(self):
        self.OnStopSingleCycle()
        #stop cycle

    #Event Handling
    def AddSubscriberForOnSingleCycleEvent(self, objMethod):
        self.OnSingleCycle += objMethod

    def AddSubscribersForOnStopSingleCycleEvent(self, objMethod):
        self.OnStopSingleCycle += objMethod