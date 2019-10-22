'''

EpiChat - A simple, text file based chat room for communication, written in Python 3.7.

I built this program as an alternate to email and other proprietary communication systems. 
It is not secure. 
Chat data is stored in an easily accessible file. 
The program does not rely on internet protocols, it simply writes to and reads from a text file in a network folder.

Requirements:
	libraries tkinter, retrying
	PyInstaller

Installation Instructions:

	Copy EpiChat_v20190823a.py, chat.ico, and install.bat to a network folder.
	Inside EpiChat_v20190823a.py, hardcode "chatLogLocation" to desired network folder location e.g. 'k:\\chatlogs\\'
	Run install.bat
	Give .exe to coworkers

'''

import random
from retrying import retry
from tkinter import *
import datetime as DT
import win32api
import win32net
#from tendo import singleton

#me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running


##### VARIABLES FOR USER INFO AND LOGFILE DETAILS 

userInfo = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)   # retrieves windows login full name
userName = userInfo["full_name"]
userChatID = '(' + userName[:-6] + ')'	# subtracts some organization info from the end of the user name, can be adjusted

chatLogLocation = 'K:\\Wes\\python\\projects\\chat\\chatLogs\\'	# add file location if desired e.g. 'chatLogs\\' or 'c:\\EpiChat\\chatLogs\\', if empty it puts the log file in the source directory 
chatFileName = chatLogLocation+'chatFile_v' + DT.datetime.today().strftime('%Y%m%d') + '.log' # starts a new log file every day, does not overwrite prior logs

##### FUNCTIONS FOR ENTERING THE CHATROOM, SENDING A CHAT MESSAGE, REFRESHING THE TEXTAREA AND QUITTING 

@retry(wait_exponential_multiplier=random.randint(700,1200), wait_exponential_max=5000, stop_max_delay=10000) # a backoff generator to avoid race conditions
def chatEnter():  # creates a log entry when the application is started

	chatEnterMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')	# creates timestamp for log entry
	chatEntry ='[' + chatEnterMessageTimeStamp + '] - ' + userChatID + ' has entered EpiChat @@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'	# creates full message for log entry

	try:
		chatWrite(chatEntry, 'a')
	except Exception as e: 
		chatWrite(chatEntry, 'r+')

	with open(chatFileName,'r') as chatFile: 
		chatText = chatFile.read()

		frame2Text.configure(state='normal') #enables text in Text widget to be altered by INSERT command in next line
		frame2Text.insert(INSERT, chatText) #INSERTs contents of logfile into Text widget
		frame2Text.see('end')
		frame2Text.configure(state='disabled') #prevents text in Text widget from being altered by user. Purely for aesthetics
		chatFile.close() 


@retry(wait_exponential_multiplier=random.randint(700,1200), wait_exponential_max=5000, stop_max_delay=10000)
def chatWrite(chatMessage, writeType): #writes message to logfile using open type 
	with open(chatFileName, writeType) as chatFile: 
		chatFile.write(chatMessage) # writes users entry into logfileg at bottom of logfile
		chatFile.close() 
	
@retry(wait_exponential_multiplier=random.randint(700,1200), wait_exponential_max=5000, stop_max_delay=10000)
def chatSend(event=None): #activated by the Send button 'chatButtonSend'

	if chatEntryField.get().strip() == '': #prevents whitespace from being entered into log. Purely for aesthetics
		return

	chatMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')
	chatEntry ='[' + chatMessageTimeStamp + '] - ' + userChatID + ': ' + chatEntryField.get() + '\n' #composes log entry from user Entry submission, combining the timestamp, user name and the text the submitted  

	chatWrite(chatEntry, 'a')

	frame2Text.configure(state='normal')
	frame2Text.delete('1.0', END)  # deletes contents of Text widget which will be repopulated with contents of logfile re-read
	frame2Text.configure(state='disabled')	

	chatEntryField.delete('0', END) # ensures Entry widget is empty after user submits comment 
	chatEntryField.focus() # ensures Entry widget retains cursor focus


	with open(chatFileName,'r') as chatFile:
		chatText = chatFile.read()

		frame2Text.configure(state='normal')
		frame2Text.insert(INSERT, chatText) #repopulates Text widget with contents of logfile re-read
		frame2Text.see('end')
		frame2Text.configure(state='disabled')


		chatFile.close() 

@retry(wait_exponential_multiplier=random.randint(700,1200), wait_exponential_max=5000, stop_max_delay=10000)
def chatRefresh(): #refreshes Text widget with contents of logfile every few seconds in the event another user submits a comment

	frame2Text.configure(state='normal')
	frame2Text.delete('1.0', END)
	frame2Text.configure(state='disabled')	

	with open(chatFileName,'r') as chatFile:
		chatText = chatFile.read()
		frame2Text.configure(state='normal')
		frame2Text.insert(INSERT, chatText)
		frame2Text.see('end')
		frame2Text.configure(state='disabled')
		chatFile.close()

	chatWindow.after(10000, chatRefresh) #reruns every 3 seconds

@retry(wait_exponential_multiplier=random.randint(700,1200), wait_exponential_max=5000, stop_max_delay=10000)
def chatQuit(): #creates an entry when users quits the application

	chatQuitMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')
	chatEntry ='[' + chatQuitMessageTimeStamp + '] - ' + userChatID + ' has exited EpiChat *************************************************************\n'

	chatWrite(chatEntry, 'a')
	
	chatWindow.destroy() #closes app
	

##### MAIN CHAT WINDOW

chatWindow = Tk()   
chatWindow.geometry('1200x700') 
chatWindow.title('EpiChat v9.8.28.a')
chatWindow.bind('<Return>', chatSend) #binds the 'Return' key to the 'chatSend' function which is activates by the Send button


##### FRAME2  # I had other frames with different numbers which I have deleted but kept the numbering system

frame2 = Frame(chatWindow) 
frame2.pack(side = TOP ) 

frame2Scrollbar = Scrollbar(frame2,bd=3 ) 
frame2Scrollbar.pack( side = RIGHT, fill = Y ) 

frame2Text = Text(frame2, wrap=WORD, width = 131, height= 23, font=("Garamond", 14), spacing1=8, relief=GROOVE,bd=3)
frame2Text.pack(fill="none", expand=TRUE)

frame2Scrollbar.config( command = frame2Text.yview ) 

##### FRAME3

frame3 = Frame(chatWindow)
frame3.pack( side = BOTTOM ) 

chatEntryField = Entry(frame3, width = 85, font=("Helvetica", 14), bd=3)
chatEntryField.focus() # ensures Entry widget retains cursor focus
chatEntryField.pack(side = LEFT)

chatButtonSend = Button(frame3, text = 'Send', width = 20, bg='lightgreen', command = chatSend, bd=3, relief=GROOVE) # chatSend function is activated when the Send button or Return key is pressed 
chatButtonSend.pack(side = RIGHT)

chatEnter() # activates chatEnter function that creates initial entry, logging that user has entered the chat room
chatWindow.after(0, chatRefresh) # activates chatRefresh function that continuously refreshes the Text widget with the contents of the logfile
chatWindow.protocol("WM_DELETE_WINDOW", chatQuit) # activates chatQuit function that logs when user has left the chat room

chatWindow.mainloop() # Whew!