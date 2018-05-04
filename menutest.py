from tkinter import *
#from tkFileDialog   import askopenfilename

import visa
rm = visa.ResourceManager()

devices = rm.list_resources()

consoleSeq = "~: " #Just a nice way to represenet input

print("Please enter device number to interface with: \n")

devices = rm.list_resources()

for x in range(0,len(devices)):
	print(str(x) + " - " + devices[x])	
	pass

number = input(consoleSeq)

my_instrument = rm.open_resource(devices[int(number)])

print("\nConnected to Instrument: " + my_instrument.query('*IDN?') + "\n")

active = True
subActive = True

#The following is to make input work in python 2
##try:
##    input = raw_input
##except NameError:
##    pass

reply = "NONE" #Default

def getChan(): #Displays Channel Data
	my_instrument.write(":PAGE:CHAN")
	print(my_instrument.query("HCOPy:DATA?"))

def NewFile():
    print ("New File!")
def OpenFile():
    name = askopenfilename()
    print (name)
def About():
    print ("HP4115A Controller... Rev0")

def WriteQuery(user_input):
	if(user_input.lower() != "exit"):
		subActive = True
		my_instrument.write(user_input)
		try:
			global reply
			reply = my_instrument.read()
			print(reply)
		except:
			pass
    
root = Tk()
root.title("HP4115A: " + my_instrument.query('*IDN?') + " - on Interface: " + devices[int(number)])
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
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

colours = ['red','green','orange','white','yellow','blue']

channel_definition = "V-I curve"

UNIT = ["SMU1:MP", "SMU2:MP", "SMU3:MP", "SMU4:MP", "VSU1", "VSU2", "VMU1", "VMU2"]
V_NAME = ["V1", "V2", "V3", "V4", "VSU1", "VSU2", "VMU1", "VMU2"]
I_NAME = ["I1", "I2", "I3", "I4", "---- ----", "---- ----", "---- ----", "---- ----"]
MODE = ["COMMON", "I", "V", "V", "V", "V", "V", "V"]
FCTN = ["CONST", "CONST", "CONST", "CONST", "CONST", "CONST", "---- ----", "---- ----"]

Label(text="CHANNELS: CHANNEL DEFINITION",width=30).grid(row=0,column=0)
Entry(bg="white", relief=SUNKEN,width=15).grid(row=0,column=1)
writebutton = Button(root, text='Write', width=6, command=root.destroy).grid(row=0, column=2)

choices = ('SWEEP', '???', '???')
var = StringVar(root)
v_name_var = StringVar(root)
var.set(choices[0])
measurement_mode = OptionMenu(root, var, *choices).grid(column=1, row=2, sticky="ew")

Label(text="    *MEASUREMENT MODE",width=30).grid(row=2,column=0)
Label(text=" *CHANNELS",width=15).grid(row=3,column=0)
Label(text="UNIT", relief=RIDGE,width=30).grid(row=4,column=0)
Label(text="VNAME", relief=RIDGE,width=15).grid(row=4,column=1)
Label(text="INAME", relief=RIDGE,width=15).grid(row=4,column=2)
Label(text="MODE", relief=RIDGE,width=15).grid(row=4,column=3)
Label(text="FUNCTION", relief=RIDGE,width=15).grid(row=4,column=4)
Label(text="STANDBY", relief=RIDGE,width=15).grid(row=4,column=5)

r = 5
for c in range(0, len(UNIT)):
	#var.set(choices[0])
	
    Label(text=UNIT[c],width=15).grid(row=r,column=0)
    Label(text=V_NAME[c], width=15, justify='center').grid(row=r,column=1)
    Label(text=I_NAME[c],width=15).grid(row=r,column=2)
    Label(text=MODE[c],width=15).grid(row=r,column=3)
    Label(text=FCTN[c],width=15).grid(row=r,column=4)
    button = Button(root, text='Stop', width=25, command=root.destroy).grid(row=r, column=6)
    r = r + 1

Label(text="Force Input:", relief=RIDGE,width=30).grid(row=15,column=0)
to_write = Entry(bg="white", relief=SUNKEN,width=75).grid(row=15,column=1, columnspan = 5)
force_write_button = Button(root, text='GPIB Write', width=25, command=WriteQuery(to_write)).grid(row=15, column=6)


Label(text="Instrument Response: ", relief=RIDGE,width=30).grid(row=16,column=0)
Label(text = reply, bg="white", relief=SUNKEN,width=75).grid(row=16,column=1, columnspan = 5)

mainloop()