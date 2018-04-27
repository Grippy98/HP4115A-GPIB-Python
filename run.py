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

def getChan(): #Displays Channel Data
	my_instrument.write(":PAGE:CHAN")
	print(my_instrument.query("HCOPy:DATA?"))

while active:
	print("What would you like to do: \n")
	print("1 - Setup Measurement")
	print("2 - Change Device Settings")
	print("3 - Get Data")
	print("4 - Force GPIB/HPIB Query")
	print("Exit")

	whatDo = input(consoleSeq)
	if whatDo == "1":
		subActive = True
		print("\n Current Setup: \n")
		getChan();
		while subActive:
			print("You Can: (Sample Command: 1:SMU1:IPULSE)\n")
			print("1 - Set Measurement Mode  (V/I/VPUL(se)/IPUL(se)/COMM(on)/DIS(able))")
			whatDoSub = input(consoleSeq)
			if whatDoSub[0] == "1":
				my_instrument.query("PAGE:CHAN:" + whatDoSub.split(":")[1] + whatDoSub.split(":")[2])
				pass
			elif whatDoSub == "exit":
				subActive = False
			else:
				print("\nWrong Input, Try Again\n")
				pass
		pass
	elif whatDo == "2":
		pass

	elif whatDo == "3":
		pass
	elif whatDo == "4":
		print("\nEnter GPIB Queries, or type \"exit\"...\n")
		while(subActive == True):
			user_input = input(consoleSeq)
			if(user_input.lower() != "exit"):
				subActive = True
				my_instrument.write(user_input)
				try:
					print(my_instrument.read())
				except:
					pass
			else:
				subActive = False
		pass
	elif whatDo.lower() == "exit":
		active = False;
		print("\nProgram Will Now Exit...\n")
	else:
		print("\n INVALID COMMAND, TRY AGAIN\n")
		pass