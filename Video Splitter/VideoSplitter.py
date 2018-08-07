####IMPORTS####
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import cv2
import numpy as np
from pathlib import Path
import os
import random
import time

####CONSTANTS####
#widget sizing
LabelW = 10
EntryW = 50
ButtonW = 10
ProgressL = 300
standardBD = 5
#current video segment number
videoNum = 0    #Number of current video file added
lineNum = 0     #Current line in file
totalLines = 0  #Number of all the lines in file
segSeconds = 10 #Segments to cut videos into X seconds long
#Options for extension menu
OPTIONS = ["Choose ...","AVI","MP4"]
#Enumerated options in extension menu
NONE = 0
AVI = 1
MP4 = 2
#Array of errors
errors = []
#formating stuff
sths = 0 #start time start of hour parameter
sthe = 2 #start time end of hour parameter
stms = 3 #start time start of minute parameter
stme = 5 #start time end of minute parameter
stss = 6 #start time start of second parameter
stse = 8 #start time end of second parameter

eths = 9  #end time start of hour parameter
ethe = 11 #end time end of hour parameter
etms = 12 #end time start of minute parameter
etme = 14 #end time end of minute parameter
etss = 15 #end time start of second parameter
etse = 17 #end time end of second parameter

extensionL = 4 # minimum extension lenght i.e '.MP4' or '.AVI' or '.TXT' 

#Timing 
hourMax = 100
minMax = 60
secMax = 60



####METHODS####
#Get video file from file selector 
def getVideoFile():
	videoEntry.delete(0,END)
	videoEntry.insert(0,askopenfilename())
	
#Get text file from file selector 
def getTextFile():
	fileEntry.delete(0,END)
	fileEntry.insert(0,askopenfilename())

#Get frame number 
def getFrame(hour,minute,sec,fps):
	return ((((int(hour)*minMax)+int(minute))*secMax+int(sec))*fps)

#Checks if format is valid
def isValidFormat(line):

	#global sths,sthe,stms,stme,stss,stse,eths,ethe,etms,etme,etss,etse, hourMax,minMax,secMax

	#format as follows "00:00:00 00:00:00 Action_Name\n" for each line
	#                   0123456789012345678
                  
	if(len(line)<(etse+1)):
		return False
	if not (line[sths:sthe].isdigit() and int(line[sths:sthe])>=0 and int(line[sths:sthe])<hourMax):
		return False
	if not (line[stms:stme].isdigit() and int(line[stms:stme])>=0 and int(line[stms:stme])<minMax):
		return False
	if not (line[stss:stse].isdigit() and int(line[stss:stse])>=0 and int(line[stss:stse])<secMax):
		return False
	if not (line[eths:ethe].isdigit() and int(line[eths:ethe])>=0 and int(line[sths:sthe])<hourMax):
		return False
	if not (line[etms:etme].isdigit() and int(line[etms:etme])>=0 and int(line[stms:stme])<minMax):
		return False
	if not (line[etss:etse].isdigit() and int(line[etss:etse])>=0 and int(line[stss:stse])<secMax):
		return False
	return True

#Presents Error screen
def errorScreen():
	errorS = tk.Toplevel()
	errorS.title("Errors")
	errorString = "Errors:\n"
	
	for e in errors:
		errorString =errorString + str(e)+"\n"

	errorL = tk.Label(errorS, text=errorString, justify=LEFT, width = EntryW).grid(row=0,column=0)
	errorS.pack_slaves()
	errorS.update()

#checks if line is correct
def checkLine(line,fps):
	#checks line format
	if not isValidFormat(line):
		return False

	#parse line
	startHour = line[sths:sthe]
	startMin = line[stms:stme]
	startSec = line[stss:stse]
	endHour = line[eths:ethe]
	endMin = line[etms:etme]
	endSec = line[etss:etse]
	action = line[etse+1:len(line)]

	#remove end line char if needed
	if(action[len(action)-1:len(action)] == '\n'):
		action = action[0:len(action)-1]

	#get start and end frames
	start = getFrame(startHour,startMin,startSec,fps)
	end = getFrame(endHour,endMin,endSec,fps)

	#if the start frame is after or equal to end frame
	if(start>=end):
		return False
	#if no action is given
	if(len(action)<1):
		return False

	return True

#Checks file for validation
def check():
	
	#reset global varibles
	global totalLines

	totalLines = 0

	#checks for all info to be entered
	if(not videoEntry.get()) or (not fileEntry.get()) or (not fpsEntry.get()) or (extVar.get() == OPTIONS[NONE]):
		msg = messagebox.showinfo( "Error", "Missing Field")
		return False

	#Checks for a valid FPS
	if not (fpsEntry.get().isdigit() and int(fpsEntry.get())>=1):
		msg = messagebox.showinfo( "Error", "Invalid Frames Per Second")
		return False

	#get info from inputed that needs to be checked
	video = videoEntry.get()
	filename = fileEntry.get()
	fps = int(fpsEntry.get())
	

	#Checks for existance of video file
	if not os.path.exists(video):
		msg = messagebox.showinfo( "Error", "Non-existant Video Path")
		return False

	#Checks for existance of annotation file
	if not (os.path.exists(filename)):
		msg = messagebox.showinfo( "Error", "Non-existant Textfile Path")
		return False

	#checks for correct file extensions
	if not (len(filename) >= extensionL and filename[len(filename)-extensionL:len(filename)].lower() == '.txt'):
		msg = messagebox.showinfo( "Error", "Invalid Textfile (must be .txt)")
		return False


	if not (len(video) >= extensionL and (video[len(video)-extensionL:len(video)].lower() == '.mp4' or filename[len(video)-extensionL:len(video)].lower() == '.avi')):
		msg = messagebox.showinfo( "Error", "Invalid Video File (must be .avi or .mp4)")
		return False


	#get text file and reads 
	file = open(fileEntry.get(), 'r') 
	line = file.readline()

	#count video segments and checks correctness of each line
	while line:
		totalLines = totalLines+1
		if not checkLine(line,fps):
			file.close()
			msg = messagebox.showinfo( "Error", "Line "+str(totalLines)+" has an error")
			return False
		line = file.readline()
	file.close()

	#if all is well
	return True
	

#Processes video snippet
def processLine(start,end,fps,action,video):

	# outputVideoFile
	global videoNum
	global lineNum

	#if end of action is before start of action
	if(start>=end) or (fps <= 0) or not action:
		errors.append("Line "+str(LineNum+1)+": End time is before start time")
		return False
	
	#If a "VideoSets" dir doesnt exist create one
	if not os.path.exists(str(Path.home())+'/Video Sets/'+action):
		os.makedirs(str(Path.home())+'/Video Sets/'+action)

	# Create a VideoCapture object
	cap = cv2.VideoCapture(video)
 
	# Check if camera opened successfully
	if (cap.isOpened() == False): 
		#msg = messagebox.showinfo( "Error","Unable to read video")
		errors.append("Line "+str(lineNum+1)+": Video could not be read")
		return False
 

	# get resolution
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))
 

	#choose correct extension for videoWriter
	if(extVar.get() == OPTIONS[AVI]):
		out = cv2.VideoWriter(str(Path.home())+'/Video Sets/'+str(action)+'/'+str(getVideoName())+'__'+str(lineNum)+'_'+str(videoNum)+'.'+extVar.get(),cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width,frame_height))
	
	elif(extVar.get() == OPTIONS[MP4]):
		out = cv2.VideoWriter(str(Path.home())+'/Video Sets/'+str(action)+'/'+str(getVideoName())+'__'+str(lineNum)+'_'+str(videoNum)+'.'+extVar.get(),cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_width,frame_height))
			
        
	#get to correct frame
	ret = True
	counter = 0
	intoSeg = 0

	while (ret and counter<start):
		ret = cap.grab()
		counter = counter+1

	#get first frame

	ret, frame = cap.read()

	while ret:

		if(counter>=start and counter <=end):
			if(intoSeg/fps > segSeconds):
				videoNum = videoNum+1
				intoSeg = 0
				out.release()

				#choose correct extension for videoWriter
				if(extVar.get() == OPTIONS[AVI]):
					out = cv2.VideoWriter(str(Path.home())+'/Video Sets/'+str(action)+'/'+str(getVideoName())+'__'+str(lineNum)+'_'+str(videoNum)+'.'+extVar.get(),cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width,frame_height))
	
				elif(extVar.get() == OPTIONS[MP4]):
					out = cv2.VideoWriter(str(Path.home())+'/Video Sets/'+str(action)+'/'+str(getVideoName())+'__'+str(lineNum)+'_'+str(videoNum)+'.'+extVar.get(),cv2.VideoWriter_fourcc(*'MP4V'), fps, (frame_width,frame_height))
	
			out.write(frame)
		if counter >= end:
			break

		ret, frame = cap.read()
		counter = counter+1
		intoSeg = intoSeg + 1

	videoNum = videoNum+1
	# When everything done, release the video capture and video write objects
	cap.release()
	out.release()
 
	# Closes all the frames
	cv2.destroyAllWindows()


	#If start frame was after end of video
	if(start >= counter):
		errors.append("Line "+str(lineNum+1)+": Start time is after video end")
		return False
	if(end > counter):
		errors.append("Line "+str(lineNum+1)+": End time is after video end")
		return False

	return True




def processVideo():
	#start_time = time.time()



	global videoNum
	global lineNum
	global errors
	global totalLines

	#reset all varibles
	videoNum = 0
	lineNum = 0
	errors = []
	totalLines = 0

	#checks for issues also gets total lines in file i.e totalLines
	if not check():
		return


	video = videoEntry.get()
	filename = fileEntry.get()
	fps = int(fpsEntry.get())
	
	

	#Opens text file
	file = open(filename, 'r') 
	line = file.readline()
	
	#Progress setup
	popup = tk.Toplevel()
	popup.title("Progress")
	#progress Bar
	progress = 0
	progress_var = tk.DoubleVar()
	progress_bar = ttk.Progressbar(popup, variable=progress_var,length = 500, maximum=totalLines)
	progress_bar.grid(row=1, column=0)
	#Progess Label
	progressL = tk.Label(popup, text=str(lineNum)+"/"+str(totalLines), height = 3).grid(row=1,column=0)
	popup.pack_slaves()
	popup.update()

	#process video snippet
	while line:
		#parse line
		startHour = line[sths:sthe]
		startMin = line[stms:stme]
		startSec = line[stss:stse]
		endHour = line[eths:ethe]
		endMin = line[etms:etme]
		endSec = line[etss:etse]
		action = line[etse+1:len(line)]
		
		#remove end line char if needed
		if(action[len(action)-1:len(action)] == '\n'):
			action = action[0:len(action)-1]

		#get start and end frames
		start = getFrame(startHour,startMin,startSec,fps)
		end = getFrame(endHour,endMin,endSec,fps)

		#Processes line
		processLine(start,end,fps,action,video)
		lineNum = lineNum+1
	
		#get next line
		line = file.readline()

		#update progress info
		progress_var.set(lineNum)
		progressL = tk.Label(popup, text=str(lineNum)+"/"+str(totalLines)).grid(row=1,column=0)
		popup.update()
	
	#close file
	file.close()
	
	#print(time.time()-start_time)



	msg = messagebox.showinfo( "Message", "Done!")
	popup.destroy()
	
	if(len(errors)>0):
		errorScreen()

	#screen.quit()'''

	



#Gets name of current video
def getVideoName():
        string = videoEntry.get()
        return string[string.rfind('/')+1:string.rfind('.')]
        

#GUI info

#Set up screen
screen = Tk()
screen.title("Processing Video")

#Main Panel
mainW = PanedWindow(screen, orient = VERTICAL)
mainW.pack(fill = BOTH, expand = 1)

title = Label(mainW, text = "Action Video Processing",font = 'bold')
submit = Button(mainW,text = "Submit", width = ButtonW, font = 'bold', command = processVideo)

#video browse Panel
videoW = PanedWindow(mainW, orient = HORIZONTAL)

videoName = Label(videoW, text = "Video:",width = LabelW)
videoEntry = Entry(videoW, bd = standardBD, width = EntryW)
videoButton = Button(videoW,text = "Browse", width = ButtonW, command = getVideoFile)

videoW.add(videoName)
videoW.add(videoEntry)
videoW.add(videoButton)

#file browse Panel
fileW = PanedWindow(mainW, orient = HORIZONTAL)

fileName = Label(fileW, text = "Text File:",width = LabelW)
fileEntry = Entry(fileW, bd = standardBD, width = EntryW)
fileButton = Button(fileW,text = "Browse", width = ButtonW, command = getTextFile)

fileW.add(fileName)
fileW.add(fileEntry)
fileW.add(fileButton)

#FPS Panel
fpsW = PanedWindow(mainW, orient = HORIZONTAL)

fpsName = Label(fpsW, text = "FPS:",width = LabelW)
fpsEntry = Entry(fpsW, bd = standardBD, width = ButtonW)
fpsName2 = Label(fpsW, text = " ",width = LabelW)
extName = Label(fpsW, text = "Extension:",width = LabelW)
#extEntry = Entry(fpsW, bd = standardBD, width = ButtonW)
extVar = StringVar(fpsW)
extVar.set(OPTIONS[NONE]) # default value
extMenu = OptionMenu(fpsW, extVar, *OPTIONS)
extMenu.pack()
extName2 = Label(fpsW, text = " ",width = LabelW)

fpsW.add(fpsName)
fpsW.add(fpsEntry)
fpsW.add(fpsName2)
fpsW.add(extName)
fpsW.add(extMenu)
fpsW.add(extName2)

#Progress
'''progressW = PanedWindow(mainW, orient = VERTICAL)

progressName = Label(progressW, text=("0/0"))
progress_var = DoubleVar()
progress = ttk.Progressbar(progressW, orient="horizontal",length=ProgressL, mode="determinate", variable=progress_var,maximum=10)
	
progressW.add(progress)
progressW.add(progressName)'''

#Add all parts
mainW.add(title)
mainW.add(videoW)
mainW.add(fileW)
mainW.add(fpsW)
#mainW.add(progressW)
mainW.add(submit)



screen.mainloop()









	




	

