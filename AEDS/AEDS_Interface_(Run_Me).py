"""
AEDS User Interface: This software allows the user to interact with the Audio Emotion Detection (AEDS)
	software through a GUI.
	This interface contains two text fields and two buttons.
	For information on how to properly use this  interface, please see the README file included with
	this document.
Authors: Base code written by Michael Knapp. Edits made by Humberto Colin, Bryan Jones, Timmothy Lane, Alex Shannon,
	and Mark Webb.
Related Software Requirements: FR.7, FR.8, FR.10, FR.11, EIR.1, EIR.2, EIR.3, EIR.4, EIR.5
"""


from tkinter import *
import tkinter as tk
import pyaudio
import Recording
import emotionProcessor
from tkinter import Menu
from tkinter import messagebox as mbox
import scikit_network
from statistics import stdev
import numpy as np
from profileManager import *
from os import *

# Hardcoded Variables 
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
wave_output_filename = "user_recording.wav"



# Code to create the window for the GUI.
# this class sets up the frame which is the entire window needed to fit the GUI buttons and lable's inside.

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(column = 1, row = 5)
               
        self.create_widgets()
        self.recorder=Recording.Recording(wave_output_filename, CHANNELS, RATE, CHUNK)
        self.processor=emotionProcessor.EmotionProcessor(wave_output_filename)
        self.recordingtest = False

        

    
   # class widgets.. this is where the code for each off six buttons two lable's and two text boxes are held.
   # Grid not pack is used.
   # grid= where is that button on label located in the frame.
   # each button has a command atribute that connects the button with a function that controls what the button does.
   
    def create_widgets(self):
       
        #Start button, which begins the recording process.
	#Related Software Requirements: EIR.1, EIR.2
        self.startButton = Button(self, text = " Start: recording          " , justify = "center", command = self.recordAudio, bg = "lightgray")
        self.startButton.grid(row = 0, column = 0)
        
        # Stop button, which ends the recording process and begins the process of metric extraction/comparison.
	# Related Software Requirements: EIR.4
        self.stopButton = Button(self, text = " Stop: recording          " , justify = "center", command = self.endAudio, bg ="lightgray")
        self.stopButton.grid(row = 1, column = 0)
        
        
        # Label for the output below "user Id or name".
        # Related Software Requirements: FR.7, FR.8
        self.label = Label(self, text = "User Name:               ", font = 13, justify = "left")
        self.label.grid(column = 1, row = 0)
    
        #output for the User id
        self.user = StringVar()
        self.txt = Entry(self, textvariable = self.user, width = 32)
        self.txt.grid(column = 1, row = 1)
            
        # Label for the GUI that Says " predicted emotion".        
        self.label = Label (self, text = "Predicted Emotion:    ",font = 13, justify = "left")
        self.label.grid(column = 1, row = 2)
        
        # Output field for the label where the predicted emotion will be added when the kNN processed the audio matrics hopefully correctly. 
        # Related Softare Requirements: FR.10, EIR.5
        self.emotionalPrediction = StringVar()
        self.text = Entry(self, textvariable = self.emotionalPrediction, width = 32)
        self.text.grid(column = 1, row = 3)

        
        #this function was written by Alex
    def recordAudio(self):
        if(self.recordingtest == True):
	        print("Already Recording!")
        else:
	        self.recorder=Recording.Recording(wave_output_filename, CHANNELS, RATE,CHUNK)
	        self.recorder.startAudio()
	        self.emotionalPrediction.set("Recording..")
	        self.recordingtest= True
        return self
    # End audio also needs a popup button.
    
    def endAudio(self):
        if(self.recordingtest == True):
            #Stop recording audio
            self.recorder.stopAudio()

            #Set the box containing the emotional prediction to be blank
            self.emotionalPrediction.set("Done Recording.")

            #Get the entered user name from the entry box
            self.userName = self.user.get()

            # Call the method to get the audio metrics
            self.audio_metrics = self.processor.collectMetrics()

            # Create a user profile object using the entered user name
            self.user_profile = profileManager(self.userName)

            # Access the profile for the given user
            self.user_profile.accessProfile()

            #Get the prediction from the scikit network
            self.predicted = scikit_network.compare_new(self.audio_metrics, self.user_profile)
            self.emotionalPrediction.set(self.predicted[0])

            #Delete the recorded audio file
            os.remove("user_recording.wav")

            #yes no box asking if returned emotion was correct
            question = ("Was predicted emotion " + self.predicted[0] + " correct?")
            if mbox.askyesno("Emotion Prediction Assessment" , question):
                self.user_profile.addtoProfile(self.audio_metrics, self.predicted[0])
                self.recordingtest = False
            else:
                newtab = Tk()
                newtab.title("Wrong Emotion Correction")
                newtab.geometry("300x158")


                self.correction = StringVar(newtab)
                self.correction.set("Normal")

                emotions = OptionMenu(newtab, self.correction, "Normal", "Excited", "Angry", "Nervous")
                emotions.grid(row = 0, column = 0)

                submitButton = Button(newtab, text = "Submit Emotion" , justify = "center", command = lambda:[self.submit(), newtab.destroy()], bg = "lightgray")
                submitButton.grid(row = 1, column = 0)

                newtab.mainloop()
        else:
            mbox.showerror("Incorrect button press!", "You must be recording to stop. Please start/restart recording.")
        return self
        
    def submit(self):
        self.predicted = self.correction.get()
        self.user_profile.addtoProfile(self.audio_metrics, self.predicted)
        self.recordingtest = False
		
# Modify root window.
root = Tk()
root.title("Audio Control Interface")

# The size of the whole frame.

root.geometry ("300x158") 

# Background for the whole GUI

app = Application(root)

#kick off the event loop
root.mainloop()



