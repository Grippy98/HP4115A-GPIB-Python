#See page 133ish of Programmer's Manual
#See page 157
#Also See: http://sine.ni.com/apps/utf8/niid_web_display.model_page?p_model_id=1135

from tkinter import *
#from tkFileDialog   import askopenfilename

import visa #PyVisa Library for GPIB Communication using National Instruments VISA Backend
rm = visa.ResourceManager()
devices = rm.list_resources()

consoleSeq = "~: " #Just a nice way to represenet input

print("\nPlease enter device number to interface with: \n")

devices = rm.list_resources()

#Quit execution if no devices found
if len(devices) == 0:
	print("No devices found... Exiting...\n")
	quit() #Terminate program
	pass

#Print the list of devices
for x in range(0,len(devices)):
	print(str(x) + " - " + devices[x])	
	pass

device_number = int(input(consoleSeq))
#Open the actual devices
my_instrument = rm.open_resource(devices[device_number])

#Get Instrument Model
print("\nConnected to Instrument: " + my_instrument.query('*IDN?') + "\n")

#The following aren't used yet but i figured making them objects in the future makes sense
class SMU(object):
	name = ""
	vname = ""
	iname = ""
	mode = ""
	func = ""
	stdby = 0

class VSU(object):
	name = ""
	vname = ""
	mode = ""
	func = ""
	stdby = 0

class VMU(object):
	name = ""
	vname = ""
	mode = ""
	stdby = 0

reply = "NONE" #Default reply from the instrument... in case it doesn't actually reply any data


def getChan(): #Displays Channel Data
	my_instrument.write(":PAGE:CHAN")
	print(my_instrument.query("HCOPy:DATA?"))

#Some of these are semi-placeholder functions
def NewFile():
    print ("New File!")
def OpenFile():
    name = askopenfilename()
    print (name)

#About page from top File menu
def About():
    print ("HP4155A Controller... Rev0")

#Write a querry to the instrument
def WriteQuery():
	my_instrument.write(to_write.get())
	print("Wrote: " + to_write.get() + "\n")
	#This needs to be in try-catch form because the instrument doesn't always return data in the expected format
	try:
		global reply #I severely questions this... need to look into when it's easier to debug
		reply = my_instrument.read()
		print(reply)
		receivedBox = Label(text = reply, bg="white", relief=SUNKEN,width=75).grid(row=16,column=1, columnspan = 5)
		receivedBox.insert(reply)
	#Nothing to really error handle, just give up on the command... this will introduce a slight delay
	except:
		pass

#Way of querying instrument data... one of two
def getData(write):
	my_instrument.write(write)
	print("Wrote: " + write + "\n")
	#Try-catch because instrument doesn't always reply in a supported format and will crash NI Backend otherwise
	try:
		reply = my_instrument.read()
		print(reply)
		return reply
	#Nothing to really error handle, just give up on the command... this will introduce a slight delay
	except:
		pass

def UpdateCOMM():
	getData(":PAGE:CHAN:COMM '" +  receivedBox.get() + "'")

#Function to refresh bulk channel data... goes through all of them through for loops, also writes them to UI
#Delays are introduced when the instrument dosn't reply... so there's some room for improvement here
def Refresh_CHAN():
	for x in range(0,4):
		V_NAME[x] = getData("PAGE:CHAN:SMU" + str(x+1) + ":VNAME?") 
		I_NAME[x] = getData("PAGE:CHAN:SMU" + str(x+1) + ":INAME?") 
		MODE[x] = getData("PAGE:CHAN:SMU" + str(x+1) + ":MODE?") 
		FCTN[x] = getData("PAGE:CHAN:SMU" + str(x+1) + ":FUNC?") 
		pass

	for x in range(0,2):
		V_NAME[x+4] = getData("PAGE:CHAN:VSU" + str(x+1) + ":VNAME?") 
		#I_NAME[x+4] = getData("PAGE:CHAN:VSU" + str(x+1) + ":INAME?") 
		MODE[x+4] = getData("PAGE:CHAN:VSU" + str(x+1) + ":MODE?") 
		FCTN[x+4] = getData("PAGE:CHAN:VSU" + str(x+1) + ":FUNC?") 
		pass

	for x in range(0,2):
		V_NAME[x+6] = getData("PAGE:CHAN:VMU" + str(x+1) + ":VNAME?") 
		#I_NAME[x+6] = getData("PAGE:CHAN:VMU" + str(x+1) + ":INAME?") 
		MODE[x+6] = getData("PAGE:CHAN:VMU" + str(x+1) + ":MODE?") 
		FCTN[x+6] = getData("PAGE:CHAN:VMU" + str(x+1) + ":FUNC?") 
		pass

	#Write the found vallues to the menu interface
	#Note c + 5 is used as a offset
	for c in range(0, len(UNIT)):
		#var.set(choices[0])
		row_offset = c + 5
		Label(text=UNIT[c],width=15).grid(row=row_offset,column=0)
		vname = Entry(text=V_NAME[c], width=15, justify='center')
		#V_NAME[c] = vname.get()
		vname.delete(0,END)
		vname.insert(0, V_NAME[c])
		vname.grid(row=row_offset,column=1)
		iname = Entry(text=I_NAME[c],width=15, justify='center')
		#if(iname.get() != I_NAME[c] and iname.get() != ""):
		#	I_NAME[c] = iname.get()
		#	print("New I_NAME at " + str(c) + " " + I_NAME[c])
		iname.delete(0,END)
		iname.insert(0, I_NAME[c])
		iname.grid(row=row_offset,column=2)
		Label(text=MODE[c],width=15).grid(row=row_offset,column=3)
		Label(text=FCTN[c],width=15).grid(row=row_offset,column=4)
		#button = Button(root, text='Stop', width=25, command=root.destroy).grid(row=r, column=6)

#Now to create the actaul GUI window
root = Tk()
root.title("Device: " + my_instrument.query('*IDN?') + " - on Interface: " + devices[device_number]) #Window Title
menu = Menu(root) #Create window menu
root.config(menu=menu) #Config menu? 
filemenu = Menu(menu) #File menu
menu.add_cascade(label="File", menu=filemenu) #The next 4-5 lines are semi-placeholder right now. Need organization TODO
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

gomenu = Menu(menu)
menu.add_cascade(label="Go", menu=gomenu)
filemenu.add_command(label="Channel Menu", command=root.quit)
filemenu.add_command(label="Display Menu", command=root.quit)
filemenu.add_command(label="???", command=root.quit)
filemenu.add_command(label="Exit", command=root.quit)

channel_definition = "V-I curve" #This should be able to be changed, but instrument doesn't reply to commands I'm trying to apply.

#The following 4 work right now, because they're the defaults, and they get updated regardless
#But going forward, I do want to change these to the object type definitions
UNIT = ["SMU1:MP", "SMU2:MP", "SMU3:MP", "SMU4:MP", "VSU1", "VSU2", "VMU1", "VMU2"]
V_NAME = ["V1", "V2", "V3", "V4", "VSU1", "VSU2", "VMU1", "VMU2"]
I_NAME = ["I1", "I2", "I3", "I4", "---- ----", "---- ----", "---- ----", "---- ----"]
MODE = ["COMMON", "I", "V", "V", "V", "V", "V", "V"]
FCTN = ["CONST", "CONST", "CONST", "CONST", "CONST", "CONST", "---- ----", "---- ----"]

#Pull In Initial Data
Refresh_CHAN()

#Now to draw the actual GUI
Label(text="CHANNELS: CHANNEL DEFINITION",width=30).grid(row=0,column=0)
receivedBox = Entry(bg="white", relief=SUNKEN,width=50)
receivedBox.insert(0, ' '.join(getData(":PAGE:CHAN:COMM?").split()).replace("\"", "").replace("}"," ").replace("\\", "")) #This is the type of line that requires documentation. Not gonna lie, It's a bunch of BS that shouldn't work but does. Thanks Python <3
receivedBox.grid(row=0,column=1,columnspan = 3)
writebutton = Button(root, text='Write', width=15, command=UpdateCOMM).grid(row=0, column=4)
refreshbutton =  Button(root, text='Refresh', width=15, command=Refresh_CHAN).grid(row=0, column=5)
writeAllButton = Button(root, text='Write ALL', width=30, command=Refresh_CHAN).grid(row=0, column=6, columnspan=2, rowspan =2)

choices = ("SWEEP", "TBD") #Can't seem to get it out of Sweep mode with the current command set
var = StringVar(root) #These two lines are a little hacky right now, should look into simplifying.
v_name_var = StringVar(root)
var.set(getData(":PAGE:CHAN:MODE?").split()) #Taking advantage of split() with empty parameters to remove white spaces
measurement_mode = OptionMenu(root, var, *choices).grid(column=1, row=2, sticky="ew") #I forget what the Stic

#The following are just more formatting

Label(text="    *MEASUREMENT MODE",width=30).grid(row=2,column=0)
Label(text=" *CHANNELS",width=15).grid(row=3,column=0)
Label(text="UNIT", relief=RIDGE,width=30).grid(row=4,column=0)
Label(text="VNAME", relief=RIDGE,width=15).grid(row=4,column=1)
Label(text="INAME", relief=RIDGE,width=15).grid(row=4,column=2)
Label(text="MODE", relief=RIDGE,width=15).grid(row=4,column=3)
Label(text="FUNCTION", relief=RIDGE,width=15).grid(row=4,column=4)
Label(text="STANDBY", relief=RIDGE,width=15).grid(row=4,column=5)

Label(text="SERIES", relief=RIDGE,width=15).grid(row=4,column=6)
Label(text="Resistance", relief=RIDGE,width=15).grid(row=5,column=6)
Label(text="0 ohm",width=15).grid(row=6,column=6)
Label(text="0 ohm",width=15).grid(row=6,column=6)
#The following govern manual GPIB command insertion

Label(text="Force Input:", relief=RIDGE,width=30).grid(row=15,column=0)
to_write = Entry(bg="white", relief=SUNKEN,width=75)
to_write.grid(row=15,column=1, columnspan = 5)
print(to_write.get())
force_write_button = Button(root, text='GPIB Write', width=30, height=2, command=WriteQuery).grid(row=15, column=6, rowspan=2)


Label(text="Instrument Response: ", relief=RIDGE,width=30).grid(row=16,column=0) #Box to display instrument response

mainloop() #Part of the TK object