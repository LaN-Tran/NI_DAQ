"""
Author: Tran Le Phuong Lan
Date: 2025.10.29
Reference:
Example of analog input voltage acquisition. -> modify for multi-channel acquisition continuously.

This example demonstrates how to acquire a continuous amount of data
using the DAQ device's internal clock.

CAUTION: plotting while continuously acquiring data causes the program to crash, 
because the pc can read out the data fast enough from the device internal buffer.
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

plt.ion()

i= 0
sampling_rate = 10000.0 # [Hz]
with nidaqmx.Task() as task:
    # DIFF: (AI + vs AI -)
    # RSE: (referenced single-ended) (AI + vs AI GND)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.DIFF, 
                                         min_val=-5.0, max_val=5.0, units=VoltageUnits.VOLTS)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1", terminal_config=TerminalConfiguration.DIFF, 
                                         min_val=-5.0, max_val=5.0, units=VoltageUnits.VOLTS)
    
    task.timing.cfg_samp_clk_timing(sampling_rate, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=int(sampling_rate))
    task.start()
    print("Running task. Press Ctrl+C to stop.")

    try:
        total_data = []
        total_read = 0
        i = 0
        while True:
            data = task.read(number_of_samples_per_channel=int(sampling_rate))
            np_data = np.array(data)
            # print(f"{np_data.shape=}, {np_data.shape[1]=}")
            # # print(f"{data=}")
            # # time.sleep(1)
            # # # if number_of_samples_per_channel < sampling rate -> ERROR 
            # x_array = np.arange(0, np_data.shape[1]) + i *(1/sampling_rate)
            # plt.scatter(x_array, np_data[0, :], c = 'r', linewidths = 0.01)
            # plt.scatter(x_array, np_data[1, :], c = 'b', linewidths = 0.01)
            # plt.pause(0.05)
            # plt.ylim(-1,1)
            # i = i+1
            total_data.append(np_data)
            read = len(np_data[0, :])
            total_read += read
            print(f"Acquired data: {read} samples. Total {total_read}.", end="\r")
    except KeyboardInterrupt:
        pass
    finally:
        task.stop()
        print(f"\nAcquired {total_read} total samples.")
        total_data = np.hstack(total_data)
        print(f"{np.shape(np.transpose(total_data))=}")
        # reference: https://numpy.org/numpy-tutorials/save-load-arrays/
        # save the acquired data to a csv file                 must be no space in the header names 
        # -> otherwise, it will cause error when reading the csv file using pandas ! 
        np.savetxt("data3.csv", np.transpose(total_data), header="ch0,ch1",delimiter = ",")

