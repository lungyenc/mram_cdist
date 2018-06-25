# GenAnalytical.py
# This program plots the SNR of multiple MRAM cells on a bit-line based on:
# [1] Rp (resistance-parallel) mean and variance
# [2] Rap (resistance-anti-parallel) mean and variance
# [3] number of MRAM cells on a bit-line
# note that we assume the random variables of each MRAM have the same 
# but independent distribution

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

class GenAnalytical:

    def __init__(self, rpM=None, rapM=None, rpStd=None, rapStd=None, nCell=None,
    histInt=None):
        self.rpM = rpM
        self.cpM = 1/rpM
        self.rapM = rapM
        self.capM = 1/rapM
        self.rpStd = rpStd
        self.cpV = rpStd * rpStd * (self.cpM**4)
        self.rapStd = rapStd
        self.capV = rapStd * rapStd * (self.capM**4)
        self.nCell = nCell
        self.histInt = histInt
        self.mdScalar = (self.cpM - self.capM)/math.sqrt(2)


    def ithMean(self, numberState):
        return numberState * self.cpM + (self.nCell - numberState) * self.capM

    def ithStd(self, numberState):
        return math.sqrt(numberState * self.cpV + (self.nCell - numberState) * 
        self.capV)

    def phi(self, x, i):    # private helper function - centered
        return 0.5 * (1 + math.erf(x / math.sqrt(2) / self.ithStd(i)))

    def phiScalar(self, x, i):  # private helper function - centered
        return 0.5 * (1 + math.erf(x* self.mdScalar / self.ithStd(i)))


    def probithj(self, i, j):
        if (j != 0 and j != self.nCell):
            return self.phiScalar(j+0.5-i, i) - self.phiScalar(j-0.5-i, i)
        elif (j == 0):
            return self.phiScalar(0.5-i, i)
        else:
            return 1 - self.phiScalar(self.nCell-0.5-i, i)



### Class Test ###
if __name__ == '__main__':
    test = GenAnalytical(6000, 12000, 350, 700, 32, 0.15)
    # print(test.ithMean(5)) # check ithMean
    # print(test.ithStd(16)) # check ithStd
    # print(test.phi(0.000043479, 16)-test.phi(-0.000043479, 16)) # check phi
    # print(test.phiScalar(0.5,16)-test.phiScalar(0,16))
    # sum = 0
    # for j in range(33):
    #     sum += test.probithj(16, j)
    # print(sum)

    print(test.phi(0.5*(test.cpM - test.capM), 0))
    print(test.probithj(0, 0))
    print(test.probithj(0, 1))
    print(test.probithj(1, 0))
    print(test.probithj(1, 1))
    print(test.probithj(1, 2))



