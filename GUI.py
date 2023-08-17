import tkinter
import yaml

class GUI:
    def __init__(self):
        self.status = True
        self.window = tkinter.Tk()
        self.window.title("Mouse Pupil and Speed Tracker")

        self.frame = tkinter.Frame(self.window)
        self.frame.pack()

        with open("Data/config.yaml", "r") as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)


        #####################################
        ###     CONTROLLER CONDITIONS     ###
        #####################################

        #Frame
        self.cc =tkinter.LabelFrame(self.frame, text="Controller Conditions")
        self.cc.grid(row= 0, column=0, padx=20, pady=10)

        # Z-Score Threshold Box
        self.cc_zscoreThresh = tkinter.Label(self.cc, text="Z-Score Threshold")
        self.cc_zscoreThresh.grid(row=0, column=0)
        self.cc_zscoreEntry = tkinter.Entry(self.cc)
        self.cc_zscoreEntry.grid(row=1, column=0)
        self.cc_zscoreEntry.insert(0, self.config["EYE_THRESHOLD"])

        # Time Threshold Box
        self.cc_activationTime = tkinter.Label(self.cc, text="Timed Activation (s)")
        self.cc_activationTime.grid(row=0, column=1)
        self.cc_activationTimeEntry = tkinter.Entry(self.cc)
        self.cc_activationTimeEntry.grid(row=1, column=1)
        self.cc_activationTimeEntry.insert(0, self.config["ACTIVATION_TIME"])

        # Speed Threshold Box
        self.cc_speedThresh = tkinter.Label(self.cc, text="Speed Threshold (cm/s)")
        self.cc_speedThresh.grid(row=2, column=0)
        self.cc_speedThreshEntry = tkinter.Entry(self.cc)
        self.cc_speedThreshEntry.grid(row=3, column=0)
        self.cc_speedThreshEntry.insert(0, self.config["SPEED_THRESHOLD"])

        # Deactivation Time
        self.cc_deactivationTime = tkinter.Label(self.cc, text="Timed Deactivation (s)")
        self.cc_deactivationTime.grid(row=2, column=1)
        self.cc_deactivationTimeEntry = tkinter.Entry(self.cc)
        self.cc_deactivationTimeEntry.grid(row=3, column=1)
        self.cc_deactivationTimeEntry.insert(0, self.config["DEACTIVATION_TIME"])

        for widget in self.cc.winfo_children():
            widget.grid_configure(padx=10, pady=5)


        ################################
        ###     SAMPLE AND TRIAL     ###
        ################################
        self.st = tkinter.LabelFrame(self.frame, text="Sample and Trial Conditions")
        self.st.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        self.st_sampleDuration = tkinter.Label(self.st, text="Sampling Duration (s)")
        self.st_sampleDuration.grid(row=0, column=0)
        self.st_sampleDurationEntry = tkinter.Entry(self.st)
        self.st_sampleDurationEntry.grid(row=1, column=0)
        self.st_sampleDurationEntry.insert(0, self.config["SAMPLE_DURATION"])

        self.st_trialDuration = tkinter.Label(self.st, text="Trial Duration (s)")
        self.st_trialDuration.grid(row=0, column=1)
        self.st_trialDurationEntry = tkinter.Entry(self.st)
        self.st_trialDurationEntry.grid(row=1, column=1)
        self.st_trialDurationEntry.insert(0, self.config["TRIAL_DURATION"])

        for widget in self.st.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Button
        self.button = tkinter.Button(self.frame, text="Start", command = self.checkData, bg='green')
        self.button.grid(row=3, column=0, sticky="news", padx=20, pady=10)


    def checkData(self):
        configDict = {}

        configDict["EYE_THRESHOLD"] = self.cc_zscoreEntry.get()
        configDict["ACTIVATION_TIME"] = self.cc_activationTimeEntry.get()
        configDict["SPEED_THRESHOLD"] = self.cc_speedThreshEntry.get()
        configDict["DEACTIVATION_TIME"] = self.cc_deactivationTimeEntry.get()
        configDict["SAMPLE_DURATION"] = self.st_sampleDurationEntry.get()
        configDict["TRIAL_DURATION"] = self.st_trialDurationEntry.get()

        for i in configDict:
            try:
                float(configDict[i])
            except ValueError:
                tkinter.messagebox.showwarning(title= "Error", message="Invalid Numeric Options")
                return
            
        if float(configDict["ACTIVATION_TIME"]) < 0 or float(configDict["DEACTIVATION_TIME"]) < 0 or float(configDict["SAMPLE_DURATION"]) < 0 or float(configDict["TRIAL_DURATION"]) < 0:
            tkinter.messagebox.showwarning(title= "Error", message="Cannot have negative time")
            return
        
        self.config["EYE_THRESHOLD"] = float(configDict["EYE_THRESHOLD"])
        self.config["ACTIVATION_TIME"] = float(configDict["ACTIVATION_TIME"])
        self.config["SPEED_THRESHOLD"] = float(configDict["SPEED_THRESHOLD"])
        self.config["DEACTIVATION_TIME"] = float(configDict["DEACTIVATION_TIME"])
        self.config["SAMPLE_DURATION"] = float(configDict["SAMPLE_DURATION"])
        self.config["TRIAL_DURATION"] = float(configDict["TRIAL_DURATION"])

        with open("Data/config.yaml", 'w') as file:
            yaml.dump(self.config, file)  
        
        self.status = False
        self.window.quit()

    def getStatus(self):
        return self.status
 
    def start(self):
        self.window.mainloop()
        for child in self.window.winfo_children(): 
            child.destroy()
        self.window.destroy()
        del self.window
        print("Done")