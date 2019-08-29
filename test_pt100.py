import serial

PT100SerialPort = serial.Serial(port='COM4', baudrate=38400)


def readPT100():
    temperatures = []
    for i in range(8):
        serialTemp = PT100SerialPort.readline()
        tempHex = serialTemp[6:10]
        temp = int(tempHex, 16) / 1000.0
        temperatures.append(temp)
    return temperatures


for i in range(20):
    print(readPT100())

PT100SerialPort.close()
