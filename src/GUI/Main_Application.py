#main window application

import tkinter as tk
from GUI.Frames.Timelapse_Frame import TimelapseFrame
from GUI.Frames.Single_Cycle_Frame import SingleCycle
from GUI.Frames.Status_Frame import StatusFrame
from GUI.Frames.Title_Frame import Title
from GUI.Frames.Manual_Control_Frame import ManualControlFrame

#main frame
class MainApplication(tk.Frame):

    #machine = Machine
    def __init__(self, parent, Machine):
        tk.Frame.__init__(self)
        self.machine = Machine

        Title(parent).grid(row=0, column=0)
        self.status_frame = StatusFrame(self, self.machine)
        self.status_frame.grid(row=1, column=0)
        self.single_cycle = SingleCycle(self)
        self.single_cycle.grid(row=2, column=0)
        self.timelapse_frame = TimelapseFrame(self, self.machine)
        self.timelapse_frame.grid(row=3, column=0)
        self.manual_control_frame = ManualControlFrame(self, self.machine)
        self.manual_control_frame.grid(row=4, column=0)

        #Event Handling Setting Subscribers#

        #single cycle
        self.single_cycle.AddSubscriberForOnSingleCycleEvent(self.machine.SingleCycle)
        self.single_cycle.AddSubscribersForOnStopSingleCycleEvent(self.machine.StopCycle)

        #status events
        '''self.machine.AddSubscribersForOnConnectedGRBLEvent(self.status_frame.ChangeGRBLStatusOn)
        self.machine.AddSubscrubersForOffConnectedGRBLEvent(self.status_frame.ChangeGRBLStatusOff)
        self.machine.AddSubscribersForOnLightConnectedEvent(self.status_frame.ChangeLightsStatusOn)
        self.machine.AddSubscriberForOffLightConnectedEvent(self.status_frame.ChangeLightsStatusOff)
        self.machine.AddSubscribersForOnLoadCameraSettingsEvent(self.status_frame.ChangeCameraSettingsOn)
        self.machine.AddSubscriberForOffLoadCameraSettingsEvent(self.status_frame.ChangeCameraSettingsOff())'''
        self.status_frame.AddSubscriberSaveFolderPathChanged(self.machine.SetSaveFolderPath)
        self.status_frame.AddSubscriberPositionTickerChanged(self.machine.SetNumOfPos)

        #manual frame events, will fill out in future when finish with machine
        #self.manual_control_frame.AddSubscriberForPositionNumChanged(self.machine.SetCurrentPosition)
        self.manual_control_frame.AddSubscriberForMoveToBtnPressed(self.machine.MoveTo)
        self.manual_control_frame.AddSubscriberForManualImageCaptureBtnPressed(self.machine.CaptureImageManual)
        self.manual_control_frame.AddSubscriberForManualBacklightOnBtnPressed(self.machine.BackLights_On)
        self.manual_control_frame.AddSubscriberForManualBacklightOffBtnPressed(self.machine.BackLights_Off)
        self.manual_control_frame.AddSubscriberForManualGrowlightOnBtnPressed(self.machine.GrowLights_On)
        self.manual_control_frame.AddSubscriberForManualGrowlightOffBtnPressed(self.machine.GrowLights_Off)

        #timelapse frame events
        self.timelapse_frame.AddSubscriberOnStartButtonPressed(self.machine.StartTimelapse)
        self.timelapse_frame.AddSubscriberOnStopButtonPressed(self.machine.StopTimelapse)
        self.timelapse_frame.AddSubscriberOnIntervalChanged(self.machine.SetTimelapseInterval)
        #self.timelapse_frame.AddSubscriberOnIntervalUnitChanged(self.) #if changing timelapse interval
        self.timelapse_frame.AddSubscriberOnEndDateChanged(self.machine.SetTimelapseEndDate)
        self.timelapse_frame.AddSubscriberOnStartNightChanged(self.machine.SetTimelapseStartOfNight)
        self.timelapse_frame.AddSubscriberOnEndNightChanged(self.machine.SetTimelapseEndOfNight)