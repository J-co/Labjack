from labjack import ljm


class Labjack:
    def __init__(self):
        self.proxyBoardPinNames = []
        self.labjackPinNames = ["AIN0", "AIN1", "AIN2", "AIN3", "AIN4",
                                "AIN5", "AIN6", "AIN7", "AIN8", "AIN9", "AIN10", "AIN11", "AIN12"]
        self.labjackHandle = None
        self.labjackNumFrames = len(self.labjackPinNames)

    def connectLabjack(self):
        self.labjackHandle = ljm.openS("T7", "ANY", "ANY")
        info = ljm.getHandleInfo(self.labjackHandle)
        print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
              "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
              (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

    def disconnectLabjack(self):
        ljm.close(self.labjackHandle)

    def readLabjack(self):
        results = ljm.eReadNames(
            self.labjackHandle, self.labjackNumFrames, self.labjackPinNames)
        print("\neReadNames results: ")
        for i in range(self.labjackNumFrames):
            print("    Name - %s, value : %f" %
                  (self.labjackPinNames[i], results[i]))
        return results