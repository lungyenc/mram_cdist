# main.py
# This program plots the conductance distribution of multiple MRAM cells on a bit-line based on
# Rp (resistance-parallel) mean and variance
# Rap (resistance-anti-parallel) mean and variance
# number of MRAM cells on a bit-line
# note that we assume the random variables of each MRAM have the same distribution but independent

import GenSampling as gs

INSTLIST = '[1] Start a new analysis\n' 
INSTLIST += '[2] Sample and plot with the current settings\n'
INSTLIST += '[3] Sameplew with the current settings\n'
INSTLIST += '[4] Plot the distribition\n'
INSTLIST += '[5] Change R\n'
INSTLIST += '[6] Print the current settings\n'
INSTLIST += '[7] Print instrcutions\n'
INSTLIST += '[8] Exit the program\n'

target = gs.GenSampling(0, 0, 0, 0, 0, 0)

def newAyalsis():
	print('Staring a new analysis...\n')
	changeR()
	changeNCell()
	changeNTest()
	printGs()
	sampleplot()

def changeR():
	while(1):
		inp = input('Please enter new RpMean RapMean RpStd RapStd: (No leading space)  Ex: 6000 12000 350 700\n')
		ints = list(map(int, inp.split(' ')))
		if len(ints) is 4:
			break
		else:
			print('Enter Error')
	target.changeR(ints[0], ints[1], ints[2], ints[3])

def changeNCell():
	while(1):
		inp = input('Please enter new number of MRAM cell: ')
		inp = int(inp)
		if inp > 0:
			break
		else:
			print('Enter Error')
	target.changeNCell(inp)	

def changeNTest():
	while(1):
		inp = input('Please enter new number of samples: ')
		inp = int(inp)
		if inp > 0:
			break
		else:
			print('Enter Error')
	target.changeNTest(inp)	

def sampleplot():
	target.samplePlot()

def sample():
	target.sample()

def plot():
	target.mplot()

def printGs():
	target.printSetting()

print('\n\n********************************************************************\n'
	  '*  Welcome to the equaivalent conductance analyzer for MRAM cells  *\n'
	  '********************************************************************\n\n')
newAyalsis()
print('\n\n'+INSTLIST)

while(1):
	inp = input('Please enter an instruction: ')
	if inp is 'help':
		inp = 7
	inp2 = int(inp)
	if (inp2 > 0 and inp2 < 9):
		if inp2 is 1:
			newAyalsis()
		elif inp2 is 2:
			sampleplot()
		elif inp2 is 3:
			sample()
		elif inp2 is 4:
			plot()
		elif inp2 is 5:
			changeR()
		elif inp2 is 6:
			printGs()	
		elif inp2 is 7:
			print(INSTLIST)
		elif inp2 is 8:
			break
	else:
		print('Enter Error')	
