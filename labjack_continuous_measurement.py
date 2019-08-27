import argparse
from Labjack import Labjack
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import csv

parser = argparse.ArgumentParser(
    description='Run a continuous readout of proxyboard DACs with Labjack')
parser.add_argument('filename', type=str,
                    help='save csv to filename')
parser.add_argument('period', nargs='?', type=int, default=60,
                    help='Period between measurements in seconds')

args = parser.parse_args()


fileName = args.filename
periodInSeconds = args.period


Labjack = Labjack()

Labjack.connectLabjack()
proxyBoardPinNames = ["IBIA", "IDB", "IREF", "VTES", "ITHR",
                      "VCN", "VCN2", "VCP", "VCLP", "VRST", "VPL", "VPH"]
header = ["Datetime"]
header.extend(proxyBoardPinNames)
with open(fileName, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
try:
    while True:
        results = Labjack.readLabjack()
        currentTime = datetime.datetime.now()
        data = [currentTime]
        data.extend(results)
        with open(fileName, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        time.sleep(periodInSeconds)
except KeyboardInterrupt:
    print('interrupted!')
