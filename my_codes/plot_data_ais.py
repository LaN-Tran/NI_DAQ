import matplotlib.pyplot as plt
import pandas as pd
# from scipy import signal
import numpy as np

# ======
# 2 plots
# ======

sampling_rate = 10000.0 # [Hz]

data = pd.read_csv(r"C:\Users\20245580\LabCode\NI_DAQ\data3.csv")
print(f"{data.head()=}")
print(repr(data.columns.tolist()))
ch0_v = data['ch0']
print(f"{ch0_v[0:3]=}\n{len(ch0_v)=}")
ch1_v = data['ch1']
print(f"{ch1_v[0:3]=}")

t_axis = np.arange(0, len(ch0_v)) / sampling_rate

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

ax1.set_xlabel('time [s]')
ax1.set_ylabel('v0 [V]')
ax1.grid()

ax2.set_xlabel('time [s]')
ax2.set_ylabel('v1 [V]')
ax2.grid()

ax1.plot(t_axis, ch0_v)
ax2.plot(t_axis, ch1_v)

plt.show()