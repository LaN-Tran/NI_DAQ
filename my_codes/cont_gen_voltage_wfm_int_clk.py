"""
Author: Lan Le Phuong Tran
Date: 2025.10.29
Reference: https://github.com/ni/nidaqmx-python/blob/master/examples/analog_out/cont_gen_voltage_wfm_int_clk.py

Example of analog output voltage generation.

This example demonstrates how to output a continuous periodic
waveform using an internal sample clock.
"""

import numpy as np
import numpy.typing

import nidaqmx
from nidaqmx.constants import AcquisitionType


def generate_sine_wave(
    frequency: float,
    amplitude: float,
    sampling_rate: float,
    number_of_samples: int,
    phase_in: float = 0.0,
) -> tuple[numpy.typing.NDArray[numpy.double], float]:
    """Generates a sine wave with a specified phase.

    Args:
        frequency: Specifies the frequency of the sine wave.
        amplitude: Specifies the amplitude of the sine wave.
        sampling_rate: Specifies the sampling rate of the sine wave.
        number_of_samples: Specifies the number of samples to generate.
        phase_in: Specifies the phase of the sine wave in radians.

    Returns:
        Indicates a tuple containing the generated data and the phase
        of the sine wave after generation.
    """
    duration_time = number_of_samples / sampling_rate
    duration_radians = duration_time * 2 * np.pi
    phase_out = (phase_in + duration_radians) % (2 * np.pi)
    t = np.linspace(phase_in, phase_in + duration_radians, number_of_samples, endpoint=False)

    return (amplitude * np.sin(frequency * t), phase_out)

def generate_DC(
    amplitude: float,
    number_of_samples: int,
) -> numpy.typing.NDArray[numpy.double]:
    """Generates a sine wave with a specified phase.

    Args:
        frequency: Specifies the frequency of the sine wave.
        amplitude: Specifies the amplitude of the sine wave.
        sampling_rate: Specifies the sampling rate of the sine wave.
        number_of_samples: Specifies the number of samples to generate.
        phase_in: Specifies the phase of the sine wave in radians.

    Returns:
        Indicates a tuple containing the generated data and the phase
        of the sine wave after generation.
    """
    t = np.ones(number_of_samples)

    return (amplitude * t)

def main():
    """Continuously generates a sine wave."""
    with nidaqmx.Task() as task:
        sampling_rate = 1000.0
        number_of_samples = 1000
        task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
        task.ao_channels.add_ao_voltage_chan("Dev1/ao1")
        task.timing.cfg_samp_clk_timing(sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)

        actual_sampling_rate = task.timing.samp_clk_rate
        print(f"Actual sampling rate: {actual_sampling_rate:g} S/s")

        data_ao0 = generate_DC(
            amplitude=0,
            number_of_samples=number_of_samples,
        )
        data_ao1 = generate_DC(
            amplitude=0,
            number_of_samples=number_of_samples,
        )
        multiple_channels_data = np.vstack((data_ao1, data_ao0))
        task.write(multiple_channels_data)
        task.start()

        input("Generating voltage continuously. Press Enter to stop.\n")

        task.stop()


if __name__ == "__main__":
    main()
