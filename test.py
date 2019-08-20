from Labjack import Labjack
import numpy as np
import matplotlib.pyplot as plt


Labjack = Labjack()

Labjack.connectLabjack()

results = np.zeros((13, 100))

for i in range(100):
    result = Labjack.readLabjack()
    results[:, i] = result

fig, ax = plt.subplots()
ax.plot(results[2, :]*1000)
plt.show()

Labjack.disconnectLabjack()
