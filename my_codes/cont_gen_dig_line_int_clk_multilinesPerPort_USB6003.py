"""Example for generating digital signals.

This example demonstrates how to output a finite digital
waveform using the DAQ device's internal clock.
"""
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, LineGrouping
import time

rate = 1  # Hz
period = 1.0 / rate
loops = 5
with nidaqmx.Task() as task:
    
    data_d00 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    data_d01_negpulse = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    data_d01_pospulse = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # data_d00 = np.array([1, 0, 0, 0])
    # data_d01 = np.array([0, 0, 0, 0])
    # convert boolen python list into numpy array of type bool
    # reference: https://stackoverflow.com/questions/43634495/convert-python-list-to-numpy-array-boolean
    # But this approach is not so elegant !
    # Maybe this approach is better: https://www.geeksforgeeks.org/python/python-boolean-array-in-numpy/
    data_d00 = np.array(data_d00, dtype=bool)
    data_d01_negpulse = np.array(data_d01_negpulse, dtype=bool)

    task.do_channels.add_do_chan("Dev3/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    task.do_channels.add_do_chan("Dev3/port0/line2", line_grouping=LineGrouping.CHAN_PER_LINE)

    for j in range(loops):
        for i in range(len(data_d00)):
            t0 = time.perf_counter()
            task.write([bool(data_d00[i]), bool(data_d01_negpulse[i])], auto_start=True)
            # sleep the remainder of the period to keep ~10 Hz
            dt = period - (time.perf_counter() - t0)
            if dt > 0:
                time.sleep(dt)

    for j in range(loops):
            for i in range(len(data_d00)):
                t0 = time.perf_counter()
                task.write([bool(data_d00[i]), bool(data_d01_pospulse[i])], auto_start=True)
                # sleep the remainder of the period to keep ~10 Hz
                dt = period - (time.perf_counter() - t0)
                if dt > 0:
                    time.sleep(dt)

# The following code causes error for USB 6003 series
# Because (as explained by Claude):
# USB 6003 does not have internal clock for digital output; as in USB 6349.
# we have to implement the timing in sofware as above.
    # # task.timing.cfg_samp_clk_timing(
    # #     # sample_rate=1 [Hz], sample_mode=AcquisitionType.FINITE, samps_per_chan=len(data_d00)
    # #     rate=1, sample_mode=AcquisitionType.CONTINUOUS)
    # task.timing.cfg_samp_clk_timing(
    #     # sample_rate=1 [Hz], sample_mode=AcquisitionType.FINITE, samps_per_chan=len(data_d00)
    #     1,sample_mode=AcquisitionType.CONTINUOUS)

    # multiple_channels_data = np.vstack((data_d00, data_d01))
    
    # number_of_samples_written = task.write(multiple_channels_data)
    # task.start()
    # print(f"Generating {number_of_samples_written} voltage samples.")
    # input("Generating voltage continuously. Press Enter to stop.\n")
    # task.stop()
