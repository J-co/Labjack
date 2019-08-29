
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mpdt

data = np.loadtxt("decreasingTemp.csv",
                  delimiter=',', skiprows=1, dtype=str)
datetime = data[:, 0]
datetimeNum = mpdt.datestr2num(datetime)
timeDelta = (datetimeNum - datetimeNum[0])*1e5

temperature = data[:, 1]
voltageADCs = data[:, 2:].astype(np.float)

labels = ["IBIA", "IDB",
          "IREF", "VTES", "ITHR", "VCN", "VCN2", "VCP", "VCLP", "VRST", "VPL", "VPH"]

fig, ax = plt.subplots()
ax.plot(timeDelta, temperature)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Temperature [C]")

fig, ax = plt.subplots()
ax2 = plt.twinx(ax)
for i in range(12):
    ax.plot(timeDelta, voltageADCs[:, i], label=labels[i])
    ax2.plot(timeDelta, voltageADCs[:, i]/7.25)
ax.set_xlabel("Time [s]")
ax.set_ylabel("Voltage [mV]")
ax2.set_ylabel("ADU")
ax.legend()


fig, ax = plt.subplots()
for i in range(12):
    ax.plot(timeDelta, 100*voltageADCs[:, i] /
            voltageADCs[0, i], label=labels[i])
ax.set_xlabel("Time [s]")
ax.set_ylabel("Relative Voltage [%]")
ax.legend()


fig, ax = plt.subplots()
for i in range(12):
    ax.plot(temperature, 100*voltageADCs[:, i] /
            voltageADCs[0, i], label=labels[i], marker='.', linestyle='')
ax.set_xlabel("Temperature [C]")
ax.set_ylabel("Relative Voltage [%]")
ax.legend()


plt.show()
