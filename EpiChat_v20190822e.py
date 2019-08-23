'''

Created by Wes McNeely, August 22, 2019

I built this program so that staff could communicate in a secure chat room.
The program does not rely on internet protocols, it simply writes to and reads from a text file in a secure network folder.
All communications are retained for future review. 
Hopefully this will prevent inadvertently sharing sensitive information through email in day-to-day communications between staff.    

They will probably never use it.

'''


from tkinter import *
import datetime as DT
import win32api
import win32net

##### VARIABLES FOR USER INFO AND LOGFILE DETAILS 

userInfo = win32net.NetUserGetInfo(win32net.NetGetAnyDCName(), win32api.GetUserName(), 2)   # retrieves windows login full name
userName = userInfo["full_name"]
userChatID = '(' + userName[:-6] + ')'	# subtracts some organization info from the end of the user name, can be adjusted

chatLogLocation = 'c:\\EpiChat\\chatLogs\\'	# change file location if desired. If empty it puts the log file in the source directory 
chatFileName = chatLogLocation+'chatFile_v' + DT.datetime.today().strftime('%Y%m%d') + '.log' # starts a new log file every day, does not overwrite prior logs

##### FUNCTIONS FOR ENTERING THE CHATROOM, SENDING A CHAT MESSAGE, REFRESHING THE TEXTAREA AND QUITTING 

def chatEnter():  # creates a log entry when the application is started

	chatEnterMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')	# creates timestamp for log entry
	chatEnterEntry ='[' + chatEnterMessageTimeStamp + '] - ' + userChatID + ' has entered EpiChat'	# creates full message for log entry
	try:
		with open(chatFileName,'r+') as chatFile: #if logfile exists, opens and reads it and writes it in reverse order so the last entry is at the top of the screen 
			chatFileContents = chatFile.read()
			chatFile.seek(0, 0)
			chatFile.write(chatEnterEntry.rstrip('\r\n') + '\n' + chatFileContents)
			chatFile.close()
	except Exception as e: #if logfile does not exist, opens and reads it and writes it in reverse order so the last entry is at the top of the screen 
		with open(chatFileName,'a+') as chatFile:
			chatFileContents = chatFile.read()
			chatFile.seek(0, 0)
			chatFile.write(chatEnterEntry.rstrip('\r\n') + '\n' + chatFileContents) # writes entry into logfile, logging users has entered the room
			chatFile.close()

	with open(chatFileName,'r') as chatFile: 
		chatText = chatFile.read()

		frame2Text.configure(state='normal') #enables text in Text widget to be altered by INSERT command in next line
		frame2Text.insert(INSERT, chatText) #INSERTs contents of logfile into Text widget
		frame2Text.configure(state='disabled') #prevents text in Text widget from being altered by user. Purely for aesthetics
		chatFile.close() 


def chatSend(event=None): #activated by the Send button 'chatButtonSend'

	if chatEntryField.get().strip() == '': #prevents whitespace from being entered into log. Purely for aesthetics
		return

	chatMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')
	chatEntry ='[' + chatMessageTimeStamp + '] - ' + userChatID + ': ' + chatEntryField.get()  #composes log entry from user Entry submission, combining the timestamp, user name and the text the submitted  

	with open(chatFileName,'r+') as chatFile: #see "def chatEnter():"
		chatFileContents = chatFile.read()
		chatFile.seek(0, 0)
		chatFile.write(chatEntry.rstrip('\r\n') + '\n' + chatFileContents) # writes users entry into logfile at top of logfile
		chatFile.close() 

	frame2Text.configure(state='normal')
	frame2Text.delete('1.0', END)  # deletes contents of Text widget which will be repopulated with contents of logfile re-read
	frame2Text.configure(state='disabled')	

	chatEntryField.delete('0', END) # ensures Entry widget is empty after user submits comment 
	chatEntryField.focus() # ensures Entry widget retains cursor focus


	with open(chatFileName,'r') as chatFile2:
		chatText = chatFile2.read()

		frame2Text.configure(state='normal')
		frame2Text.insert(INSERT, chatText) #repopulates Text widget with contents of logfile re-read
		frame2Text.configure(state='disabled')


		chatFile2.close() 


def chatRefresh(): #refreshes Text widget with contents of logfile every few seconds in the event another user submits a comment

	frame2Text.configure(state='normal')
	frame2Text.delete('1.0', END)
	frame2Text.configure(state='disabled')	

	with open(chatFileName,'r') as chatFile:
		chatText = chatFile.read()
		frame2Text.configure(state='normal')
		frame2Text.insert(INSERT, chatText)
		frame2Text.configure(state='disabled')
		chatFile.close()

	chatWindow.after(2000, chatRefresh) #reruns every 2 seconds


def chatQuit(): #creates an entry when users quits the application

	chatQuitMessageTimeStamp=DT.datetime.today().strftime('%m-%d-%Y %H:%M:%S')
	chatQuitEntry ='[' + chatQuitMessageTimeStamp + '] - ' + userChatID + ' has left EpiChat'


	with open(chatFileName,'r+') as chatFile:
		chatFileContents = chatFile.read()
		chatFile.seek(0, 0)
		chatFile.write(chatQuitEntry.rstrip('\r\n') + '\n' + chatFileContents)
		chatFile.close() 
	
	chatWindow.destroy() #closes app
	

##### MAIN CHAT WINDOW

chatWindow = Tk()   
chatWindow.geometry('900x700') 
chatWindow.title('EpiChat v9.8.22.e')
chatWindow.bind('<Return>',chatSend) #binds the 'Return' key to the 'chatSend' function which is activates by the Send button


##### FRAME2  # I had other frames with different numbers which I have deleted but kept the numbering system

frame2 = Frame(chatWindow) 
frame2.pack(side = TOP ) 

frame2Scrollbar = Scrollbar(frame2) 
frame2Scrollbar.pack( side = RIGHT, fill = Y ) 

frame2Text = Text(frame2, wrap=WORD, width = 145, height= 40)
frame2Text.pack(fill="none", expand=TRUE)

frame2Scrollbar.config( command = frame2Text.yview ) 

##### FRAME3

frame3 = Frame(chatWindow)
frame3.pack( side = BOTTOM ) 

chatEntryField = Entry(frame3, width = 117)
chatEntryField.focus() # ensures Entry widget retains cursor focus
chatEntryField.pack(side = LEFT)

chatButtonSend = Button(frame3, text = 'Send', width = 20, bg='lightgreen', command = chatSend) # chatSend function is activated when the Send button or Return key is pressed 
chatButtonSend.pack(side = RIGHT)

chatEnter() # activates chatEnter function that creates initial entry, logging that user has entered the chat room
chatWindow.after(0, chatRefresh) # activates chatRefresh function that continuously refreshes the Text widget with the contents of the logfile
chatWindow.protocol("WM_DELETE_WINDOW", chatQuit) # activates chatQuit function that logs when user has left the chat room

chatWindow.mainloop() # Whew!
