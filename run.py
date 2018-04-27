import visa
rm = visa.ResourceManager()

devices = rm.list_resources()

consoleSeq = "~: " #Just a nice way to represenet input

print("Please enter device number to interface with:")

for x in xrange(0,size(rm.list_resources())):
	print(str(x) + ") " + devices[x])	
	pass

number = input(consoleSeq)