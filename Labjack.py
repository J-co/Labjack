from labjack import ljm
import numpy as np


class Labjack:
    """ 
    Class that connects/disconnects to a labjack handle
     and reads the first 12 analog input pins and returns them in mV
    """

    def __init__(self):
        self.proxyBoardPinNames = ["IBIA", "IDB",
                                   "IREF", "VTES", "ITHR", "VCN", "VCN2", "VCP", "VCLP", "VRST", "VPL", "VPH"]
        self.labjackPinNames = ["AIN0", "AIN1", "AIN2", "AIN3", "AIN4",
                                "AIN5", "AIN6", "AIN7", "AIN8", "AIN9", "AIN10", "AIN11"]
        self.labjackHandle = None
        self.labjackNumChannels = len(self.labjackPinNames)

    def connectLabjack(self):
        self.labjackHandle = ljm.openS("T7", "ANY", "ANY")
        info = ljm.getHandleInfo(self.labjackHandle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

        ljm.eWriteName(self.labjackHandle, "AIN_ALL_RANGE", 10.0)
        ljm.eWriteName(self.labjackHandle, "AIN_ALL_RESOLUTION_INDEX", 8)

    def disconnectLabjack(self):
        ljm.close(self.labjackHandle)

    def readLabjack(self):
        results = ljm.eReadNames(
            self.labjackHandle, self.labjackNumChannels, self.labjackPinNames)
        # convert to mV and round
        results = [round(elem*1000, 2) for elem in results]
        print("\neReadNames results: ")
        for i in range(self.labjackNumChannels):
            print("    Name - %s, value [mV]: %f" %
                  (self.proxyBoardPinNames[i], results[i]))
        return results

    def readLabjackMean(self, repetitions):
        results = np.zeros((self.labjackNumChannels, repetitions))
        for i in range(repetitions):
            singleRead = self.readLabjack()
            results[:, i] = singleRead
        meanResult = np.mean(results, axis=1)
        return meanResult
