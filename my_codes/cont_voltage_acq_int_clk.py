"""Example of analog input voltage acquisition.

This example demonstrates how to acquire a continuous amount of data
using the DAQ device's internal clock.
"""

import nidaqmx
# nidaqmx.constants is found in the 
# (where the nidaqmax package is installed in the conda virtual environment (e.g microcontroller))
# `C:\Users\<user-ID>\AppData\Local\anaconda3\envs\microcontroller\Lib\site-packages\nidaqmx\constants.py`
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import TerminalConfiguration
from nidaqmx.constants import VoltageUnits

import matplotlib.pyplot as plt
import numpy as np

import time

plt.ylim((-5, 5))
plt.ion()

i= 0
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.DIFF, 
                                         min_val=-5.0, max_val=5.0, units=VoltageUnits.VOLTS)
    
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config=TerminalConfiguration.DIFF, 
                                         min_val=-5.0, max_val=5.0, units=VoltageUnits.VOLTS)
    # DIFF: single-ended (AI + vs AI -)
    task.timing.cfg_samp_clk_timing(1000.0, sample_mode=AcquisitionType.CONTINUOUS)
    # task.timing.cfg_samp_clk_timing(1000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=10)
    task.start()
    print("Running task. Press Ctrl+C to stop.")

    try:
        total_read = 0
        i = 0
        while True:
            data = task.read(number_of_samples_per_channel=1000)
            # data = task.read(number_of_samples_per_channel=-1)
            np_data = np.array(data)
            # print(f"{np_data.shape=}, {np_data.shape[1]=}")
            # print(f"{data=}")
            # time.sleep(1)
            # # if number_of_samples_per_channel < sampling rate -> ERROR 
            x_array = np.arange(0, np_data.shape[1]) + i * 1000
            plt.scatter(x_array, np_data[0, :], c = 'r', linewidths = 0.01)
            plt.scatter(x_array, np_data[1, :], c = 'b', linewidths = 0.01)
            plt.pause(0.05)
            i = i+1
    except KeyboardInterrupt:
        pass
    finally:
        task.stop()
        print(f"\nAcquired {total_read} total samples.")
