"""Example for generating digital signals.

This example demonstrates how to output a finite digital
waveform using the DAQ device's internal clock.
"""

import nidaqmx
from nidaqmx.constants import AcquisitionType, LineGrouping

with nidaqmx.Task() as task:
    # data = [bool(i % 2) for i in range(1001)]
    data = [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    # for i in range(10):
    #     data += [True, False, False, False, False, False]

    task.do_channels.add_do_chan("Dev1/port0/line0", line_grouping=LineGrouping.CHAN_PER_LINE)
    
    task.timing.cfg_samp_clk_timing(
        1, sample_mode=AcquisitionType.CONTINUOUS, samps_per_chan=len(data)
    )
    
    number_of_samples_written = task.write(data)
    task.start()
    print(f"Generating {number_of_samples_written} voltage samples.")
    input("Generating voltage continuously. Press Enter to stop.\n")
    task.stop()
