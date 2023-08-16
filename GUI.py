import tkinter
from tkinter import ttk
from tkinter import messagebox
import yaml

status = True

def checkData():
    configDict = {}

    configDict["EYE_THRESHOLD"] = cc_zscoreEntry.get()
    configDict["ACTIVATION_TIME"] = cc_activationTimeEntry.get()
    configDict["SPEED_THRESHOLD"] = cc_speedThreshEntry.get()
    configDict["DEACTIVATION_TIME"] = cc_deactivationTimeEntry.get()
    configDict["SAMPLE_DURATION"] = st_sampleDurationEntry.get()
    configDict["TRIAL_DURATION"] = st_trialDurationEntry.get()

    for i in configDict:
        try:
            float(configDict[i])
        except ValueError:
            tkinter.messagebox.showwarning(title= "Error", message="Invalid Numeric Options")
            return
        
    if float(configDict["ACTIVATION_TIME"]) < 0 or float(configDict["DEACTIVATION_TIME"]) < 0 or float(configDict["SAMPLE_DURATION"]) < 0 or float(configDict["TRIAL_DURATION"]) < 0:
        tkinter.messagebox.showwarning(title= "Error", message="Cannot have negative time")
        return
    
    config["EYE_THRESHOLD"] = float(configDict["EYE_THRESHOLD"])
    config["ACTIVATION_TIME"] = float(configDict["ACTIVATION_TIME"])
    config["SPEED_THRESHOLD"] = float(configDict["SPEED_THRESHOLD"])
    config["DEACTIVATION_TIME"] = float(configDict["DEACTIVATION_TIME"])
    config["SAMPLE_DURATION"] = float(configDict["SAMPLE_DURATION"])
    config["TRIAL_DURATION"] = float(configDict["TRIAL_DURATION"])

    with open("config.yaml", 'w') as file:
        yaml.dump(config, file)  

    window.destroy()
    status = False

def getStatus():
    return status

window = tkinter.Tk()
window.title("Mouse Pupil and Speed Tracker")

frame = tkinter.Frame(window)
frame.pack()

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
#####################################
###     CONTROLLER CONDITIONS     ###
#####################################

#Frame
cc =tkinter.LabelFrame(frame, text="Controller Conditions")
cc.grid(row= 0, column=0, padx=20, pady=10)

# Z-Score Threshold Box
cc_zscoreThresh = tkinter.Label(cc, text="Z-Score Threshold")
cc_zscoreThresh.grid(row=0, column=0)
cc_zscoreEntry = tkinter.Entry(cc)
cc_zscoreEntry.grid(row=1, column=0)
cc_zscoreEntry.insert(0, config["EYE_THRESHOLD"])

# Time Threshold Box
cc_activationTime = tkinter.Label(cc, text="Timed Activation (s)")
cc_activationTime.grid(row=0, column=1)
cc_activationTimeEntry = tkinter.Entry(cc)
cc_activationTimeEntry.grid(row=1, column=1)
cc_activationTimeEntry.insert(0, config["ACTIVATION_TIME"])

# Speed Threshold Box
cc_speedThresh = tkinter.Label(cc, text="Speed Threshold (cm/s)")
cc_speedThresh.grid(row=2, column=0)
cc_speedThreshEntry = tkinter.Entry(cc)
cc_speedThreshEntry.grid(row=3, column=0)
cc_speedThreshEntry.insert(0, config["SPEED_THRESHOLD"])

# Deactivation Time
cc_deactivationTime = tkinter.Label(cc, text="Timed Deactivation (s)")
cc_deactivationTime.grid(row=2, column=1)
cc_deactivationTimeEntry = tkinter.Entry(cc)
cc_deactivationTimeEntry.grid(row=3, column=1)
cc_deactivationTimeEntry.insert(0, config["DEACTIVATION_TIME"])

for widget in cc.winfo_children():
    widget.grid_configure(padx=10, pady=5)


################################
###     SAMPLE AND TRIAL     ###
################################
st = tkinter.LabelFrame(frame, text="Sample and Trial Conditions")
st.grid(row=1, column=0, sticky="news", padx=20, pady=10)

st_sampleDuration = tkinter.Label(st, text="Sampling Duration (s)")
st_sampleDuration.grid(row=0, column=0)
st_sampleDurationEntry = tkinter.Entry(st)
st_sampleDurationEntry.grid(row=1, column=0)
st_sampleDurationEntry.insert(0, config["SAMPLE_DURATION"])

st_trialDuration = tkinter.Label(st, text="Trial Duration (s)")
st_trialDuration.grid(row=0, column=1)
st_trialDurationEntry = tkinter.Entry(st)
st_trialDurationEntry.grid(row=1, column=1)
st_trialDurationEntry.insert(0, config["TRIAL_DURATION"])

for widget in st.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tkinter.Button(frame, text="Start", command = checkData, bg='green')
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
 
window.mainloop()