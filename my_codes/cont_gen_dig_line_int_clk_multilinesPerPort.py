"""Example for generating digital signals.

This example demonstrates how to output a finite digital
waveform using the DAQ device's internal clock.
"""
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, LineGrouping

with nidaqmx.Task() as task:
    
    data_d00 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # data_d01 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    data_d01 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # data_d00 = np.array([1, 0, 0, 0])
    # data_d01 = np.array([0, 0, 0, 0])
    # convert boolen python list into numpy array of type bool
    # reference: https://stackoverflow.com/questions/43634495/convert-python-list-to-numpy-array-boolean
    # But this approach is not so elegant !
    # Maybe this approach is better: https://www.geeksforgeeks.org/python/python-boolean-array-in-numpy/
    data_d00 = np.array(data_d00, dtype=bool)
    data_d01 = np.array(data_d01, dtype=bool)

    task.do_channels.add_do_chan("Dev1/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    task.do_channels.add_do_chan("Dev1/port0/line2", line_grouping=LineGrouping.CHAN_PER_LINE)
    
    # task.timing.cfg_samp_clk_timing(
    #     # sample_rate=1 [Hz], sample_mode=AcquisitionType.FINITE, samps_per_chan=len(data_d00)
    #     rate=1, sample_mode=AcquisitionType.CONTINUOUS)
    task.timing.cfg_samp_clk_timing(
        # sample_rate=1 [Hz], sample_mode=AcquisitionType.FINITE, samps_per_chan=len(data_d00)
        1,sample_mode=AcquisitionType.CONTINUOUS)

    multiple_channels_data = np.vstack((data_d00, data_d01))
    
    number_of_samples_written = task.write(multiple_channels_data)
    task.start()
    print(f"Generating {number_of_samples_written} voltage samples.")
    input("Generating voltage continuously. Press Enter to stop.\n")
    task.stop()
