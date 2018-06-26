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
class MU: #Parent class, VMU is contained in here
	def __init__(self, name, vname, mode, row):
		self.name = name
		self.vname = vname
		self.mode = mode
		self.row = row
		self.row_offset = 5 + self.row#This is kinda archaic long term...
		self.modes = ["V", "DVOL"]
		self.functions = ["VAR1", "VAR2", "VARD", "CONS"]

	def update(self):
		self.unit_label = Label(text=self.name,width=15)
		self.unit_label.grid(row=self.row_offset,column=0) #It's importnat .grid is done in separate lines to conserve types
		self.vname_label = Entry(text=self.vname, width=15, justify='center')
		self.vname_label.delete(0,END)
		self.vname_label.insert(0,self.vname) #I have no idea why this needs to be like this, but it does
		self.vname_label.grid(row=self.row_offset,column=1)
		

		self.mode_thing = StringVar(root)
		self.mode_thing.set(self.mode)

		self.mode_label = OptionMenu(root, self.mode_thing, *self.modes)
		self.mode_label.grid(row=self.row_offset,column=3)


		
	def getParams(self):
		self.vname = getData("PAGE:CHAN:" + self.name + ":VNAME?")[:-1] #Because GPIB returns an extra space that then screws up commands
		self.mode = getData("PAGE:CHAN:" + self.name + ":MODE?")[:-1]

	def writeParams(self):
		my_instrument.write("PAGE:CHAN:" + self.name + ":VNAME " + "\"" + self.vname + "\"")
		my_instrument.write("PAGE:CHAN:" + self.name + ":MODE " + self.mode)
		#print("Wrote: "+ "PAGE:CHAN:" + self.name + ":MODE " + self.mode) 

class SMU(MU):
	def __init__(self, name, vname, iname, mode, function, standby, row):
		self.name = name
		self.vname = vname
		self.iname = iname
		self.mode = mode
		self.function = function
		self.standby = standby
		self.row = row
		self.row_offset = 5 + self.row#This is kinda archaic long term...
		self.modes = ["V", "I", "VPU", "IPU", "COMM"]
		self.functions = ["VAR1", "VAT2", "VARD", "CONS"]

	def updateExtended(self):
		self.iname_label = Entry(text=self.iname, width=15, justify='center')
		self.iname_label.delete(0,END)
		self.iname_label.insert(0,self.iname) #I have no idea why this needs to be like this, but it does
		self.iname_label.grid(row=self.row_offset,column=2)

		self.function_thing = StringVar(root)
		self.function_thing.set(self.function)

		self.function_label = OptionMenu(root, self.function_thing, *self.functions)
		self.function_label.grid(row=self.row_offset,column=4)

		#There's something wrong here but I'm not sure why. Iname blanks on refresh but writes work fine
	def getExtendedParams(self):
		self.iname = getData("PAGE:CHAN:" + self.name + ":INAME?")[:-1] #Because GPIB returns a space we don't want
		self.function = getData("PAGE:CHAN:" + self.name + ":FUNC?")[:-1]
		#self.standby = getData("PAGE:CHAN:" + self.name + ":STBY?") #??? This might not work 

	def writeExtendedParams(self):
		my_instrument.write("PAGE:CHAN:" + self.name + ":INAME " + "\"" + self.iname + "\"") 
		my_instrument.write("PAGE:CHAN:" + self.name + ":FUNC " + "\"" + self.function + "\"") 

class VSU(MU):
	def __init__(self, name, vname, mode, function, standby, row):
		self.name = name
		self.vname = vname
		self.mode = mode
		self.function = function
		self.standby = standby
		self.row = row
		self.row_offset = 5 + row#This is kinda archaic long term...
		self.modes = ["V", "DIS"]
		self.functions = ["VAR1", "VAR2", "VARD", "CONS"]

	def updateExtended(self):
		self.function_thing = StringVar(root)
		self.function_thing.set(self.function)

		self.function_label = OptionMenu(root, self.function_thing, *self.functions)
		self.function_label.grid(row=self.row_offset,column=4)

	def getExtendedParams(self):
		self.function = getData("PAGE:CHAN:" + self.name + ":FUNC?")[:-1]
		#self.standby = getData("PAGE:CHAN:" + self.name + ":STBY?")
	
	def writeExtendedParams(self):
		my_instrument.write("PAGE:CHAN:" + self.name + ":FUNC " + "\"" + self.function + "\"") 


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
		queryBox = Label(text = reply, bg="white", relief=SUNKEN,width=75).grid(row=16,column=1, columnspan = 5)
		queryBox.insert(reply)
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
	getData(":PAGE:CHAN:COMM '" +  program_description.get() + "'")

def updateLabels():
	SMU1.getParams()
	SMU1.getExtendedParams()
	SMU1.update()
	SMU1.updateExtended()

	SMU2.getParams()
	SMU2.getExtendedParams()
	SMU2.update()
	SMU2.updateExtended()

	SMU3.getParams()
	SMU3.getExtendedParams()
	SMU3.update()
	SMU3.updateExtended()

	SMU4.getParams()
	SMU4.getExtendedParams()
	SMU4.update()
	SMU4.updateExtended()

	VSU1.getParams()
	VSU1.getExtendedParams()
	VSU1.update()
	VSU1.updateExtended()

	VSU2.getParams()
	VSU2.getExtendedParams()
	VSU2.update()
	VSU2.updateExtended()
	
	VMU1.getParams()
	VMU1.update()

	VMU2.getParams()
	VMU2.update()

def writeLabels():
	SMU1.vname = SMU1.vname_label.get()
	SMU2.vname = SMU2.vname_label.get()
	SMU3.vname = SMU3.vname_label.get()
	SMU4.vname = SMU4.vname_label.get()

	SMU1.iname = SMU1.iname_label.get()
	SMU2.iname = SMU2.iname_label.get()
	SMU3.iname = SMU3.iname_label.get()
	SMU4.iname= SMU4.iname_label.get()

	VSU1.vname = VSU1.vname_label.get()
	VSU2.vname = VSU2.vname_label.get()
	VMU1.vname = VMU1.vname_label.get()
	VMU2.vname = VMU2.vname_label.get()

	SMU1.mode = SMU1.mode_thing.get()
	SMU2.mode = SMU2.mode_thing.get()
	SMU3.mode = SMU3.mode_thing.get()
	SMU4.mode = SMU4.mode_thing.get()

	VSU1.mode = VSU1.mode_thing.get()
	VSU2.mode = VSU2.mode_thing.get()

	VMU1.mode = VMU1.mode_thing.get()
	VMU2.mode = VMU2.mode_thing.get()

	SMU1.function = SMU1.function_thing.get()
	SMU2.function = SMU2.function_thing.get()
	SMU3.function = SMU3.function_thing.get()
	SMU4.function = SMU4.function_thing.get()

	VSU1.function = VSU1.function_thing.get()
	VSU2.function = VSU2.function_thing.get()

	SMU1.writeParams()
	SMU1.writeExtendedParams()
	SMU2.writeParams()
	SMU2.writeExtendedParams()
	SMU3.writeParams()
	SMU3.writeExtendedParams()
	SMU4.writeParams()
	SMU4.writeExtendedParams()

	VSU1.writeParams()
	VSU1.writeExtendedParams()
	VSU2.writeParams()
	VSU2.writeExtendedParams()

	VMU1.writeParams()
	VMU1.writeParams()

#Function to refresh bulk channel data... goes through all of them through for loops, also writes them to UI
#Delays are introduced when the instrument dosn't reply... so there's some room for improvement here

#Now to create the actaul GUI window
root = Tk()
root.title("Device: " + my_instrument.query('*IDN?') + " - on Interface: " + devices[device_number]) #Window Title

channel_definition = "V-I curve" #This should be able to be changed, but instrument doesn't reply to commands I'm trying to apply.

SMU1 = SMU("SMU1", "", "I1", "", "", "", 1)
SMU1.getParams()
SMU1.getExtendedParams()
SMU1.update()
SMU1.updateExtended()

SMU2 = SMU("SMU2", "", "I2", "", "", "", 2)
SMU2.getParams()
SMU2.getExtendedParams()
SMU2.update()
SMU2.updateExtended()

SMU3 = SMU("SMU3", "", "I3", "", "", "", 3)
SMU3.getParams()
SMU3.getExtendedParams()
SMU3.update()
SMU3.updateExtended()

SMU4 = SMU("SMU4", "", "I4", "", "", "", 4)
SMU4.getParams()
SMU4.getExtendedParams()
SMU4.update()
SMU4.updateExtended()

VSU1 = VSU("VSU1", "", "", "", "", 5)
VSU1.getParams()
VSU1.getExtendedParams()
VSU1.update()
VSU1.updateExtended()

VSU2 = VSU("VSU2", "", "", "", "", 6)
VSU2.getParams()
VSU2.getExtendedParams()
VSU2.update()
VSU2.updateExtended()

VMU1 = MU("VMU1", "", "", 7)
VMU1.getParams()
VMU1.update()

VMU2 = MU("VMU2", "", "", 8)
VMU2.getParams()
VMU2.update()

#Now to draw the actual GUI
Label(text="CHANNELS: CHANNEL DEFINITION",width=30).grid(row=0,column=0)
program_description = Entry(bg="white", relief=SUNKEN,width=50)
program_description.insert(0, ' '.join(getData(":PAGE:CHAN:COMM?").split()).replace("\"", "").replace("}"," ").replace("\\", "")) #This is the type of line that requires documentation. Not gonna lie, It's a bunch of BS that shouldn't work but does. Thanks Python <3
program_description.grid(row=0,column=1,columnspan = 3)
writebutton = Button(root, text='Write', width=15, command=UpdateCOMM).grid(row=0, column=4)
refreshbutton =  Button(root, text='Refresh', width=15, command=updateLabels).grid(row=0, column=5)
writeAllButton = Button(root, text='Write ALL', width=20, command=writeLabels).grid(row=0, column=6, columnspan=2, rowspan =2)

choices = ("SWEEP", "TBD") #Can't seem to get it out of Sweep mode with the current command set
var = StringVar(root) #These two lines are a little hacky right now, should look into simplifying.
v_name_var = StringVar(root)
var.set(getData(":PAGE:CHAN:MODE?").split()) #Taking advantage of split() with empty parameters to remove white spaces
measurement_mode = OptionMenu(root, var, *choices)
measurement_mode.grid(column=1, row=2, sticky="ew") #I forget what the Stic

#The following are just more formatting

Label(text="    *MEASUREMENT MODE",width=30).grid(row=2,column=0)
Label(text=" *CHANNELS",width=15).grid(row=3,column=0)
Label(text="UNIT", relief=RIDGE,width=30).grid(row=4,column=0)
Label(text="VNAME", relief=RIDGE,width=15).grid(row=4,column=1)
Label(text="INAME", relief=RIDGE,width=15).grid(row=4,column=2)
Label(text="MODE", relief=RIDGE,width=15).grid(row=4,column=3)
Label(text="FUNCTION", relief=RIDGE,width=15).grid(row=4,column=4)
Label(text="STANDBY", relief=RIDGE,width=15).grid(row=4,column=5)

Label(text="SERIES\nRESISTANCE", relief=RIDGE,width=15).grid(row=4,column=6)
Label(text="0 ohm",width=15).grid(row=5,column=6)
Label(text="0 ohm",width=15).grid(row=6,column=6)
Label(text="-- --",width=15).grid(row=11,column=6)
Label(text="-- --",width=15).grid(row=12,column=6)
#The following govern manual GPIB command insertion

Label(text="Force Input:", relief=RIDGE,width=30).grid(row=15,column=0)
to_write = Entry(bg="white", relief=SUNKEN,width=75)
to_write.grid(row=15,column=1, columnspan = 5)
print(to_write.get())
force_write_button = Button(root, text='GPIB Write', width=30, height=2, command=WriteQuery).grid(row=15, column=6, rowspan=2)


Label(text="Instrument Response: ", relief=RIDGE,width=30, height = 3).grid(row=16,column=0, rowspan= 3) #Box to display instrument response

mainloop() #Part of the TK object