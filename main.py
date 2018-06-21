# main.py
# This program plots the conductance distribution of multiple MRAM cells on a 
# bit-line based on:
# [1] Rp (resistance-parallel) mean and variance
# [2] Rap (resistance-anti-parallel) mean and variance
# [3] number of MRAM cells on a bit-line
# note that we assume the random variables of each MRAM have the same 
# but independent distribution

import GenSampling as gs

INSTLIST = ('[1] Start a new analysis\n' 
'[2] Sample and plot with the current settings\n'
'[3] Sameplew with the current settings\n'
'[4] Plot the distribition\n'
'[5] Change R\n'
'[6] Print the current settings\n'
'[7] Print instrcutions\n'
'[8] Exit the program\n')

target = gs.GenSampling(None, None, None, None, None, None)

def newAyalsis():
	print('Staring a new analysis...\n')
	global target
	target = gs.GenSampling(0, 0, 0, 0, 0, 0)	
	changeR()
	changeNCell()
	changeNTest()
	printGs()
	sampleplot()

def changeR():
	while(1):
		inp = input('Please enter new RpMean RapMean RpStd RapStd: (No leading' 
			'space)  Ex: 6000 12000 350 700\n')
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

print('\n\n'
'********************************************************************\n'
'*  Welcome to the equaivalent conductance analyzer for MRAM cells  *\n'
'********************************************************************\n\n')

print(INSTLIST)

while(1):
	inp = input('Please enter an instruction or help for the instrcution list: ')
	if inp == 'help':
		inp = '7'
	try:
		inp2 = int(inp)
	except ValueError:
		print('Please enter 1 to 8')
		continue
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
			print('\n'+INSTLIST)
		elif inp2 is 8:
			break
	else:
		print('Please enter 1 to 8')	
