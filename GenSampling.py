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

    def meanPlot(self):
        if self.rdy:
            mean = np.mean(self.ceq, axis=0)
            plt.plot(mean,'-o')
            plt.show()
        else:
            self.notReady()

    def variancePlot(self):
        if self.rdy:
            variance = np.std(self.ceq, axis = 0)
            plt.plot(variance,'-o')
            plt.show()
        else:
            self.notReady()            

    def snrPlot(self):
        if self.rdy:
            mean = np.mean(self.ceq, axis=0)
            for i in range(len(mean)-1, 0, -1):
                mean[i] -= mean[i-1]
            variance = np.std(self.ceq, axis = 0)
            for i in range(len(variance)-1, 0, -1):
                #variance[i] = max(variance[i], variance[i-1])
                variance[i] = variance[i] + variance[i-1]
            snr = (mean/variance)
            snr = snr * snr 
            snr = snr[1:len(snr)]
            plt.plot(snr,'-o')
            plt.show()
        else:
            self.notReady()   

    def snrNcellPlot(self, nCells):
        if self.rdy:
            print('Sapmling the lowest SNR cases...')
            ceq = np.zeros((nCells-1, self.nTest, 2))
            for k in range(2, nCells+1, 1):
                for t in range(self.nTest):
                    for i in range(k-1,k+1,1):
                        ctemp = 0
                        for j in range(i):
                            ctemp = ctemp + 1/np.random.normal(self.rpM,self.rpStd)
                        for j in range(k-i):
                            ctemp = ctemp + 1/np.random.normal(self.rapM,self.rapStd)
                        ceq[k-2, t, i-k+1] = ctemp
            ceq *= 1000
            mean = np.mean(ceq, axis=1)
            mean = mean[:,1] - mean[:,0]
            variance = np.std(ceq, axis = 1)
            variance= variance[:, 1] + variance[:, 0]
            snr = (mean/variance)
            snr = snr * snr 
            plt.plot(range(2, nCells+1, 1), snr,'-o')
            plt.show()
        else:
            self.notReady()            


### Class Test ###
if __name__ == '__main__':
    test = GenSampling(6000, 12000, 350, 700, 32, 1000)
    test.printSetting()
    #test.samplePlot()
    test.sample()
    #test.meanPlot()
    #test.variancePlot()
    test.snrPlot()
    #test.snrNcellPlot(128)

