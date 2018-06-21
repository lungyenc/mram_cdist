# GenSampling.py
# This program plots the conductance distribution of multiple MRAM cells on a 
# bit-line based on:
# [1] Rp (resistance-parallel) mean and variance
# [2] Rap (resistance-anti-parallel) mean and variance
# [3] number of MRAM cells on a bit-line
# note that we assume the random variables of each MRAM have the same 
# but independent distribution

import numpy as np
import matplotlib.pyplot as plt

class GenSampling:

    def __init__(self, rpM=None, rapM=None, rpStd=None, rapStd=None, nCell=None,
    nTest=None, histInt=None):
        if (rpM is None or rapM is None or rpStd is None or rapStd is None or 
        nCell is None or nTest is None):
            self.__init__(0, 0, 0, 0, 0, 0)
            self.rdy = False
            print('default constructor!')
        else:
            self.changeR(rpM, rapM, rpStd, rapStd) # Rp, Rap mean, std
            self.changeNCell(nCell)                # number of MRAM cells
            self.changeNTest(nTest)                # number of samples
            if histInt is None:
                self.changeHistInt(0.015)       # histogram bin interval (mA/V)
            else:
                self.changeHistInt(histInt)
            self.rdy = True

    def isReady(self):
        return self.rdy

    def notReady(self):
        print('Initialization is needed')

    def changeRpM(self, rpM):
        self.rpM = rpM
        self.ceq = None

    def changeRapM(self, rapM):
        self.rapM = rapM
        self.ceq = None

    def changeRpStd(self, rpStd):
        self.rpStd = rpStd
        self.ceq = None

    def changeRapStd(self, rapStd):
        self.rapStd = rapStd  
        self.ceq = None              

    def changeNCell(self, nCell):
        self.nCell = nCell
        self.ceq = None

    def changeNTest(self, nTest):
        self.nTest = nTest
        self.ceq = None

    def changeHistInt(self, histInt):
        self.histInt = histInt

    def changeR(self, rpM, rapM, rpStd, rapStd):
        self.changeRpM(rpM)            # Rp mean
        self.changeRapM(rapM)          # Rap mean
        self.changeRpStd(rpStd)        # Rp standard deviation 
        self.changeRapStd(rapStd)      # Rap standard deviation

    def printSetting(self):
        if self.rdy:
            print('Current setting: Rp mean= '+ str(self.rpM) +' Rap mean= '+ 
            str(self.rapM) +' Rp Std= '+ str(self.rpStd) +
            ' Rap Std= '+ str(self.rapStd) +' Number of cell= '+ str(self.nCell)
            +' Number samples= '+ str(self.nTest))
        else:
            self.notReady()

    def samplePlot(self, nTest=None):
        if self.rdy:
            if nTest is not None:
                self.changeNTest(nTest)
            else:
                self.sample()
                self.mplot()
        else:
            self.notReady()

    def sample(self):
        if self.rdy:
            print('Sapmling '+str(self.nTest)+' times')
            self.ceq = np.zeros((self.nTest,self.nCell+1))
            for t in range(self.nTest):
                for i in range(self.nCell+1):   # the circuit has N+1 output 
                #states: [0 ... Ncell] cells store 0 and [Ncell ... 0] 
                #cells store 1
                    ctemp = 0
                    for j in range(i):
                        ctemp = ctemp + 1/np.random.normal(self.rpM,self.rpStd)
                    for j in range(self.nCell-i):
                        ctemp = ctemp + 1/np.random.normal(self.rapM,self.rapStd)
                    self.ceq[t, i] = ctemp
            self.ceq *= 1000   
        else:
            self.notReady()

    def mplot(self):
        if self.rdy:
            if self.ceq is None:
                print('There\'s no data for the current setting. Do you want to'
                ' sample now? ')
                ans = input('Y for yes')
                if ans is 'Y':
                    self.samplePlot()
                else:
                    print('Please run sample() first. Exiting the program...')
            else:
                print('Plotting from the last sample')
                hMin = np.min(self.ceq)
                hMax = np.max(self.ceq)
                hist_bin = np.linspace(hMin, hMax, (hMax-hMin)//self.histInt)       
                plt.hist(self.ceq, hist_bin, width=0.01)
                plt.show()
        else:
            self.notReady()



