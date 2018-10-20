#Gui interface for Audio Emotional detection program CSC-450 Michael Knapp

from tkinter import *
import tkinter as tk
#import pyaudio
#import Recording
#import emotionProcessor
from tkinter import Menu
from tkinter import messagebox as mbox

CHUNK = 1024
#FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
wave_output_filename = "test.wav"

#app = tk.Tk()
# create the window for the GUI
# this class sets up the frame which is the entire window needed to fit the GUI buttons and lable's inside.

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid(column = 2, row = 5)
        self.create_widgets()
        self.recorder=Recording.Recording(wave_output_filename, CHANNELS, RATE, CHUNK)
        self.processor=emotionProcessor.EmotionProcessor(wave_output_filename)
    
   # class widgets.. this is where the code for each off six buttons two lable's and two text boxes are held.
   # .pack()= makes the button fit to the entire collumn not just the size of the text inside the button.
   # grid= where is that button on lable located in the frame.
   # each button has a command atribute that connects the button with a function that controls what the button does.
   
    def create_widgets(self):
        self.startButton = Button(self, text = " Start: recording          " , justify = "center", command = self.recordAudio, bg = "lightgray",fg ="green")
        self.startButton.grid(row = 0, column = 0)

        self.stopButton = Button(self, text = " Stop: recording          " , justify = "center", command = self.endAudio, bg ="lightgray",fg = "red")
        self.stopButton.grid(row = 1, column = 0)
        
        self.playButton = Button(self, text = "Play Recorded Audio", justify = "center", command = self.playAudio, bg = "lightgray",fg = "green")
        self.playButton.grid(row = 2 , column = 0)

        self.saveButton = Button (self, text = "Save Audio                 ", justify = "center", command = self.saveAudio, bg = "lightgray")
        self.saveButton.grid(row = 3, column = 0)

        self.deleteButton = Button (self,text = "Delete Audio              ", justify = "center", command = self.deleteAudio, bg = "lightgray",fg = 'black')
        self.deleteButton.grid(row = 4, column = 0)

        self.processButton = Button(self,text = "Process Emotion       ", justify = "center", command = self.processAudio,bg = "lightgray", fg = "orange")
        self.processButton.grid(row = 5, column = 0)

        self.txt = Entry(self, width = 20)
        self.txt.grid(column = 2, row = 0)

        self.label = Label(self, text = "User Name:", font = 13)
        self.label.grid(column = 1, row = 0)
        
        #not sure who put this in here but I removed them because we shouldn't need more than user at a time. 
        #this goes for both lable and entry box. 
        
        #self.label = Label(self, text = "User Name:")
        #self.label.grid(column = 2, row = 0)

        #self.text = Entry(self, width = 20)
        #self.text.grid(column = 3, row = 0)
        
        self.label = Label (self, text = "Emotion:",font = 13)
        self.label.grid(column = 1, row = 1)

        self.text = Entry(self, width = 20)
        self.text.grid(column = 2, row = 1)

        chk_state = BooleanVar()
        chk_state.set(True) #set the state of the check button
        chk = Checkbutton(self, text='Check To Train Emotion', var=chk_state)
        chk.grid(column = 1, row = 2)

        self.label = Label (self, text = "List of Processed Emotions")
        self.label.grid(column = 1, row = 3)

        """self.text2 = Text(self, width = 10)
        self.text2.grid(column =2, row = 3)"""
        
        """self.scrollbar = Scrollbar = Scrollbar(self.root)
        self.scrollbar.pack(x = 100, y = 200)
        self.outputArea = Text(self.root, height=5, width = 100)
        self.outputArea.place(x=0,y=120)"""
        
        
        
# attaching the command of each button to the correct function that needs to fire when a button is pressed.
#can't test any further until the fuctions self.recorder.startAudio() errors because these are not valid functions yet.
# added pop window functions for recordAudio fuction adn the endAudio fuction. code that was pasted is at he bottom commented out just in case there are problems testing this that.../n
#            ....way we can go back and figure what is incorrect.  please leave this for now.
    def recordAudio(self):
        self.recorder.startAudio()
        app = tk.Tk()
        menuBar = Menu(app)
        app.config(menu=menuBar)
        mbox.askyesnocancel('Yes or No or Cancel action Box', 'Choose the Action')
        msgMenu = Menu(menuBar, tearoff=0)
        msgMenu.add_command(label= "Close", command =_msgBox)
        menuBar.add_cascade(label = "File", menu=msgMenu)
        app.mainloop()
        return self
    def endAudio(self):
        self.recorder.stopAudio()
        app = tk.Tk()
        menuBar = Menu(app)
        app.config(menu=menuBar)
        mbox.askyesnocancel('Yes or No or Cancel action Box', 'Choose the Action')
        msgMenu = Menu(menuBar, tearoff=0)
        msgMenu.add_command(label= "Close", command =_msgBox)
        menuBar.add_cascade(label = "File", menu=msgMenu)
        app.mainloop()
        return self
    def processAudio(self):
        self.processor.pitchProc()
        return self
    def playAudio(self):
        return self
    def saveAudio(self):
        return self
    def deleteAudio(self):
        return self
# all of this is part of the popwindow code added to endAudio function and the recordAudio buttons        
"""menuBar = Menu(app)
app.config(menu=menuBar)

#display a Yes or No or Cancel Box
def _msgBox():
    mbox.askyesnocancel('Yes or No or Cancel action Box', 'Choose the Action')
#create the message menu
msgMenu = Menu(menuBar, tearoff=0)
msgMenu.add_command(label= "Close", command =_msgBox)
menuBar.add_cascade(label = "File", menu=msgMenu)
app.mainloop()"""




#modify root window
root = Tk()
root.title("Audio Control GUI")
root.geometry ("400x158") # the size of the whole frame
app = Application(root)

#kick off the event loop
root.mainloop()

