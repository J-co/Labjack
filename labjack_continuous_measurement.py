"""
This is a script that starts a continuous readout of the analog input pins
of the the Labjack T7 and saves them to a csv file. Additionally a PT100 
sensor is read out and saved as well.

Invoke this script from terminal like:
python scriptname.py filename.csv periodBetweenMeasurements

Make sure the COM Port for the PT100 is correct and that it is connected to the first slot
of the PT100 read-out device
"""
import argparse
from Labjack import Labjack
import time
import datetime
import csv
import serial


# Argument Parser
parser = argparse.ArgumentParser(
    description='Run a continuous readout of proxyboard DACs with Labjack')
parser.add_argument('filename', type=str,
                    help='save csv to filename')
parser.add_argument('period', nargs='?', type=int, default=60,
                    help='Period between measurements in seconds')
args = parser.parse_args()
fileName = args.filename
periodInSeconds = args.period

# Connect to Labjack
Labjack = Labjack()
Labjack.connectLabjack()
proxyBoardPinNames = ["IBIA [mV]", "IDB [mV]", "IREF [mV]", "VTES [mV]", "ITHR [mV]",
                      "VCN [mV]", "VCN2 [mV]", "VCP [mV]", "VCLP [mV]", "VRST [mV]", "VPL [mV]", "VPH [mV]"]

# Connect to PT100
PT100SerialPort = serial.Serial(port='COM4', baudrate=38400)


def readPT100(nSensors):
    # This function reads all 8 channels of the PT100 readout device
    # and returns the first nSensors
    temperatures = []
    for i in range(8):
        serialTemp = PT100SerialPort.readline()
        tempHex = serialTemp[6:10]
        temp = int(tempHex, 16) / 1000.0
        temperatures.append(temp)
    return temperatures[:nSensors]


# csv file setup
header = ["Datetime", "Temperature [K]"]
header.extend(proxyBoardPinNames)
with open(fileName, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
try:
    while True:
        labjackResults = Labjack.readLabjack()
        temperatures = readPT100(1)
        currentTime = datetime.datetime.now()
        data = [currentTime, temperatures[0]]
        data.extend(labjackResults)
        with open(fileName, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        time.sleep(periodInSeconds)
except KeyboardInterrupt:
    PT100SerialPort.close()
    print('interrupted!')
