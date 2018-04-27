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

while active:
	print("What would you like to do: \n")
	print("1 - Start New Measurement")
	print("2 - Change Device Settings")
	print("3 - Get Data")
	print("4 - Force GPIB/HPIB Query")
	print("Exit")

	whatDo = input(consoleSeq)
	if whatDo == "1":
		pass
	elif whatDo == "2":
		pass

	elif whatDo == "3":
		pass
	elif whatDo == "4":
		print("\nEnter GPIB Queries, or type \"exit\"...\n")
		while(subActive == True):
			user_input = input(consoleSeq).lower()
			if(user_input != "exit"):
				subActive = True
				print(my_instrument.query(user_input))
			else:
				subActive = False
		pass
	elif whatDo.lower() == "exit":
		active = False;
		print("\nProgram Will Now Exit...\n")
	else:
		print("\n INVALID COMMAND, TRY AGAIN\n")
		pass